# chat/models.py

from django.db import models
from django.contrib.auth.models import User

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.TextField(blank=True)
    archivo_audio = models.FileField(upload_to='archivos_audio/', blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje {self.pk} - {self.contenido[:50]}'
