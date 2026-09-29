import re
from django import forms
from usuarios.models import Usuario

class UsuarioModelForm(forms.ModelForm):
    cpf = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'maxlength':14,
            'placeholder': '000.000.000-00',
            'inputmode': 'numeric',
        })
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nascimento', 'sexo', 'foto']
        widgets = {
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'})
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11:
            raise forms.ValidationError("O CPF deve ter exatamente 11 números.")
        
        return cpf
