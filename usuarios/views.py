from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from usuarios.forms import UsuarioModelForm


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar.html', {'usuarios' : usuarios} )


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
    return render( request, 'form.html', { 'form': form})


@login_required
def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'confirmar_exclusao.html', {'usuario':usuario})