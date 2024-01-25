from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.consumers import WebRTCConsumer
from .forms import RegistroForm
from .models import Mensaje
from django.http import HttpResponse
from .models import Mensaje

def list_msj(request):
    mensajes = Mensaje.objects.all()
    return render(request, 'list_msj.html', {'mensajes': mensajes})


def chat(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            # Crea un nuevo usuario
            usuario, creado = User.objects.get_or_create(username=formulario.cleaned_data['usuario'])

            # Guarda el mensaje en la base de datos
            mensaje = Mensaje.objects.create(
                usuario=usuario,
                contenido=formulario.cleaned_data['contenido']
            )

            # Envía el mensaje a través de WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                WebRTCConsumer.GROUP_NAME,
                {
                    'type': 'chat.message',
                    'message': mensaje.contenido,
                }
            )
            mensajes = Mensaje.objects.all()
            return render(request, 'list_msj.html', {'mensajes': mensajes})
    else:
        formulario = RegistroForm()

    return render(request, 'chat.html', {'formulario': formulario})
