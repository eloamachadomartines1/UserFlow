from django.contrib import admin
from usuarios.models import Usuario

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'idade', 'sexo']