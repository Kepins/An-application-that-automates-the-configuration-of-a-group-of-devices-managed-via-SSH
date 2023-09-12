import paramiko

from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from application.api.serializers.conn_status_serializer import ConnStatusSerializer
from application.utils.task_utils import check_connection


@shared_task(ignore_result=True)
def check_connection_task(group_id, device_id, request_uuid=None):
    response = ConnStatusSerializer(
        partial=True,
        data={
            "request_uuid": request_uuid,
            "device": device_id,
            "warnings": [],
        },
    )

    channel_layer = get_channel_layer()

    status, warns, password, key = check_connection(device_id, group_id)
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
