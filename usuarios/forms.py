from django import forms
from usuarios.models import Usuario

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # qual modelo estamos usando
        fields = ['nome', 'cpf', 'idade', 'sexo']
        # todos os campos que queremos que pegue

        