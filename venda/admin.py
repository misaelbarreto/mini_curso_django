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

    # Ref:
    # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/javascript/
    # https://stackoverflow.com/questions/3785178/how-to-use-custom-js-with-django-inline/3824931#3824931
    class Media:
        js = [
            'https://code.jquery.com/jquery-3.3.1.min.js',
            '/static/venda/js/carregar_venda_item_preco.js'
        ]


    def get_client_cpf(self, obj):
        return obj.cliente.cpf
    get_client_cpf.short_description = 'Cpf'
    get_client_cpf.admin_order_field = 'cliente__cpf'
admin.site.register(Venda, VendaAdmin)


class VendaItemAdmin(admin.ModelAdmin):
    list_display = ('venda', 'get_venda_client', 'numero_item', 'produto', 'quantidade', 'preco')
    #search_fields = ['cliente__nome', 'cliente__cpf']

    class Media:
        js = [
            'https://code.jquery.com/jquery-3.3.1.min.js',
            '/static/venda/js/teste.js'
        ]


    def get_venda_client(self, obj):
        return obj.venda.cliente
    get_venda_client.short_description = 'Cliente'
    get_venda_client.admin_order_field = 'venda__cliente__nome'
admin.site.register(VendaItem, VendaItemAdmin)