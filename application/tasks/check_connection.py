import paramiko

from celery import shared_task

from application.models import Device, Group


class SshConnectionException(Exception):
    def __init__(self, error):
        self.error = error


def test_auth_key(transport, username, key_pair):
    try:
        # try to create instance of key from key content
        # TODO change key_type to be dynamic
        pk = paramiko.pkey.PKey.from_type_string(
            "ssh-ed25519", key_pair.private_key_content
        )
    except paramiko.ssh_exception.SSHException:
        # key instance cannot be created
        raise SshConnectionException("Wrong key format")

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
    device = Device.objects.get(pk=device_id)
    group = Group.objects.get(pk=group_id)
    try:
        transport = paramiko.Transport((device.hostname, device.port))
        transport.connect()
    except paramiko.ssh_exception.SSHException:
        print("Host not available")
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
        print("Auth")
        print(warns)
    else:
        print("Couldn't auth")
