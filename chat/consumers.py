# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class WebRTCConsumer(AsyncWebsocketConsumer):
#     GROUP_NAME = 'chat_group'  # Ajusta este nombre según tu necesidad

#     async def connect(self):
#         await self.channel_layer.group_add(
#             self.GROUP_NAME,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.GROUP_NAME,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json.get('message', '')
#         usuario = text_data_json.get('usuario', 'Anónimo')
#         audio_url = text_data_json.get('audio_url', '')

        

#         await self.channel_layer.group_send(
#             self.GROUP_NAME,
#             {
#                 'type': 'chat.message',
#                 'message': message,
#                 'usuario': usuario,
#                 'audio_url': audio_url,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         usuario = event.get('usuario', 'Anónimo')
#         audio_url = event.get('audio_url', '')

#         # Enviar el mensaje al WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'usuario': usuario,
#             'audio_url': audio_url,
#         }))

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WebRTCConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'chat_group'

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
        message_type = text_data_json.get('type', '')  # 'text' or 'audio'
        
        if message_type == 'text':
            await self.handle_text_message(text_data_json)
        elif message_type == 'audio':
            await self.handle_audio_message(text_data_json)

    async def handle_text_message(self, data):
        message = data.get('message', '')
        usuario = data.get('usuario', 'Anónimo')

        await self.channel_layer.group_send(
            self.GROUP_NAME,
            {
                'type': 'chat.message',
                'message': message,
                'usuario': usuario,
                'audio_url': '',  # No se envía URL de audio para mensajes de texto
            }
        )

    async def handle_audio_message(self, data):
        usuario = data.get('usuario', 'Anónimo')
        audio_data = data.get('audio_data', '')

        await self.channel_layer.group_send(
            self.GROUP_NAME,
            {
                'type': 'chat.message',
                'message': '',  # No hay mensaje de texto para mensajes de audio
                'usuario': usuario,
                'audio_data': audio_data,
            }
        )

    async def chat_message(self, event):
        message = event.get('message', '')
        usuario = event.get('usuario', 'Anónimo')
        audio_url = event.get('audio_url', '')
        audio_data = event.get('audio_data', '')

        await self.send(text_data=json.dumps({
            'message': message,
            'usuario': usuario,
            'audio_url': audio_url,
            'audio_data': audio_data,
        }))
