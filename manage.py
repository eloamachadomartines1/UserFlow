#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()





# Ou seja, só passa se for exatamente 11 números, nem mais, nem menos, sem letras ou símbolos.

# 2. No forms.py — validação customizada (opcional, mas recomendado)

# O validator do model já funciona, mas fazer a validação também no form garante uma mensagem de erro mais clara antes de tentar salvar no banco:

# python
# from django import forms
# from .models import Usuario

# class UsuarioForm(forms.ModelForm):
    # class Meta:
        # model = Usuario
        # fields = ['nome', 'cpf', 'idade', 'sexo']

    # def clean_cpf(self):
        # cpf = self.cleaned_data.get('cpf')
        # if not cpf.isdigit():
            # raise forms.ValidationError('O CPF deve conter apenas números.')
        # if len(cpf) != 11:
            # raise forms.ValidationError('O CPF deve ter exatamente 11 números.')
        # return cpf
# 3. Gerar e aplicar a migration

# Como alteramos o models.py (adicionamos o validators), precisa gerar uma nova migration:

# bash
# python manage.py makemigrations
# python manage.py migrate