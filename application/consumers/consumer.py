import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import jwt

from application.models import CustomUser


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"group"  # Set the group name
        token = self.scope['url_route']['kwargs']['token']
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            try:
                database_sync_to_async(self.get_user)(data["user_id"])
            except CustomUser.DoesNotExist:
                logging.error("User does not exist")
                await self.close()
                return
        except (
            jwt.exceptions.DecodeError,
            jwt.exceptions.InvalidTokenError,
            jwt.ExpiredSignatureError,
        ):
            logging.error("Invalid token")
            await self.close()
            return

        # Add the client to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    def get_user(self, user_id):
        return CustomUser.objects.get(pk=user_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_checkconn_update(self, event):
        # Send a custom message to the client
        await self.send(text_data=json.dumps(event))

    async def send_runscript_update(self, event):
        # Send a custom message to the client
        await self.send(text_data=json.dumps(event))
