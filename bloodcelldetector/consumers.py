# bloodcelldetector/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'progress_group'

        # Debug logging
        print("Connecting to progress_group")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Debug logging
        print("Disconnecting from progress_group")

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Debug logging
        print(f"Received message: {message}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'progress_message',
                'message': message
            }
        )

    # Receive message from room group
    async def progress_message(self, event):
        message = event['message']

        # Debug logging
        print(f"Sending message: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
