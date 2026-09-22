from django import forms
from usuarios.models import Usuario

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # qual modelo estamos usando
        fields = ['nome', 'cpf', 'idade', 'sexo']
        # todos os campos que queremos que pegue

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf.isdigit():
            raise forms.ValidationError('O CPF deve ter exatamente 11 números.')
        return cpf