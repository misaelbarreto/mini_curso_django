from django.contrib import admin
from .models import Venda, VendaItem

# Register your models here.
class VendaItemInline(admin.StackedInline):
    model = VendaItem
    extra = 3

class VendaAdmin(admin.ModelAdmin):
    inlines = [VendaItemInline]
    list_display = ('__str__', 'cliente', 'get_client_cpf', 'data_hora', 'qtd_vendaitens')
    search_fields = ['cliente__nome', 'cliente__cpf']

    def get_client_cpf(self, obj):
        return obj.cliente.cpf
    get_client_cpf.short_description = 'Cpf'
    get_client_cpf.admin_order_field = 'cliente__cpf'
admin.site.register(Venda, VendaAdmin)


class VendaItemAdmin(admin.ModelAdmin):
    list_display = ('venda', 'get_venda_client', 'numero_item', 'produto', 'quantidade', 'preco')
    #search_fields = ['cliente__nome', 'cliente__cpf']

    def get_venda_client(self, obj):
        return obj.venda.cliente
    get_venda_client.short_description = 'Cliente'
    get_venda_client.admin_order_field = 'venda__cliente__nome'
admin.site.register(VendaItem, VendaItemAdmin)