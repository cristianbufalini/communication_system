from django.urls import path
from . import views
from .consumers import WebRTCConsumer

urlpatterns = [
    path('', views.list_msj, name='list_msj'),
    path('chat/', views.chat, name='chat'),
    # Puedes agregar más rutas aquí según tus necesidades
]

websocket_urlpatterns = [
    path('ws/webrtc/', WebRTCConsumer.as_asgi()),  # Ruta para el consumidor de WebRTC
    # Puedes agregar más rutas WebSocket aquí si es necesario
]
