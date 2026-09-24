import os
import sys

def main():
    
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



# Ah entendi, minha confusão  obrigado por corrigir! Então nesse projeto novo (o CRUD de usuários) não existe nada de login/cadastro ainda. Vamos criar isso do zero, certinho.

# O que vamos usar

# Não precisa criar um app novo só pra isso — dá pra colocar as views de cadastro/login/logout dentro do próprio app usuarios, usando o sistema de autenticação nativo do Django (User, UserCreationForm, LoginView, LogoutView).

# 1. usuarios/views.py — adicionar a view de cadastro
# python
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from .models import Usuario
# from .forms import UsuarioForm

# def cadastro_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'usuarios/cadastro.html', {'form': form})


# def listar_usuarios(request):
#     usuarios = Usuario.objects.all()
#     return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

# @login_required
# def criar_usuario(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm()
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def editar_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm(instance=usuario)
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def excluir_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         usuario.delete()
#         return redirect('listar_usuarios')
#     return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario})
# 2. usuarios/urls.py — adicionar cadastro, login e logout
# python
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', views.listar_usuarios, name='listar_usuarios'),
#     path('novo/', views.criar_usuario, name='criar_usuario'),
#     path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
#     path('excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),

#     path('cadastro/', views.cadastro_view, name='cadastro'),
#     path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='listar_usuarios'), name='logout'),
# ]

# next_page='listar_usuarios' já resolve aquilo que você pediu: ao fazer logout, volta pra lista de usuários — que é exatamente a tela com os botões de "Cadastrar" e "Login" reaparecendo (porque a pessoa não está mais autenticada).

# 3. usuarios/templates/usuarios/cadastro.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; font-size: 0.9em; }
# </style>

# <h1>Cadastre-se</h1>

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#         {% if form.username.errors %}<div class="erro">{{ form.username.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password1.id_for_label }}">Senha</label>
#         {{ form.password1 }}
#         {% if form.password1.errors %}<div class="erro">{{ form.password1.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password2.id_for_label }}">Confirmar senha</label>
#         {{ form.password2 }}
#         {% if form.password2.errors %}<div class="erro">{{ form.password2.errors }}</div>{% endif %}
#     </div>
#     <button type="submit">Cadastrar</button>
# </form>
# {% endblock %}
# 4. usuarios/templates/usuarios/login.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; }
# </style>

# <h1>Login</h1>

# {% if form.errors %}
#     <p class="erro">Usuário ou senha inválidos.</p>
# {% endif %}

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password.id_for_label }}">Senha</label>
#         {{ form.password }}
#     </div>
#     <button type="submit">Entrar</button>
# </form>
# {% endblock %}
# 5. settings.py — apontar login e redirecionamento
# python
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'listar_usuarios'
# 6. base.html — header com cadastro/login/logout

# Se seu projeto ainda não tem um base.html, aqui vai um completo, no mesmo estilo do exemplo que você mostrou (navbar azul):

# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
#     <meta charset="UTF-8">
#     <title>{% block title %}Usuários{% endblock %}</title>
#     <style>
#         body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f7f7f7; }
#         nav { background-color: #0096c7; height: 50px; display: flex; align-items: center; }
#         nav ul { list-style: none; display: flex; margin: 0; padding: 0 20px; }
#         nav ul li { margin-right: 20px; }
#         nav ul li a { color: #fff; text-decoration: none; }
#         nav ul li a:hover { text-decoration: underline; }
#         main { padding: 20px; max-width: 1000px; margin: 0 auto; }
#     </style>
# </head>
# <body>
#     <nav>
#         <ul>
#             {% if not user.is_authenticated %}
#                 <li><a href="{% url 'cadastro' %}">Cadastre-se</a></li>
#                 <li><a href="{% url 'login' %}">Login</a></li>
#             {% endif %}
#             <li><a href="{% url 'listar_usuarios' %}">Usuários</a></li>
#             {% if user.is_authenticated %}
#                 <li><a href="{% url 'logout' %}">Sair</a></li>
#             {% endif %}
#         </ul>
#     </nav>
#     <main>
#         {% block content %}
#         {% endblock %}
#     </main>
# </body>
# </html>

# Esse base.html fica direto em usuarios/templates/base.html (fora da subpasta usuarios/, senão o {% extends "base.html" %} não acha ele — o Django procura templates soltos na raiz de templates/ de qualquer app instalado).

