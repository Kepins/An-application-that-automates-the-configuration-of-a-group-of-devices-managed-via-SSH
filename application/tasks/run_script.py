from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from celery import shared_task
from fabric import Connection
from invoke import UnexpectedExit
from paramiko import AuthenticationException

from application.api.serializers import RunScriptStatusSerializer
from application.models import Script, Device
from application.utils.task_utils import (
    check_connection,
    RunScriptStatus,
)


@shared_task(ignore_result=True)
def run_script_on_device(group_pk, device_pk, script_pk, request_uuid):
    response = RunScriptStatusSerializer(
        partial=True,
        data={
            "request_uuid": request_uuid,
            "device": device_pk,
            "warnings": [],
        },
    )
    channel_layer = get_channel_layer()

    status, warns, password, key = check_connection(device_pk, group_pk)
    if status != RunScriptStatus.OK:
        response.initial_data["status"] = status.value
        response.initial_data["warnings"] = warns
        response.is_valid(raise_exception=True)
        async_to_sync(channel_layer.group_send)(
            f"group",
            {
                "type": "send.checkconn.update",  # This is the custom consumer type you define
                "message": response.data,
            },
        )
        return
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
        response.initial_data["status"] = RunScriptStatus.OK.value
    except AuthenticationException as e:
        warns.append("Auth error during creating connection")
        response.initial_data["status"] = RunScriptStatus.OK.value
    except UnexpectedExit as e:
        warns.append(e.args[0].stderr)
        response.initial_data["status"] = RunScriptStatus.OK.value
    response.initial_data["warnings"] = warns
    response.is_valid(raise_exception=True)
    async_to_sync(channel_layer.group_send)(
        f"group",
        {
            "type": "send.checkconn.update",
            "message": response.data,
        },
    )
