import json

from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"group"  # Set the group name

        # Add the client to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_checkconn_update(self, event):
        # Send a custom message to the client
        await self.send(text_data=json.dumps(event))