# Resultado
# Situação	Vê lista	Cadastra/Login visível	Editar/Excluir
# Deslogado	✅	✅ (Cadastre-se / Login)	❌
# Logado	✅	❌ (some, aparece "Sair")	✅

# Depois disso, rode python manage.py migrate (se ainda não rodou) e teste o fluxo completo: cadastrar → fazer login → editar/excluir → logout.

# E se por um acaso eu quiser sair no botão de logout e nao retornar apenas uma tela branca? É porq o next_page não está funcionando?

# Diagnosing why logout redirect isn't working.

# Boa pergunta — e sim, é bem provável que seja exatamente isso!

# O motivo real

# Em versões mais recentes do Django (seu projeto está na 6.1.1), o LogoutView não aceita mais GET, só POST. Ou seja, um link comum:

# html
# <a href="{% url 'logout' %}">Sair</a>

# Faz uma requisição GET — e o Django recusa (retorna erro 405 "Method Not Allowed", que às vezes aparece como tela em branco dependendo do navegador/config). O next_page nem chega a ser processado, porque o logout não é executado.

# Solução: trocar o link por um formulário com POST

# No base.html, troca:

# html
# {% if user.is_authenticated %}
#     <li><a href="{% url 'logout' %}">Sair</a></li>
# {% endif %}

# Por:

# html
# {% if user.is_authenticated %}
#     <li>
#         <form method="post" action="{% url 'logout' %}" style="display: inline;">
#             {% csrf_token %}
#             <button type="submit" class="logout-btn">Sair</button>
#         </form>
#     </li>
# {% endif %}
# CSS pra deixar o botão parecido com um link (opcional)

# Já que ele vira um <button> em vez de <a>, o visual muda um pouco. Pra deixar igual aos outros itens do menu:

# css
# .logout-btn {
#     background: none;
#     border: none;
#     color: #fff;
#     cursor: pointer;
#     font-size: inherit;
#     font-family: inherit;
#     padding: 0;
#     text-decoration: none;
# }
# .logout-btn:hover {
#     text-decoration: underline;
# }
# Por que isso muda?

# Faz sentido do ponto de vista de segurança: logout é uma ação que modifica estado (encerra a sessão), então o Django força que seja feito via POST (com proteção CSRF), assim como criar/editar/excluir. GET é reservado só pra "visualizar" coisas, não pra executar ações.

# Depois dessa troca, o next_page='listar_usuarios' volta a funcionar normalmente, porque agora o logout realmente é processado.Ah entendi, minha confusão — obrigado por corrigir! Então nesse projeto novo (o CRUD de usuários) não existe nada de login/cadastro ainda. Vamos criar isso do zero, certinho.

# O que vamos usar

# Não precisa criar um app novo só pra isso — dá pra colocar as views de cadastro/login/logout dentro do próprio app usuarios, usando o sistema de autenticação nativo do Django (User, UserCreationForm, LoginView, LogoutView).

# 1. usuarios/views.py — adicionar a view de cadastro
# python
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from .models import Usuario
# from .forms import UsuarioForm

# def cadastro_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'usuarios/cadastro.html', {'form': form})


# def listar_usuarios(request):
#     usuarios = Usuario.objects.all()
#     return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

# @login_required
# def criar_usuario(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm()
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def editar_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm(instance=usuario)
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def excluir_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         usuario.delete()
#         return redirect('listar_usuarios')
#     return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario})
# 2. usuarios/urls.py — adicionar cadastro, login e logout
# python
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', views.listar_usuarios, name='listar_usuarios'),
#     path('novo/', views.criar_usuario, name='criar_usuario'),
#     path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
#     path('excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),

#     path('cadastro/', views.cadastro_view, name='cadastro'),
#     path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='listar_usuarios'), name='logout'),
# ]

# next_page='listar_usuarios' já resolve aquilo que você pediu: ao fazer logout, volta pra lista de usuários — que é exatamente a tela com os botões de "Cadastrar" e "Login" reaparecendo (porque a pessoa não está mais autenticada).

# 3. usuarios/templates/usuarios/cadastro.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; font-size: 0.9em; }
# </style>

