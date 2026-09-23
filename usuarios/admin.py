from django.contrib import admin
from django.utils.html import format_html
from usuarios.models import Usuario

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'idade', 'sexo']


def mostrar_foto(self, obj):
         if obj.foto:
             return format_html('<img src="{}" width="50" style="border-radius:5px;" />', obj.foto.url)
         return "Sem foto"

mostrar_foto.short_description = 'Foto'