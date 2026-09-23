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




    # Building a login-protected content management system.
# Building a login-protected content management system.
# Boa, vamos implementar isso usando o sistema de autenticação nativo do Django (é o mais simples e seguro pra isso).

# 1. usuarios/urls.py  adicionar rotas de login/logout
# python
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
    # path('', views.listar_usuarios, name='listar_usuarios'),
    # path('novo/', views.criar_usuario, name='criar_usuario'),
    # path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    # path('excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),

    # path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='listar_usuarios'), name='logout'),
# ]
# Usei as views prontas do Django (LoginView/LogoutView) — elas já cuidam de toda a lógica de autenticação, validação de senha, sessão, etc. Você só precisa do template de login.

# 2. usuarios/templates/usuarios/login.html
# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
    # <meta charset="UTF-8">
    # <title>Login</title>
    # <style>
        # body { font-family: Arial, sans-serif; margin: 40px; }
        # .form-group { margin-bottom: 15px; }
        # label { display: block; margin-bottom: 5px; font-weight: bold; }
        # input { padding: 6px; width: 250px; }
        # button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
        # .erro { color: red; }
    # </style>
# </head>
# <body>
    # <h1>Login</h1>

    # {% if form.errors %}
        # <p class="erro">Usuário ou senha inválidos.</p>
    # {% endif %}

    # <form method="post">
        # {% csrf_token %}
        # <div class="form-group">
            # <label for="{{ form.username.id_for_label }}">Usuário</label>
            # {{ form.username }}
        # </div>
        # <div class="form-group">
            # <label for="{{ form.password.id_for_label }}">Senha</label>
            # {{ form.password }}
        # </div>
        # <button type="submit">Entrar</button>
    # </form>

    # <p><a href="{% url 'listar_usuarios' %}">&larr; Voltar para a lista</a></p>
# </body>
# </html>

# 3. usuarios/views.py — proteger criar, editar e excluir com @login_required
# python
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Usuario
# from .forms import UsuarioForm

# def listar_usuarios(request):
    # usuarios = Usuario.objects.all()
    # return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

# @login_required
# def criar_usuario(request):
    # if request.method == 'POST':
        # form = UsuarioForm(request.POST, request.FILES)
        # if form.is_valid():
            # form.save()
            # return redirect('listar_usuarios')
    # else:
        # form = UsuarioForm()
    # return render(request, 'usuarios/form.html', {'form': form})

# @login_required
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

# @login_required
# def excluir_usuario(request, pk):
    # usuario = get_object_or_404(Usuario, pk=pk)
    # if request.method == 'POST':
        # usuario.delete()
        # return redirect('listar_usuarios')
    # return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario})
# @login_required faz o Django checar se o usuário está logado antes de executar a view. Se não estiver, redireciona automaticamente pra tela de login.

# 4. Configurar pro Django saber qual é a tela de login (settings.py)
# Adicione no final do arquivo de settings do projeto:

# python
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'listar_usuarios'
# LOGIN_URL é pra onde o @login_required redireciona quando alguém não logado tenta acessar uma rota protegida.

# 5. listar.html — esconder os botões de Editar/Excluir/Novo pra quem não está logado
# html
# <h1>Usuários cadastrados</h1>

# {% if user.is_authenticated %}
    # <p>Olá, {{ user.username }}! <a href="{% url 'logout' %}">Sair</a></p>
    # <p><a href="{% url 'criar_usuario' %}" class="btn novo">+ Novo usuário</a></p>
# {% else %}
    # <p><a href="{% url 'login' %}">Fazer login</a> para editar ou excluir usuários</p>
# {% endif %}

# <table>
    # <thead>
        # <tr>
            # <th>Foto</th>
            # <th>Nome</th>
            # <th>CPF</th>
            # <th>Idade</th>
            # <th>Sexo</th>
            # {% if user.is_authenticated %}
                # <th>Ações</th>
            # {% endif %}
        # </tr>
    # </thead>
    # <tbody>
        # {% for usuario in usuarios %}
        # <tr>
            # <td>
                # {% if usuario.foto %}
                    # <img src="{{ usuario.foto.url }}" class="avatar">
                # {% else %}
                    # <div class="avatar avatar-vazio">?</div>
                # {% endif %}
            # </td>
            # <td>{{ usuario.nome }}</td>
            # <td>{{ usuario.cpf }}</td>
            # <td>{{ usuario.idade|default:"-" }}</td>
            # <td>{{ usuario.get_sexo_display }}</td>
            # {% if user.is_authenticated %}
            # <td>
                # <a href="{% url 'editar_usuario' usuario.pk %}" class="btn editar">Editar</a>
                # <a href="{% url 'excluir_usuario' usuario.pk %}" class="btn excluir">Excluir</a>
            # </td>
            # {% endif %}
        # </tr>
        # {% empty %}
        # <tr>
            # <td colspan="6">Nenhum usuário cadastrado.</td>
        # </tr>
        # {% endfor %}
    # </tbody>
# </table>
# {% if user.is_authenticated %} funciona automaticamente em qualquer template Django — a variável user já vem disponível em todo request, contanto que django.contrib.auth.middleware.AuthenticationMiddleware esteja no MIDDLEWARE do settings (ele vem por padrão em todo projeto novo).

# 6. Criar um usuário para testar o login
# Se ainda não tiver um superusuário:

# bash
# python manage.py createsuperuser
# Use esse login e senha na tela /usuarios/login/.

# Resumo do comportamento final
# Situação	Ver lista	Editar/Excluir	Criar novo
# Não logado	✅ Sim	❌ Bloqueado (redireciona pro login)	❌ Bloqueado
# Logado	✅ Sim	✅ Sim	✅ Sim