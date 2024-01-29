from django.contrib.auth.models import User
from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.consumers import WebRTCConsumer
from .forms import RegistroForm
from .models import Mensaje
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import tempfile
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid

#vista de listar archivos multimedia
def list_msj(request):
    mensajes = Mensaje.objects.all()
    return render(request, 'list_msj.html', {'mensajes': mensajes})

#vista de mensaje
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



def grabar_audio():
    duracion_grabacion = 5  # segundos (ajusta según tus necesidades)
    frecuencia_muestreo = 44100  # Hz (ajusta según tus necesidades)

    print("Grabando audio...")
    # Grabar audio desde el micrófono
    audio_grabado = sd.rec(int(duracion_grabacion * frecuencia_muestreo),
                           samplerate=frecuencia_muestreo, channels=1, dtype=np.int16)
    sd.wait()
    print("Grabación completada.")

    # Guardar el audio grabado en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=settings.MEDIA_ROOT) as temp_file:
        archivo_temporal = temp_file.name
        write(archivo_temporal, frecuencia_muestreo, audio_grabado)

    return archivo_temporal

# Vista 'crear_audio' con la lógica de grabación de audio
def crear_audio(request):
    archivo_temporal = grabar_audio()

    # Puedes realizar alguna lógica adicional aquí, como guardar el archivo en tu modelo Mensaje o en otra ubicación deseada.
    print("Audio grabado:", archivo_temporal)

    return JsonResponse({'status': 'success', 'audio_path': archivo_temporal})

# Vista 'audio' que llama a la lógica de grabación de audio
def audio(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST, request.FILES)
        if formulario.is_valid():
            print("Formulario válido") 
            usuario, creado = User.objects.get_or_create(username=formulario.cleaned_data['usuario'])
            archivo_audio = formulario.cleaned_data['archivo_audio']

            if archivo_audio:
                # Si se proporciona un archivo de audio, usarlo directamente
                mensaje = Mensaje.objects.create(
                    usuario=usuario,
                    archivo_audio=archivo_audio
                )
            else:
                # Si no se proporciona un archivo de audio, grabar audio en tiempo real
                archivo_temporal = grabar_audio()
                mensaje = Mensaje.objects.create(
                    usuario=usuario,
                    archivo_audio=SimpleUploadedFile(name='audio.wav', content=open(archivo_temporal, 'rb').read())
                )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                WebRTCConsumer.GROUP_NAME,
                {
                    'type': 'chat.message',
                    'message': 'Mensaje de audio',
                    'audio_url': mensaje.archivo_audio.url if mensaje.archivo_audio else None,
                }
            )

            mensajes = Mensaje.objects.all()
            return render(request, 'list_msj.html', {'mensajes': mensajes})

    else:
        formulario = RegistroForm()

    return render(request, 'audio.html', {'formulario': formulario})

