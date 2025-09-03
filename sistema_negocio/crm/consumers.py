# crm/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conv_id']
        self.room_group_name = f'chat_{self.room_name}'

        # Unirse a un grupo de chat específico para esta conversación
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Esta función se llama cuando el servidor recibe un mensaje desde el WebSocket
    async def chat_message(self, event):
        # Envía el mensaje de vuelta al cliente (JavaScript)
        await self.send(text_data=json.dumps(event['message']))