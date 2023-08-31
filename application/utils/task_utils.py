from fabric import Connection
from io import StringIO
from paramiko import SSHException, RSAKey

from application.models import Device, Group, CustomUser


def create_connection(device_pk, group_pk):
    group = Group.objects.get(pk=group_pk)
    user = CustomUser.objects.first()
    device = Device.objects.get(pk=device_pk)
    if key_pair := device.key_pair:
        try:  # try connect using device's key
            key_content = key_pair.private_key_content
            private_key = RSAKey(file_obj=StringIO(key_content))
            return Connection(
                host=device.hostname,
                user=device.username,
                port=device.port,
                connect_kwargs={"pkey": private_key, "timeout": 10},
            )
        except SSHException:
            print("Wrong private key")
    if device.password:  # try connect using device's password
        return Connection(
            host=device.hostname,
            port=device.port,
            user=device.username,
            connect_kwargs={"password": device.password, "timeout": 10},
        )
    if key_pair2 := group.key_pair:
        if (
            key_pair2 != key_pair
        ):  # try connect using group's key if it is different from group's key
            try:
                key_content = key_pair2.private_key_content
                private_key = RSAKey(file_obj=StringIO(key_content))
                return Connection(
                    host=device.hostname,
                    user=device.username,
                    port=device.port,
                    connect_kwargs={"pkey": private_key, "timeout": 10},
                )
            except SSHException:
                print("Wrong private key")
    if key_pair3 := user.key_pair:
        if key_pair3 not in [key_pair, key_pair2]:
            try:  # try connect using user's key if it is different from device's key and group's key
                key_content = key_pair2.private_key_content
                private_key = RSAKey(file_obj=StringIO(key_content))
                return Connection(
                    host=device.hostname,
                    user=device.username,
                    port=device.port,
                    connect_kwargs={"pkey": private_key, "timeout": 10},
                )
            except SSHException:
                print("Wrong private key")
    else:  # password and key_pair not specified
        print("No device and key_pair specified")
        return False
