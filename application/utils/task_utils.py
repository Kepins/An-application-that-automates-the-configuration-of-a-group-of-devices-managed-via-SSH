from enum import Enum
from io import StringIO
import socket

from fabric import Connection
from invoke import UnexpectedExit
import paramiko
from paramiko.ssh_exception import AuthenticationException


from application.exceptions import SshConnectionException
from application.models import Device, Group, Script


class ConnectionStatus(Enum):
    OK = "Ok"
    BadAuthMethods = "Bad authentication methods"
    HostNotAvailable = "(Network)Host not available"


class RunScriptStatus(Enum):
    ErrorWhileRunningScript = "Error while running script"
    OK = "Ok"
    BadAuthMethods = "Bad authentication methods"
    HostNotAvailable = "(Network)Host not available"


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


def check_connection(device_id, group_id):
    device = Device.objects.get(pk=device_id)
    group = Group.objects.get(pk=group_id)
    password = None
    key = None
    warns = []
    try:
        transport = paramiko.Transport((device.hostname, device.port))
        transport.connect()
    except paramiko.ssh_exception.SSHException:
        status = ConnectionStatus.HostNotAvailable
        return status, warns, password, key
    except socket.gaierror:
        status = ConnectionStatus.HostNotAvailable
        warns.append("Invalid hostname or port")
        return status, warns, password, key

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

    transport.close()
    if authenticated:
        status = ConnectionStatus.OK
    else:
        status = ConnectionStatus.BadAuthMethods
    return status, warns, password, key


def run_script(device_pk, group_pk, script_pk):
    status, warns, password, key = check_connection(device_pk, group_pk)
    if status != ConnectionStatus.OK:
        return status, warns
    device = Device.objects.get(pk=device_pk)
    if key:
        connection = Connection(
            host=device.hostname,
            user=device.username,
            port=device.port,
            connect_kwargs={"pkey": key, "timeout": 10},
        )
    else:
        connection = Connection(
            host=device.hostname,
            user=device.username,
            port=device.port,
            connect_kwargs={"password": password, "timeout": 10},
        )
    script = Script.objects.get(pk=script_pk)
    try:
        connection.run(script.script, hide=True)
        status = RunScriptStatus.OK
    except AuthenticationException:
        warns.append("Auth error during creating connection")
        status = RunScriptStatus.HostNotAvailable
    except UnexpectedExit as e:
        warns.append(e.args[0].stderr)
        status = RunScriptStatus.ErrorWhileRunningScript
    return status, warns
