import json
from io import StringIO

import paramiko

from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from application.models import Device, Group


class SshConnectionException(Exception):
    def __init__(self, error):
        self.error = error


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

    return True


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

    return True


@shared_task(ignore_result=True)
def check_connection(group_id, device_id):
    channel_layer = get_channel_layer()
    device = Device.objects.get(pk=device_id)
    group = Group.objects.get(pk=group_id)
    try:
        transport = paramiko.Transport((device.hostname, device.port))
        transport.connect()
    except paramiko.ssh_exception.SSHException:
        async_to_sync(channel_layer.group_send)(
            f"group",
            {
                "type": "send.checkconn.update",  # This is the custom consumer type you define
                "message": json.dumps(
                    {
                        "id_device": device.id,
                        "status": "Host not available",
                        "warnings": [],
                    }
                ),
            },
        )
        return

    warns = []
    authenticated = False

    # try
    if not authenticated and device.key_pair:
        try:
            authenticated = test_auth_key(transport, device.username, device.key_pair)
        except SshConnectionException as e:
            warns.append(e.error)

    if not authenticated and group.key_pair:
        try:
            authenticated = test_auth_key(transport, device.username, group.key_pair)
        except SshConnectionException as e:
            warns.append(e.error)

    if not authenticated and device.password:
        try:
            authenticated = test_auth_pass(transport, device.username, device.password)
        except SshConnectionException as e:
            warns.append(e.error)

    transport.close()

    if authenticated:
        async_to_sync(channel_layer.group_send)(
            f"group",
            {
                "type": "send.checkconn.update",  # This is the custom consumer type you define
                "message": json.dumps(
                    {
                        "id_device": device.id,
                        "status": "Ok",
                        "warnings": warns,
                    }
                ),
            },
        )
        print("Auth")
        print(warns)
    else:
        async_to_sync(channel_layer.group_send)(
            f"group",
            {
                "type": "send.checkconn.update",  # This is the custom consumer type you define
                "message": json.dumps(
                    {
                        "id_device": device.id,
                        "status": "Bad authentication methods",
                        "warnings": warns,
                    }
                ),
            },
        )
        print(warns)
        print("Couldn't auth")
