from django.db import models

# Create your models here.

class Usuario(models.Model):
# Isso é a forma do Django de criar um campo com opções fixas
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]
        
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    idade = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)


    def __str__(self):
        return self.nome



