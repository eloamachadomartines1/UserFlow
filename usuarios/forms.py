import re
from django import forms
from usuarios.models import Usuario

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # qual modelo estamos usando
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'foto']
        # todos os campos que queremos que pegue
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'cpf': forms.TextInput(attrs={
                'maxlength': 14,
                'placeholder': '000.000.000-00',
                'inputmode': 'numeric',
            }),
        }
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cpf = re.sub(r'\D', '', cpf) #remove tudo que nao for numero(ponto, traço)
        if len(cpf) != 11:
            raise forms.ValidationError('O CPF deve ter exatamente 11 números.')

        return cpf