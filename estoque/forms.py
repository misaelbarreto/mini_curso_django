from django import forms

from .models import TipoProduto, Produto


class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = '__all__'

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('tipo_produto',)