# <h1>Cadastre-se</h1>

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#         {% if form.username.errors %}<div class="erro">{{ form.username.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password1.id_for_label }}">Senha</label>
#         {{ form.password1 }}
#         {% if form.password1.errors %}<div class="erro">{{ form.password1.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password2.id_for_label }}">Confirmar senha</label>
#         {{ form.password2 }}
#         {% if form.password2.errors %}<div class="erro">{{ form.password2.errors }}</div>{% endif %}
#     </div>
#     <button type="submit">Cadastrar</button>
# </form>
# {% endblock %}
# 4. usuarios/templates/usuarios/login.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; }
# </style>

# <h1>Login</h1>

# {% if form.errors %}
#     <p class="erro">Usuário ou senha inválidos.</p>
# {% endif %}

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password.id_for_label }}">Senha</label>
#         {{ form.password }}
#     </div>
#     <button type="submit">Entrar</button>
# </form>
# {% endblock %}
# 5. settings.py — apontar login e redirecionamento
# python
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'listar_usuarios'
# 6. base.html — header com cadastro/login/logout

# Se seu projeto ainda não tem um base.html, aqui vai um completo, no mesmo estilo do exemplo que você mostrou (navbar azul):

# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
#     <meta charset="UTF-8">
#     <title>{% block title %}Usuários{% endblock %}</title>
#     <style>
#         body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f7f7f7; }
#         nav { background-color: #0096c7; height: 50px; display: flex; align-items: center; }
#         nav ul { list-style: none; display: flex; margin: 0; padding: 0 20px; }
#         nav ul li { margin-right: 20px; }
#         nav ul li a { color: #fff; text-decoration: none; }
#         nav ul li a:hover { text-decoration: underline; }
#         main { padding: 20px; max-width: 1000px; margin: 0 auto; }
#     </style>
# </head>
# <body>
#     <nav>
#         <ul>
#             {% if not user.is_authenticated %}
#                 <li><a href="{% url 'cadastro' %}">Cadastre-se</a></li>
#                 <li><a href="{% url 'login' %}">Login</a></li>
#             {% endif %}
#             <li><a href="{% url 'listar_usuarios' %}">Usuários</a></li>
#             {% if user.is_authenticated %}
#                 <li><a href="{% url 'logout' %}">Sair</a></li>
#             {% endif %}
#         </ul>
#     </nav>
#     <main>
#         {% block content %}
#         {% endblock %}
#     </main>
# </body>
# </html>

# Esse base.html fica direto em usuarios/templates/base.html (fora da subpasta usuarios/, senão o {% extends "base.html" %} não acha ele — o Django procura templates soltos na raiz de templates/ de qualquer app instalado).

# Resultado
# Situação	Vê lista	Cadastra/Login visível	Editar/Excluir
# Deslogado	✅	✅ (Cadastre-se / Login)	❌
# Logado	✅	❌ (some, aparece "Sair")	✅

# Depois disso, rode python manage.py migrate (se ainda não rodou) e teste o fluxo completo: cadastrar → fazer login → editar/excluir → logout.

# E se por um acaso eu quiser sair no botão de logout e nao retornar apenas uma tela branca? É porq o next_page não está funcionando?

# Diagnosing why logout redirect isn't working.

# Boa pergunta — e sim, é bem provável que seja exatamente isso!

# O motivo real

# Em versões mais recentes do Django (seu projeto está na 6.1.1), o LogoutView não aceita mais GET, só POST. Ou seja, um link comum:

# html
# <a href="{% url 'logout' %}">Sair</a>

# Faz uma requisição GET — e o Django recusa (retorna erro 405 "Method Not Allowed", que às vezes aparece como tela em branco dependendo do navegador/config). O next_page nem chega a ser processado, porque o logout não é executado.

# Solução: trocar o link por um formulário com POST

# No base.html, troca:

# html
# {% if user.is_authenticated %}
#     <li><a href="{% url 'logout' %}">Sair</a></li>
# {% endif %}

# Por:

# html
# {% if user.is_authenticated %}
#     <li>
#         <form method="post" action="{% url 'logout' %}" style="display: inline;">
#             {% csrf_token %}
#             <button type="submit" class="logout-btn">Sair</button>
#         </form>
#     </li>
# {% endif %}
# CSS pra deixar o botão parecido com um link (opcional)

# Já que ele vira um <button> em vez de <a>, o visual muda um pouco. Pra deixar igual aos outros itens do menu:

# css
# .logout-btn {
#     background: none;
#     border: none;
#     color: #fff;
#     cursor: pointer;
#     font-size: inherit;
#     font-family: inherit;
#     padding: 0;
#     text-decoration: none;
# }
# .logout-btn:hover {
#     text-decoration: underline;
# }
# Por que isso muda?

# Faz sentido do ponto de vista de segurança: logout é uma ação que modifica estado (encerra a sessão), então o Django força que seja feito via POST (com proteção CSRF), assim como criar/editar/excluir. GET é reservado só pra "visualizar" coisas, não pra executar ações.

# Depois dessa troca, o next_page='listar_usuarios' volta a funcionar normalmente, porque agora o logout realmente é processado.Ah entendi, minha confusão — obrigado por corrigir! Então nesse projeto novo (o CRUD de usuários) não existe nada de login/cadastro ainda. Vamos criar isso do zero, certinho.

# O que vamos usar

# Não precisa criar um app novo só pra isso — dá pra colocar as views de cadastro/login/logout dentro do próprio app usuarios, usando o sistema de autenticação nativo do Django (User, UserCreationForm, LoginView, LogoutView).

# 1. usuarios/views.py — adicionar a view de cadastro
# python
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from .models import Usuario
# from .forms import UsuarioForm

# def cadastro_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'usuarios/cadastro.html', {'form': form})


# def listar_usuarios(request):
#     usuarios = Usuario.objects.all()
#     return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

# @login_required
# def criar_usuario(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm()
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def editar_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             form.save()
#             return redirect('listar_usuarios')
#     else:
#         form = UsuarioForm(instance=usuario)
#     return render(request, 'usuarios/form.html', {'form': form})

# @login_required
# def excluir_usuario(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     if request.method == 'POST':
#         usuario.delete()
#         return redirect('listar_usuarios')
#     return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario})
# 2. usuarios/urls.py — adicionar cadastro, login e logout
# python
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', views.listar_usuarios, name='listar_usuarios'),
#     path('novo/', views.criar_usuario, name='criar_usuario'),
#     path('editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
#     path('excluir/<int:pk>/', views.excluir_usuario, name='excluir_usuario'),

#     path('cadastro/', views.cadastro_view, name='cadastro'),
#     path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='listar_usuarios'), name='logout'),
# ]

# next_page='listar_usuarios' já resolve aquilo que você pediu: ao fazer logout, volta pra lista de usuários — que é exatamente a tela com os botões de "Cadastrar" e "Login" reaparecendo (porque a pessoa não está mais autenticada).

# 3. usuarios/templates/usuarios/cadastro.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; font-size: 0.9em; }
# </style>

# <h1>Cadastre-se</h1>

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#         {% if form.username.errors %}<div class="erro">{{ form.username.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password1.id_for_label }}">Senha</label>
#         {{ form.password1 }}
#         {% if form.password1.errors %}<div class="erro">{{ form.password1.errors }}</div>{% endif %}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password2.id_for_label }}">Confirmar senha</label>
#         {{ form.password2 }}
#         {% if form.password2.errors %}<div class="erro">{{ form.password2.errors }}</div>{% endif %}
#     </div>
#     <button type="submit">Cadastrar</button>
# </form>
# {% endblock %}
# 4. usuarios/templates/usuarios/login.html
# html
# {% extends "base.html" %}

# {% block content %}
# <style>
#     .form-group { margin-bottom: 15px; }
#     label { display: block; margin-bottom: 5px; font-weight: bold; }
#     input { padding: 6px; width: 250px; }
#     button { padding: 8px 16px; background-color: #0096c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
#     .erro { color: red; }
# </style>

# <h1>Login</h1>

# {% if form.errors %}
#     <p class="erro">Usuário ou senha inválidos.</p>
# {% endif %}

# <form method="post">
#     {% csrf_token %}
#     <div class="form-group">
#         <label for="{{ form.username.id_for_label }}">Usuário</label>
#         {{ form.username }}
#     </div>
#     <div class="form-group">
#         <label for="{{ form.password.id_for_label }}">Senha</label>
#         {{ form.password }}
#     </div>
#     <button type="submit">Entrar</button>
# </form>
# {% endblock %}
# 5. settings.py — apontar login e redirecionamento
# python
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'listar_usuarios'
# 6. base.html — header com cadastro/login/logout

# Se seu projeto ainda não tem um base.html, aqui vai um completo, no mesmo estilo do exemplo que você mostrou (navbar azul):

# html
# <!DOCTYPE html>
# <html lang="pt-br">
# <head>
#     <meta charset="UTF-8">
#     <title>{% block title %}Usuários{% endblock %}</title>
#     <style>
#         body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f7f7f7; }
#         nav { background-color: #0096c7; height: 50px; display: flex; align-items: center; }
#         nav ul { list-style: none; display: flex; margin: 0; padding: 0 20px; }
#         nav ul li { margin-right: 20px; }
#         nav ul li a { color: #fff; text-decoration: none; }
#         nav ul li a:hover { text-decoration: underline; }
#         main { padding: 20px; max-width: 1000px; margin: 0 auto; }
#     </style>
# </head>
# <body>
#     <nav>
#         <ul>
#             {% if not user.is_authenticated %}
#                 <li><a href="{% url 'cadastro' %}">Cadastre-se</a></li>
#                 <li><a href="{% url 'login' %}">Login</a></li>
#             {% endif %}
#             <li><a href="{% url 'listar_usuarios' %}">Usuários</a></li>
#             {% if user.is_authenticated %}
#                 <li><a href="{% url 'logout' %}">Sair</a></li>
#             {% endif %}
#         </ul>
#     </nav>
#     <main>
#         {% block content %}
#         {% endblock %}
#     </main>
# </body>
# </html>

# Esse base.html fica direto em usuarios/templates/base.html (fora da subpasta usuarios/, senão o {% extends "base.html" %} não acha ele — o Django procura templates soltos na raiz de templates/ de qualquer app instalado).

# Resultado
# Situação	Vê lista	Cadastra/Login visível	Editar/Excluir
# Deslogado	✅	✅ (Cadastre-se / Login)	❌
# Logado	✅	❌ (some, aparece "Sair")	✅

# Depois disso, rode python manage.py migrate (se ainda não rodou) e teste o fluxo completo: cadastrar → fazer login → editar/excluir → logout.

# E se por um acaso eu quiser sair no botão de logout e nao retornar apenas uma tela branca? É porq o next_page não está funcionando?

# Diagnosing why logout redirect isn't working.

# Boa pergunta — e sim, é bem provável que seja exatamente isso!

# O motivo real

# Em versões mais recentes do Django (seu projeto está na 6.1.1), o LogoutView não aceita mais GET, só POST. Ou seja, um link comum:

# html
# <a href="{% url 'logout' %}">Sair</a>

# Faz uma requisição GET — e o Django recusa (retorna erro 405 "Method Not Allowed", que às vezes aparece como tela em branco dependendo do navegador/config). O next_page nem chega a ser processado, porque o logout não é executado.

# Solução: trocar o link por um formulário com POST

# No base.html, troca:

# html
# {% if user.is_authenticated %}
#     <li><a href="{% url 'logout' %}">Sair</a></li>
# {% endif %}

# Por:

# html
# {% if user.is_authenticated %}
#     <li>
#         <form method="post" action="{% url 'logout' %}" style="display: inline;">
#             {% csrf_token %}
#             <button type="submit" class="logout-btn">Sair</button>
#         </form>
#     </li>
# {% endif %}
# CSS pra deixar o botão parecido com um link (opcional)

# Já que ele vira um <button> em vez de <a>, o visual muda um pouco. Pra deixar igual aos outros itens do menu:

# # css
# # .logout-btn {
# #     background: none;
# #     border: none;
# #     color: #fff;
# #     cursor: pointer;
    # font-size: inherit;
    # font-family: inherit;
    # padding: 0;
    # text-decoration: none;
# }
# .logout-btn:hover {
    # text-decoration: underline;
# }
# Por que isso muda?

# Faz sentido do ponto de vista de segurança: logout é uma ação que modifica estado (encerra a sessão), então o Django força que seja feito via POST (com proteção CSRF), assim como criar/editar/excluir. GET é reservado só pra "visualizar" coisas, não pra executar ações.

# Depois dessa troca, o next_page='listar_usuarios' volta a funcionar normalmente, porque agora o logout realmente é processado.