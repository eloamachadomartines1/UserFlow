from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario
from usuarios.forms import UsuarioModelForm
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse




def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', { 'form' : form })



def listar_usuarios(request):
    usuarios = Usuario.objects.filter(ativo=True)
    return render(request, 'listar.html', {'usuarios': usuarios})

@login_required
def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios') 
    # se nao validar vai voltar tudo do começo
    else:
        form = UsuarioModelForm()  
    return render(request, 'form.html', {'form': form })  


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
    return render( request, 'form.html', { 'form': form })


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