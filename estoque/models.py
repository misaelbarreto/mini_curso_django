from django.core.exceptions import ValidationError
from django.db import transaction
from django.db import models

# Create your models here.


class TipoProduto(models.Model):
    descricao = models.CharField(verbose_name='Nome', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Tipo de Produto'
        verbose_name_plural = 'Tipos de Produtos'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao


class Produto(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=100, unique=True)
    preco = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2)
    tipo_produto = models.ForeignKey(to=TipoProduto, on_delete=models.CASCADE)
    # Quantidade em estoque é uma informação redundante. Pensando a longo prazo, pode ficar muito caro ficar calculando
    # isso com base nas entradas e saídas registradas no estoque.
    quantidade_em_estoque = models.IntegerField(verbose_name='Quantidade Em Estoque', default=0, editable=False)
    data_ultima_atualizacao = models.DateTimeField(verbose_name='Data da Última Atualização', auto_now=True, editable=False)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    TIPO_MOVIMENTACAO_ENTRADA = 'ENTRADA'
    TIPO_MOVIMENTACAO_SAIDA = 'SAIDA'
    TIPO_MOVIMENTACAO_VENDA_EFETUADA = 'VENDA_EFETUADA'
    TIPO_MOVIMENTACAO_VENDA_CANCELADA = 'VENDA_CANCELADA'
    TIPO_MOVIMENTACAO_CHOICES = (
        (TIPO_MOVIMENTACAO_ENTRADA, u'Entrada'),
        (TIPO_MOVIMENTACAO_SAIDA, u'Saída'),
        (TIPO_MOVIMENTACAO_VENDA_EFETUADA, u'Venda Efetuada'),
        (TIPO_MOVIMENTACAO_VENDA_CANCELADA, u'Venda Cancelada'),
    )

    produto = models.ForeignKey(to=Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name='Quantidade')
    tipo_movimentacao = models.CharField(verbose_name='Tipo de Movimentação', max_length=10, choices=TIPO_MOVIMENTACAO_CHOICES)
    observacao = models.CharField(verbose_name='Observação', max_length=255, blank=True, null=True)
    data = models.DateTimeField(verbose_name='Data', auto_now=True,editable=False)

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['produto', 'quantidade', 'tipo_movimentacao']

    def __str__(self):
        return '{} - {} - {}'.format(self.produto, self.quantidade, self.tipo_movimentacao)

    def clean(self):
        if self.id:
            raise ValidationError('Os registros de estoque não podem ser editados.');
        else:
            self.__get_saldo_quantidade_em_estoque()

    def delete(self, using=None, keep_parents=False):
        raise ValidationError('Os registros de estoque não podem ser removidos.');

    def __get_saldo_quantidade_em_estoque(self):
        # Atualizando a informação da quantidade em estoque do produto.
        if self.tipo_movimentacao in [Estoque.TIPO_MOVIMENTACAO_ENTRADA, Estoque.TIPO_MOVIMENTACAO_VENDA_CANCELADA]:
            return self.produto.quantidade_em_estoque + self.quantidade
        elif self.tipo_movimentacao in [Estoque.TIPO_MOVIMENTACAO_SAIDA, Estoque.TIPO_MOVIMENTACAO_VENDA_EFETUADA]:
            if self.produto.quantidade_em_estoque <= self.quantidade:
                raise ValidationError('O saldo atual de "{}" é de {}. Impossível realizar uma baixa de {}.'\
                                      .format(self.produto, self.produto.quantidade_em_estoque, self.quantidade))
            return self.produto.quantidade_em_estoque - self.quantidade


    @transaction.atomic()
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.produto.quantidade_em_estoque = self.__get_saldo_quantidade_em_estoque()
        self.produto.save()
        super().save(force_insert, force_update, using, update_fields)


