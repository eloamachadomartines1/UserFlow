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






# 1. Atualizar o models.py
# python
# from django.db import models
# from django.core.validators import RegexValidator

# class Usuario(models.Model):
    # SEXO_CHOICES = [
        # ('M', 'Masculino'),
        # ('F', 'Feminino'),
        # ('O', 'Outro'),
    # ]

    # cpf_validator = RegexValidator(
        # regex=r'^\d{11}$',
        # message='CPF deve conter exatamente 11 números, sem pontos ou traços.'
    # )

    # nome = models.CharField(max_length=100)
    # cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    # idade = models.IntegerField(blank=True, null=True)
    # sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    # foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    # def __str__(self):
        # return self.nome

# upload_to='usuarios/' significa que as fotos vão ser salvas em media/usuarios/.

# 2. Instalar o Pillow (obrigatório para ImageField)
# bash
# pip install Pillow

# Sem essa biblioteca, o Django nem deixa rodar makemigrations num model com ImageField.

# 3. Configurar MEDIA_URL e MEDIA_ROOT no settings.py do projeto

# Adicione (se ainda não tiver):

# python
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# 4. Servir os arquivos de mídia no urls.py do projeto
# python
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
    # ... suas rotas existentes
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 5. Atualizar o forms.py
# python
# from django import forms
# from .models import Usuario

# class UsuarioForm(forms.ModelForm):
    # class Meta:
        # model = Usuario
        # fields = ['nome', 'cpf', 'idade', 'sexo', 'foto']

    # def clean_cpf(self):
        # cpf = self.cleaned_data.get('cpf')
        # if not cpf.isdigit():
            # raise forms.ValidationError('O CPF deve conter apenas números.')
        # if len(cpf) != 11:
            # raise forms.ValidationError('O CPF deve ter exatamente 11 números.')
        # return cpf
# 6. Atualizar o usuarios/views.py
# 
# Precisa capturar request.FILES, além de request.POST, nas views de criar e editar:

# python
# def criar_usuario(request):
    # if request.method == 'POST':
        # form = UsuarioForm(request.POST, request.FILES)
        # if form.is_valid():
            # form.save()
            # return redirect('listar_usuarios')
    # else:
        # form = UsuarioForm()
    # return render(request, 'usuarios/form.html', {'form': form})

# def editar_usuario(request, pk):
    # usuario = get_object_or_404(Usuario, pk=pk)
    # if request.method == 'POST':
        # form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        # if form.is_valid():
            # form.save()
            # return redirect('listar_usuarios')
    # else:
        # form = UsuarioForm(instance=usuario)
    # return render(request, 'usuarios/form.html', {'form': form})
# 7. Atualizar o form.html — adicionar enctype

# Sem isso, o navegador não envia arquivos, só texto:

# html
# <form method="post" enctype="multipart/form-data">
# 8. Atualizar o admin.py
# python
# from django.contrib import admin
# from .models import Usuario

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
    # list_display = ['nome', 'cpf', 'idade', 'sexo']

# (Não coloquei foto no list_display porque o admin mostraria só o caminho do arquivo como texto — se quiser, dá pra mostrar como miniatura, mas exige um pouco mais de código. Quer que eu monte isso?)

# 9. Gerar e aplicar a migration
# bash
# python manage.py makemigrations
# python manage.py migrate
# 10. Mostrar a foto na listagem (opcional)

# Se quiser exibir no listar.html:

# html
# <td>
    # {% if usuario.foto %}
        # <img src="{{ usuario.foto.url }}" width="50">
    # {% else %}
        # -
    # {% endif %}
# </td>

# Depois de aplicar tudo isso, rode python manage.py runserver e teste criar um usuário com foto. Quer que eu já adicione a miniatura no admin também?

# como assim

# Desculpa, deixei muita coisa de uma vez! Qual parte especificamente ficou confusa? Pode ser:

# O processo todo — muitos passos juntos e você quer que eu explique devagar, um de cada vez
# Um passo específico — tipo o que é enctype="multipart/form-data", ou por que precisa do Pillow, ou o que é request.FILES
# Onde colocar cada coisa — tipo não saber exatamente qual arquivo abrir pra colar cada trecho

# Me fala o que travou que eu explico com mais calma.

# "Quer que eu já adicione a miniatura no admin também?"

# Ah, isso! Deixa eu explicar melhor.

# O problema

# No Django Admin (/admin/), se você adicionar foto no list_display, ele não mostra a imagem — mostra só o texto do caminho do arquivo, tipo:

# usuarios/foto123.jpg

# Não dá pra ver a foto de verdade na lista, só o nome do arquivo. Meio inútil visualmente.

# O que eu quis dizer com "miniatura"

# É fazer o admin mostrar uma imagem pequena de verdade (um preview/thumbnail) na coluna, em vez do texto do caminho. Assim, na lista de usuários dentro do /admin/, você vê a carinha da pessoa direto, sem precisar clicar pra abrir o registro.

# Como fica (comparação)

# Sem miniatura (só list_display = ['nome', 'cpf', 'foto']):

# Nome       | CPF         | Foto
# Eloá       | 12345678901 | usuarios/foto123.jpg

# Com miniatura:

# Nome       | CPF         | Foto
# Eloá       | 12345678901 | [🖼️ imagem pequena aqui]
# O código pra fazer isso

# Se você quiser, no usuarios/admin.py:

# python
# from django.contrib import admin
# from django.utils.html import format_html
# from .models import Usuario

# @admin.register(Usuario)
# class UsuarioAdmin(admin.ModelAdmin):
    # list_display = ['nome', 'cpf', 'idade', 'sexo', 'mostrar_foto']
# 
    # def mostrar_foto(self, obj):
        # if obj.foto:
            # return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.foto.url)
        # return "Sem foto"
    # mostrar_foto.short_description = 'Foto'

# Isso cria um "campo virtual" (mostrar_foto) que não existe no banco, só serve pra exibição — ele pega a URL da foto e monta uma tag <img> pequena.
