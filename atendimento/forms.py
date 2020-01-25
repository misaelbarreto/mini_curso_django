from django import forms
from .models import Cliente


class ClienteManualForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    estado_civil = forms.ChoiceField(label='Estado Civil', choices=Cliente.ESTADO_CIVIL_CHOICES)
    cpf = forms.CharField(label='CPF', max_length=14)
    data_nascimento = forms.DateField(label='Data de Nascimento', required=False)
    email = forms.EmailField(label='E-mail', max_length=100, required=False)

    # Validação global do form.
    # https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-a-specific-field-attribute
    # def clean(self):
    #     raise ValidationError('Bloqueio temporário de cadastro.')
    #     return super().clean()


    # Caso precise realizar algum tratamento, alguma formatação, aqui é o local. O dado retornado será atualizado
    # no dicionário "self.cleaned_data".
    # https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-a-specific-field-attribute
    # def clean_cpf(self):
    #     data = self.cleaned_data['cpf']
    #     if Cliente.objects.filter(cpf=data).exists():
    #         raise forms.ValidationError('CPF já cadastrado na nossa base de dados.')
    #
    #     return data
