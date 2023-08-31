from celery import shared_task
from fabric import Connection, task
from io import StringIO
from django.conf import settings
import paramiko
from paramiko import RSAKey, SSHException
import os
from application.models import Device, Group, Script


@shared_task(ignore_result=True)
def run_script_on_device(group_pk, device_pk, script_pk):
    if connection := create_connection(device_pk):
        return  # inform via websockets
    script = Script.objects.get(pk=script_pk)
    try:
        result = connection.run(script.script, hide=True)
        print(result.stdout)
        return  # worked websocket
    except SSHException as e:
        print("SSH connection error:", str(e))
        return  # fail websocket


@shared_task(ignore_result=True)
def check_connection(group_pk, device_pk):
    if connection := create_connection(device_pk):
        return  # inform via websockets
    try:
        test_script = "#!/bin/bash\n echo HI"
        result = connection.run(test_script, hide=True)
        if result == "HI":
            return  # goood websocket
        else:
            return  # fail websocket
    except SSHException as e:
        print("SSH connection error:", str(e))
        # websocket


def create_connection(device_pk):
    device = Device.objects.get(pk=device_pk)
    if key_pair := device.key_pair:
        try:
            key_content = key_pair.private_key_content
            private_key = paramiko.RSAKey(file_obj=StringIO(key_content))
            return Connection(
                host=device.hostname,
                user=device.username,
                connect_kwargs={"pkey": private_key, "timeout": 10},
            )
        except SSHException:
            print("Wrong private key")
    if device.password:
        return Connection(
            host=device.hostname,
            user=device.username,
            connect_kwargs={"password": device.password, "timeout": 10},
        )
    else:  # password and key_pair not specified
        return False
