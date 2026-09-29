from django import template

register = template.Library()

@register.filter
def formatar_cpf(cpf):
    if not cpf or len(cpf) != 11:
        return cpf
    return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'