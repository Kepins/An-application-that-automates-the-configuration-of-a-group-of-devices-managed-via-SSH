from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery import shared_task

from application.api.serializers import RunScriptStatusSerializer
from application.utils.task_utils import (
    run_script,
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

    status, warns = run_script(device_pk, group_pk, script_pk)
    response.initial_data["status"] = status.value
    response.initial_data["warnings"] = warns
    response.is_valid(raise_exception=True)
    async_to_sync(channel_layer.group_send)(
        f"group",
        {
            "type": "send.runscript.update",  # This is the custom consumer type you define
            "message": response.data,
        },
    )
    return
