from django.urls import path
from . import views
from .consumers import WebRTCConsumer
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.list_msj, name='list_msj'),
    path('chat/', views.chat, name='chat'),
    path('audio/', views.audio, name='audio'),
    path('crear_audio/', views.crear_audio, name='crear_audio'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

websocket_urlpatterns = [
    path('ws/webrtc/', WebRTCConsumer.as_asgi()),  # Ruta para el consumidor de WebRTC
    # Puedes agregar más rutas WebSocket aquí si es necesario
]
