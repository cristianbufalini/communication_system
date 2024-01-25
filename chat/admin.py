# chat/admin.py
from django.contrib import admin
from .models import Mensaje

class MensajeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'contenido', 'fecha_envio']
    search_fields = ['usuario__username', 'contenido']

    def save_model(self, request, obj, form, change):
        # Asigna el usuario actual al mensaje antes de guardarlo
        if not change:  # Solo al crear nuevos mensajes
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Mensaje, MensajeAdmin)
