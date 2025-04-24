import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        await self.channel_layer.group_add(
            f"order_{self.order_id}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"order_{self.order_id}",
            self.channel_name
        )

    async def order_update(self, event):
        await self.send(text_data=json.dumps(event))