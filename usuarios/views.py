from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuario
from usuarios.forms import UsuarioModelForm
# Create your views here.

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar.html', {'usuarios' : usuarios} )



def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios') 
    # se nao validar vai voltar tudo do começo
    else:
        form = UsuarioModelForm()  

    return render(request, 'form.html', {'form': form})  


def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, instance=usuario)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')

    else:
        form = UsuarioModelForm(instance=usuario)
    return render( request, 'form.html', { 'form': form})


def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'confirmar_exclusao.html', {'usuario':usuario})