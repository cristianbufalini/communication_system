import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WebRTCConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'chat_group'  # Ajusta este nombre según tu necesidad

    async def connect(self):
        await self.channel_layer.group_add(
            self.GROUP_NAME,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.GROUP_NAME,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        usuario = text_data_json.get('usuario', 'Anónimo')  # Obtener el usuario o establecer como 'Anónimo' si no está presente

        # Puedes hacer algo con el mensaje y el usuario recibido si es necesario
        # En este ejemplo, simplemente reenviamos el mensaje al grupo de WebSocket

        await self.channel_layer.group_send(
            self.GROUP_NAME,
            {
                'type': 'chat.message',
                'message': message,
                'usuario': usuario,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        usuario = event.get('usuario', 'Anónimo')  # Obtener el usuario o establecer como 'Anónimo' si no está presente

        # Enviar el mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'usuario': usuario,
        }))
