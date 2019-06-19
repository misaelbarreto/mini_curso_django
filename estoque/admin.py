from django.contrib import admin
from .models import Produto, TipoProduto, Estoque

# Register your models here.
class TipoProdutoAdmin(admin.ModelAdmin):
    search_fields = ['descricao',]
admin.site.register(TipoProduto, TipoProdutoAdmin)


class EstoqueAdmin(admin.ModelAdmin):
    search_fields = ['produto__nome']
    list_display = ('produto', 'quantidade', 'tipo_movimentacao', 'data', 'observacao')
admin.site.register(Estoque, EstoqueAdmin)


class ProdutoAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_filter = ['tipo_produto', ]
    list_display = ('nome', 'preco', 'tipo_produto', 'quantidade_em_estoque',  'data_ultima_atualizacao')
admin.site.register(Produto, ProdutoAdmin)