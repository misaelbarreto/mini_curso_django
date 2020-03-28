from django import forms
from django.forms import inlineformset_factory

from .models import TipoProduto, Produto


class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = '__all__'


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('tipo_produto',)

ProdutoFormset = inlineformset_factory(TipoProduto, Produto,
                                       exclude = ('tipo_produto',),
                                       can_delete=True)
