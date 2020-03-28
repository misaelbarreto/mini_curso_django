from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TipoProdutoForm, ProdutoForm, ProdutoFormset

# Create your views here.


'''
- - - - - - - - - - - - - - - - - -
Controle Manual de Tipos de Produto
- - - - - - - - - - - - - - - - - -
'''
@transaction.atomic()
def modo_manual_tipo_produto_add(request):
    tipo_produto_form = TipoProdutoForm(request.POST or None, prefix='tp')
    # Neste cadastro de exemplo, estamos forçando o usuário a informar 2 produtos ao cadastrar um tipo de produto.
    produto_forms = [ProdutoForm(request.POST or None, prefix='p-'+str(x)) for x in range(0, 2)]

    if request.method == "POST":
        if tipo_produto_form.is_valid() and all([cf.is_valid() for cf in produto_forms]):
            tipo_produto = tipo_produto_form.save()
            for pf in produto_forms:
                # O "commit=False" devolve um objeto produto, validado, mas não persistido!
                produto = pf.save(commit=False)
                produto.tipo_produto = tipo_produto
                produto.save()

            messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso')
            # return HttpResponseRedirect('/estoque/tipo_produto/manual/add/')
            return redirect('modo_manual_tipo_produto_add')

    # https://stackoverflow.com/questions/5154358/django-what-is-the-difference-between-render-render-to-response-and-direc
    return render(request,
                  'estoque/modo_manual/tipo_produto/add/add.html',
                  {'tipo_produto_form': tipo_produto_form, 'produto_forms': produto_forms})


@transaction.atomic()
def modo_manual_tipo_produto_add_2(request):
    tipo_produto_form = TipoProdutoForm()
    produto_formset = ProdutoFormset()

    if request.method == 'POST':
        tipo_produto_form = TipoProdutoForm(request.POST)
        if tipo_produto_form.is_valid():
            tipo_produto = tipo_produto_form.save(commit=False)
            produto_formset = ProdutoFormset(request.POST, request.FILES, instance=tipo_produto)
            if produto_formset.is_valid():
                tipo_produto.save()
                produto_formset.save()
                messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso')
                return redirect('modo_manual_tipo_produto_add_2')

    return render(request,
                  'estoque/modo_manual/tipo_produto/add/add_2.html',
                  {'tipo_produto_form': tipo_produto_form, 'produto_formset': produto_formset})