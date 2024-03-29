# import os
from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from chat.consumers import WebRTCConsumer  # Ajusta la importación según tu estructura
# from django.urls import re_path



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'communication_system.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             [
#                 re_path(r'ws/chat/$', WebRTCConsumer.as_asgi()),
#                 # Puedes agregar más rutas aquí para otros consumidores de Channels
#             ]
#         )
#     ),
# })


# chat/asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from chat.consumers import WebRTCConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/webrtc/", WebRTCConsumer.as_asgi()),
                # Añade la siguiente línea para manejar las solicitudes de información del WebSocket
                re_path(r'^ws/info/$', WebRTCConsumer.as_asgi()),
            ]
        )
    ),
})


