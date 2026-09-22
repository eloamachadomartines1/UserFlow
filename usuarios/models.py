from django.db import models
from django.core.validators import RegexValidator

class Usuario(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    cpf_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='CPF deve conter exatamente 11 números, sem pontos ou traços.'
    )

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, validators=[cpf_validator])
    idade = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    def __str__(self):
        return self.nome