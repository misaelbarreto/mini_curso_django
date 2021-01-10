from django.core.exceptions import ValidationError
from django.db import models, transaction
from atendimento.models import Cliente
from estoque.models import Produto, Estoque


# Create your models here.

class Venda(models.Model):
    cliente = models.ForeignKey(to=Cliente, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(verbose_name='Data e Hora', auto_now=True)

    class Meta:
        unique_together=[['cliente', 'data_hora']]
        ordering = ['-data_hora']

    def __str__(self):
        return 'Venda Nº {}'.format(self.id)

    def delete(self, using=None, keep_parents=False):
        if self.vendaitem_set.exists():
            raise ValidationError('Uma venda não pode ser excluída.')
        return super().delete(using, keep_parents)

    def qtd_vendaitens(self):
        return self.vendaitem_set.count()
    qtd_vendaitens.short_description = 'Quantidade de Itens'


class VendaItem(models.Model):
    venda = models.ForeignKey(to=Venda, on_delete=models.CASCADE)
    numero_item = models.IntegerField(verbose_name='Nº do Item', editable=False)
    produto = models.ForeignKey(to=Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name='Quantidade')
    preco = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2, editable=True)
    item_cancelado = models.BooleanField(verbose_name='Item cancelado', default=False)

    class Meta:
        ordering = ['-venda__id', 'numero_item']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_cancelado_old_value = self.item_cancelado

    def __str__(self):
        return '{} - Item Nº {}'.format(self.venda, self.numero_item)

    def __alteracao_proibida_detectada(self):
        venda_old = VendaItem.objects.get(pk=self.pk)
        if (self.venda != venda_old.venda
            or self.numero_item != venda_old.numero_item
            or self.produto != venda_old.produto
            or self.quantidade != venda_old.quantidade
            or self.preco != venda_old.preco):
            return True
        else:
            return False

    def _get_estoque_instance_to_record(self):
        estoque = Estoque(produto=self.produto,
                          quantidade=self.quantidade,
                          tipo_movimentacao=Estoque.TIPO_MOVIMENTACAO_VENDA_CANCELADA if self.item_cancelado else Estoque.TIPO_MOVIMENTACAO_VENDA_EFETUADA,
                          observacao=self)
        return estoque

    def clean(self):
        is_insert = not self.id

        if is_insert:
            if self.item_cancelado:
                raise ValidationError('Uma item não registrado não pode ser cancelado.')
        else:
            if self.item_cancelado_old_value and not self.item_cancelado:
                raise ValidationError('Operação não permitida pois este item já foi cancelado.')
            if self.__alteracao_proibida_detectada():
                raise ValidationError('Os dados da item da venda não podem ser alterados.')

        # Chamando a validação de estoque, para ver se não há nenhuma regra que está sendo ferida.
        self._get_estoque_instance_to_record().clean()
        super().clean()

    @transaction.atomic()
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_insert = not self.id
        if is_insert:
            self.numero_item = VendaItem.objects.filter(venda=self.venda).count() + 1
        self.preco = self.produto.preco
        super().save(force_insert, force_update, using, update_fields)

        # Executando o registro da venda junto ao estoque.
        self._get_estoque_instance_to_record().save()

    def delete(self, using=None, keep_parents=False):
        raise ValidationError('O item de uma venda não pode ser excluído, apenas cancelado.')
