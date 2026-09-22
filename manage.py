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





# python manage.py startapp usuarios
# 2. Registrar o app no settings.py

# No arquivo de settings do seu projeto, adicione 'usuarios' em INSTALLED_APPS:

# python
# INSTALLED_APPS = [
    # ...
    # 'usuarios',
# ]


# 3. usuarios/models.py
# python
# from django.db import models

# class Usuario(models.Model):
    # SEXO_CHOICES = [
        # ('M', 'Masculino'),
        # ('F', 'Feminino'),
        # ('O', 'Outro'),
    # ]

    # nome = models.CharField(max_length=100)
    # cpf = models.CharField(max_length=11, unique=True)
    # idade = models.IntegerField(blank=True, null=True)
    # sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    # def __str__(self):
        # return self.nome


# 4. usuarios/forms.py
# python
# from django import forms
# from .models import Usuario

# class UsuarioForm(forms.ModelForm):
    # class Meta:
        # model = Usuario
        # fields = ['nome', 'cpf', 'idade', 'sexo']

# 5. usuarios/views.py
# python
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Usuario
# from .forms import UsuarioForm

# def listar_usuarios(request):
    # usuarios = Usuario.objects.all()
    # return render(request, 'usuarios/listar.html', {'usuarios': usuarios})



# def criar_usuario(request):
    # if request.method == 'POST':
        # form = UsuarioForm(request.POST)
        # if form.is_valid():
            # form.save()
            # return redirect('listar_usuarios')
    # else:
        # form = UsuarioForm()
    # return render(request, 'usuarios/form.html', {'form': form})



# def editar_usuario(request, pk):
    # usuario = get_object_or_404(Usuario, pk=pk)
    # if request.method == 'POST':
        # form = UsuarioForm(request.POST, instance=usuario)
        # if form.is_valid():
            # form.save()
            # return redirect('listar_usuarios')
    # else:
        # form = UsuarioForm(instance=usuario)
    # return render(request, 'usuarios/form.html', {'form': form})



# def excluir_usuario(request, pk):
    # usuario = get_object_or_404(Usuario, pk=pk)
    # if request.method == 'POST':
        # usuario.delete()
        # return redirect('listar_usuarios')
    # return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario})


# 6. usuarios/urls.py (criar esse arquivo)
# python
# from django.urls import path
# from . import views

# urlpatterns = [
    # path('', views.listar_usuarios, name='listar_usuarios'),
    # path('novo/', views.criar_usuario, name='criar_usuario'),
    # path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    # path('excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),
# ]


# 7. Incluir no urls.py do projeto

# No arquivo principal de urls do projeto:

# python
# from django.urls import path, include

# urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('usuarios/', include('usuarios.urls')),
# ]

# 8. Templates

# Crie a pasta usuarios/templates/usuarios/ com 3 arquivos: listar.html, form.html e confirmar_exclusao.html.

# Quer que eu monte esses 3 templates agora?

# sim

# Aqui estão os 3 templates. Como é um projeto novo (sem base.html definido ainda), fiz eles autocontidos, com um HTML básico completo — se você já tiver ou criar um base.html depois, é só me avisar que adapto pra usar {% extends %}.

# usuarios/templates/usuarios/listar.html
# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
    # <meta charset="UTF-8">
    # <title>Lista de Usuários</title>
    # <style>
        # body { font-family: Arial, sans-serif; margin: 40px; }
        # table { border-collapse: collapse; width: 100%; }
        # th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
        # th { background-color: #f2f2f2; }
        # a.btn { text-decoration: none; padding: 6px 12px; border-radius: 4px; margin-right: 5px; }
        # a.novo { background-color: #0096c7; color: white; }
        # a.editar { background-color: #ffc107; color: black; }
        # a.excluir { background-color: #dc3545; color: white; }
    # </style>
# </head>
# <body>
    # <h1>Usuários cadastrados</h1>

    # <p><a href="{% url 'criar_usuario' %}" class="btn novo">+ Novo usuário</a></p>

    # <table>
        # <thead>
            # <tr>
                # <th>Nome</th>
                # <th>CPF</th>
                # <th>Idade</th>
                # <th>Sexo</th>
                # <th>Ações</th>
            # </tr>
        # </thead>
        # <tbody>
            # {% for usuario in usuarios %}
            # <tr>
                # <td>{{ usuario.nome }}</td>
                # <td>{{ usuario.cpf }}</td>
                # <td>{{ usuario.idade|default:"-" }}</td>
                # <td>{{ usuario.get_sexo_display }}</td>
                # <td>
                    # <a href="{% url 'editar_usuario' usuario.pk %}" class="btn editar">Editar</a>
                    # <a href="{% url 'excluir_usuario' usuario.pk %}" class="btn excluir">Excluir</a>
                # </td>
            # </tr>
            # {% empty %}
            # <tr>
                # <td colspan="5">Nenhum usuário cadastrado.</td>
            # </tr>
            # {% endfor %}
        # </tbody>
    # </table>
# </body>
# </html>
# usuarios/templates/usuarios/form.html

# Esse é reaproveitado tanto pra criar quanto pra editar (o título muda sozinho dependendo se form.instance.pk existe):

# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
    # <meta charset="UTF-8">
    # <title>{% if form.instance.pk %}Editar{% else %}Novo{% endif %} Usuário</title>
    # <style>
        # body { font-family: Arial, sans-serif; margin: 40px; }
        # .form-group { margin-bottom: 15px; }
        # label { display: block; margin-bottom: 5px; font-weight: bold; }
        # input, select { padding: 6px; width: 250px; }
        # button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
        # .erro { color: red; font-size: 0.9em; }
        # a { text-decoration: none; color: #555; }
    # </style>
# </head>
# <body>
    # <h1>{% if form.instance.pk %}Editar{% else %}Novo{% endif %} Usuário</h1>

    # <form method="post">
        # {% csrf_token %}

        # {% for field in form %}
        # <div class="form-group">
            # <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            # {{ field }}
            # {% if field.errors %}
                # <div class="erro">{{ field.errors }}</div>
            # {% endif %}
        # </div>
        # {% endfor %}

        # <button type="submit">Salvar</button>
    # </form>

    # <p><a href="{% url 'listar_usuarios' %}">&larr; Voltar para a lista</a></p>
# </body>
# </html>
# usuarios/templates/usuarios/confirmar_exclusao.html
# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
    # <meta charset="UTF-8">
    # <title>Confirmar Exclusão</title>
    # <style>
        # body { font-family: Arial, sans-serif; margin: 40px; }
        # button { padding: 8px 16px; background-color: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }
        # a.cancelar { padding: 8px 16px; background-color: #ccc; color: black; border-radius: 4px; text-decoration: none; }
    # </style>
# </head>
# <body>
    # <h1>Confirmar exclusão</h1>

    # <p>Tem certeza que deseja excluir o usuário <strong>{{ usuario.nome }}</strong>?</p>

    # <form method="post">
        # {% csrf_token %}
        # <button type="submit">Sim, excluir</button>
        # <a href="{% url 'listar_usuarios' %}" class="cancelar">Cancelar</a>
    # </form>
# </body>
# </html>

# Depois de criar esses 3 arquivos, rode:

# bash
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver