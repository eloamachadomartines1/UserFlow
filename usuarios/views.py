import re
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.core.paginator import Paginator

from usuarios.models import Usuario
from usuarios.forms import UsuarioModelForm


def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})


@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.filter(ativo=True).order_by('nome')

    termo = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', 'nome')
    if tipo not in ('nome', 'cpf', 'data'):
        tipo = 'nome'

    if termo:
        if tipo == 'cpf':
            # Aceita com ou sem pontos/traço: só os números importam
            cpf_numeros = re.sub(r'\D', '', termo)
            if cpf_numeros:
                usuarios = usuarios.filter(cpf__icontains=cpf_numeros)
            else:
                usuarios = usuarios.none()

        elif tipo == 'data':
            data_convertida = None
            for formato in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
                try:
                    data_convertida = datetime.strptime(termo, formato).date()
                    break
                except ValueError:
                    continue

            if data_convertida:
                usuarios = usuarios.filter(data_nascimento=data_convertida)
            else:
                usuarios = usuarios.none()

        else:
            usuarios = usuarios.filter(nome__icontains=termo)

    paginator = Paginator(usuarios, 8)
    numero_pagina = request.GET.get('page')
    pagina = paginator.get_page(numero_pagina)

    return render(request, 'listar.html', {
        'usuarios': pagina,
        'termo_busca': termo,
        'tipo_busca': tipo,
    })


@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioModelForm()
    return render(request, 'form.html', {'form': form})


@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES, instance=usuario)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioModelForm(instance=usuario)
    return render(request, 'form.html', {'form': form})


@login_required
def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.ativo = False
        usuario.save()

        url_desfazer = reverse('restaurar_usuario', args=[usuario.pk])
        messages.success(
            request,
            format_html('Usuário <strong>{}</strong> excluído. <a href="{}" class="link-desfazer">Desfazer</a>', usuario.nome, url_desfazer)
        )
        return redirect('listar_usuarios')
    return render(request, 'confirmar_exclusao.html', {'usuario': usuario})


@login_required
def restaurar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.ativo = True
    usuario.save()
    messages.success(request, format_html('Usuário <strong>{}</strong> restaurado.', usuario.nome))
    return redirect('listar_usuarios')