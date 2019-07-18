from django.contrib import admin
from .models import Cliente

# Register your models here.

# Exemplo 1: Registrar um modelo junto ao Django Admin.
# admin.site.register(Cliente)


# Exemplo 2: Registrar um modelo junto ao Django Admin e fazendo customizações básicas.
class ClienteAdmin(admin.ModelAdmin):
    fields = ['nome', 'cpf', 'estado_civil',]
    search_fields = ['nome', 'cpf']
    list_filter = ['estado_civil', ]
    list_display = ('nome', 'cpf', 'estado_civil', 'data_nascimento', 'email', 'data_hora_cadastro')
    list_display_links = ('nome',)

admin.site.register(Cliente, ClienteAdmin)