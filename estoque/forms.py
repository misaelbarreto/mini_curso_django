from django import forms
from django.forms import inlineformset_factory

from .models import TipoProduto, Produto


class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = '__all__'
        widgets = {'xxx': forms.HiddenInput()}


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ('tipo_produto',)

# https://docs.djangoproject.com/en/3.0/topics/forms/formsets/#formsets
ProdutoFormSet = inlineformset_factory(TipoProduto, Produto,
                                       exclude = ('tipo_produto',),
                                       can_delete=True,)



from django.utils.safestring import mark_safe

# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#     def render(self):
#         return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class HorizontalRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_style = 'style="display: inline-block; margin-right: 10px;"'
        self.renderer.inner_html = '<li ' + css_style + '>{choice_value}{sub_widgets}</li>'

class JsonAvaliacaoForm(forms.Form):
    CHOICES = [
        (None, 'Aguardando Avaliação'),
        ('OK', 'OK'),
        ('ERROR', 'Com Problema'),
    ]

    like = forms.ChoiceField(label='Nome da Mãe - Maria José',
                            choices=CHOICES,
                             widget=forms.RadioSelect(attrs={'class': 'special'}),
                             initial=None)
