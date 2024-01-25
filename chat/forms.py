from django import forms

class RegistroForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario', max_length=150)
    contenido = forms.CharField(label='Contenido del mensaje', widget=forms.Textarea)

    # Puedes agregar más campos según tus necesidades

    def clean_usuario(self):
        # Realiza validaciones adicionales si es necesario
        usuario = self.cleaned_data['usuario']
        return usuario
