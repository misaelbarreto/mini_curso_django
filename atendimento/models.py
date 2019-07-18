from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.db import models


class Cliente(models.Model):
    ESTADO_CIVIL_CHOICES = (
        ('SOLTEIRO', u'Solteiro'),
        ('CASADO', u'Casado'),
        ('DIVORCIADO', u'Divorciado'),
        ('VIUVO', u'Viúvo'),
    )

    nome = models.CharField(verbose_name='Nome', max_length=100)
    estado_civil = models.CharField(verbose_name='Estado Civil', max_length=10, choices=ESTADO_CIVIL_CHOICES)
    cpf = models.CharField(verbose_name='CPF', max_length=14)
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    email = models.EmailField('E-mail', max_length=100, blank=True, null=True)
    data_hora_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    class Meta:
        ordering = ['nome']

    # Retorna a representação padrão desse modelo.
    def __str__(self):
        return self.nome

    # Método que faz validações customizadas. O ideal é que toda a validação do modelo se concentre aqui, e não em views
    # ou forms, assim temos o código em um só local e facilitamos a sua manutenção.
    # ModelForms invocam o método clean() antes de chamar o método save(). Obs:  Admin utiliza internamente um ModelForm.
    def clean(self):
        if self.nome:
            self.nome = self.nome.strip()
            if len(self.nome.split(' ')) < 2:
                raise ValidationError({'nome':'Nome e sobrenome são requeridos.'})

        super().clean()

