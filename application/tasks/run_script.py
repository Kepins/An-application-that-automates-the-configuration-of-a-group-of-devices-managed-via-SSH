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
            "result_std": "",
            "result_err": "",
        },
    )
    channel_layer = get_channel_layer()

    status, warns, result_std, result_err = run_script(device_pk, group_pk, script_pk)
    response.initial_data["status"] = status.value
    response.initial_data["warnings"] = warns
    response.initial_data["result_std"] = result_std
    response.initial_data["result_err"] = result_err
    response.is_valid(raise_exception=True)
    async_to_sync(channel_layer.group_send)(
        f"group",
        {
            "type": "send.runscript.update",  # This is the custom consumer type you define
            "message": response.data,
        },
    )
    return
