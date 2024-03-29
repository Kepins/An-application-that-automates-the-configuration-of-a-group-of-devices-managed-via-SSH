import binascii
from enum import Enum
from io import StringIO
import socket

from fabric import Connection
from invoke import UnexpectedExit
import paramiko
from paramiko.ssh_exception import AuthenticationException
from paramiko import PKey
import base64

from application.exceptions import SshConnectionException
from application.models import Device, Group, Script


class ConnectionStatus(Enum):
    OK = "Ok"
    BadAuthMethods = "Bad authentication methods"
    HostNotAvailable = "Connection problem"
    BadDevicePublicKey = "Bad public key format"


class RunScriptStatus(Enum):
    ErrorWhileRunningScript = "Error while running script"
    OK = "Ok"
    BadAuthMethods = "Bad authentication methods"
    HostNotAvailable = "Connection problem"


def load_key(pkey_content):
    classes = [paramiko.RSAKey, paramiko.Ed25519Key, paramiko.DSSKey, paramiko.ECDSAKey]
    for c in classes:
        try:
            return c(file_obj=StringIO(pkey_content))
        except (paramiko.ssh_exception.SSHException, IOError) as e:
            pass
    raise SshConnectionException("Wrong key format")


def test_auth_key(transport, username, key_pair):
    pk = load_key(key_pair.private_key_content)
    try:
        # try to authenticate
        transport.auth_publickey(username, pk)
    except paramiko.ssh_exception.BadAuthenticationType:
        raise SshConnectionException("Key-auth method not allowed")
    except paramiko.ssh_exception.AuthenticationException:
        raise SshConnectionException("Key-auth failed")
    except paramiko.ssh_exception.SSHException:
        raise SshConnectionException("Network error")

    return True, pk


def test_auth_pass(transport, username, password):
    try:
        # try to authenticate
        transport.auth_password(username, password)
    except paramiko.ssh_exception.BadAuthenticationType:
        raise SshConnectionException("Password-auth method not allowed")
    except paramiko.ssh_exception.AuthenticationException:
        raise SshConnectionException("Password-auth failed")
    except paramiko.ssh_exception.SSHException:
        raise SshConnectionException("Network error")

    return True, password


def check_connection(device_id, group_id, close_transport=True):
    device = Device.objects.get(pk=device_id)
    group = Group.objects.get(pk=group_id)
    warns = []

    hostkey = None
    if device.public_key:
        try:
            key_bytes = base64.b64decode(device.public_key.split(" ")[1])
        except (binascii.Error, IndexError):
            status = ConnectionStatus.BadDevicePublicKey
            warns.append("Invalid format of device public key")
            return status, warns, None
        try:
            hostkey = PKey.from_type_string(device.public_key.split(" ")[0].lower(), key_bytes)
        except:
            status = ConnectionStatus.BadDevicePublicKey
            warns.append("Invalid format of device public key")
            return status, warns, None
    try:
        transport = paramiko.Transport((device.hostname, device.port))
    except socket.gaierror as e:
        status = ConnectionStatus.HostNotAvailable
        warns.append("Invalid hostname or port")
        return status, warns, None
    try:
        transport.connect(hostkey=hostkey)
    except paramiko.ssh_exception.SSHException as e:
        status = ConnectionStatus.HostNotAvailable
        if str(e) == "Bad host key from server":
            warns.append("Device's SSH server uses different public key than specified")
        else:
            warns.append(str(e))
        transport.close()
        return status, warns, None

    if not device.public_key:
        device_key = transport.get_remote_server_key()
        device.public_key = f"ssh-{device_key.algorithm_name} {device_key.get_base64()}"
        device.save()
    authenticated = False

    # try
    if not authenticated and device.key_pair:
        try:
            authenticated, key = test_auth_key(
                transport, device.username, device.key_pair
            )
        except SshConnectionException as e:
            warns.append(f"(Device Key){e.error}")

    if not authenticated and group.key_pair:
        try:
            authenticated, key = test_auth_key(
                transport, device.username, group.key_pair
            )
        except SshConnectionException as e:
            warns.append(f"(Group Key){e.error}")

    if not authenticated and device.password:
        try:
            authenticated, password = test_auth_pass(
                transport, device.username, device.password
            )
        except SshConnectionException as e:
            warns.append(f"(Device Password){e.error}")

    if not any([device.key_pair, group.key_pair, device.password]):
        warns.append("No authentication method")

    if authenticated:
        status = ConnectionStatus.OK
    else:
        status = ConnectionStatus.BadAuthMethods

    if close_transport or status != ConnectionStatus.OK:
        transport.close()
        return status, warns, None
    return status, warns, transport


def run_script(device_pk, group_pk, script_pk):
    result_std = ""
    result_err = ""
    status, warns, transport = check_connection(device_pk, group_pk, close_transport=False)
    if status != ConnectionStatus.OK:
        return status, warns, result_std, result_err
    script = Script.objects.get(pk=script_pk)
    channel = transport.open_session()

    channel.exec_command(script.script)
    channel.recv_exit_status()

    if channel.exit_status == 0:
        status = RunScriptStatus.OK
    else:
        status = RunScriptStatus.ErrorWhileRunningScript

    stdout = channel.makefile('r')
    stderr = channel.makefile_stderr('r')

    result_std = stdout.read().decode('utf-8')
    result_err = stderr.read().decode('utf-8')

    stderr.close()
    stdout.close()

    channel.close()
    transport.close()
    return status, warns, result_std, result_err
