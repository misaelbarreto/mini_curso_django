from django.db import models

# Create your models here.
from django.db import models


class Cliente(models.Model):
    ESTADO_CIVIL_CHOICES = (
        ('SOLTEIRO', u'Solteiro'),
        ('CASADO', u'Casado'),
        ('DIVORCIADO', u'Divorciado'),
        ('VIUV', u'Viúvo'),
    )

    nome = models.CharField(verbose_name='Nome', max_length=100)
    estado_civil = models.CharField(verbose_name='Estado Civil', max_length=10, choices=ESTADO_CIVIL_CHOICES)
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    data_nascimento = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['nome']

    # Label padrão que será exibido em toda o admin do Django.
    def __str__(self):
        return self.nome