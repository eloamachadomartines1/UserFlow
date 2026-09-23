from django.contrib import admin
from usuarios.models import Usuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'idade', 'sexo')
    search_fields = ('nome', 'cpf')

admin.site.register(Usuario, UsuarioAdmin)