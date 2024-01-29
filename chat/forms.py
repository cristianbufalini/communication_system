from django import forms

class RegistroForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', max_length=150)
    contenido = forms.CharField(required=False, label='Contenido del mensaje', widget=forms.Textarea)
    archivo_audio = forms.FileField(required=False)
    audio_path = forms.CharField(widget=forms.HiddenInput(), required=False)  # Nuevo campo para la ruta del audio grabado


    # Puedes agregar más campos según tus necesidades

    def clean_usuario(self):
        # Realiza validaciones adicionales si es necesario
        usuario = self.cleaned_data['usuario']
        return usuario
