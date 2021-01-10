from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from estoque.models import TipoProduto
from .forms import TipoProdutoForm, ProdutoForm, ProdutoFormSet, JsonAvaliacaoForm

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

# @transaction.atomic()
# def modo_manual_tipo_produto_add_2(request):
#     tipo_produto_form = TipoProdutoForm()
#     produto_formset = ProdutoFormSet()
#
#     if request.method == 'POST':
#         tipo_produto_form = TipoProdutoForm(request.POST)
#         if tipo_produto_form.is_valid():
#             tipo_produto = tipo_produto_form.save(commit=False)
#             produto_formset = ProdutoFormSet(request.POST, request.FILES, instance=tipo_produto)
#             if produto_formset.is_valid():
#                 tipo_produto.save()
#                 produto_formset.save()
#                 messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso')
#                 return redirect('modo_manual_tipo_produto_add_2')
#
#     return render(request,
#                   'estoque/modo_manual/tipo_produto/add/add_2.html',
#                   {'tipo_produto_form': tipo_produto_form, 'produto_formset': produto_formset})

@transaction.atomic()
def modo_manual_tipo_produto_add_2(request):
    tipo_produto_form = TipoProdutoForm(request.POST or None, request.FILES or None)
    produto_formset = ProdutoFormSet(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if tipo_produto_form.is_valid() and produto_formset.is_valid():
            tipo_produto = tipo_produto_form.save()

            produto_formset.instance = tipo_produto
            produto_formset.save()
            messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso')
            return redirect('modo_manual_tipo_produto_add_2')

    return render(request,
                  'estoque/modo_manual/tipo_produto/add/add_2.html',
                  {'tipo_produto_form': tipo_produto_form, 'produto_formset': produto_formset})


@transaction.atomic()
def modo_manual_tipo_produto_add_or_edit(request, id=None):
    try:
        tipo_produto = TipoProduto.objects.get(id=id)
        tipo_produto_id = id
        xxx = id
    except TipoProduto.DoesNotExist:
        tipo_produto = TipoProduto()

    tipo_produto_form = TipoProdutoForm(data=request.POST or None,
                                        files=request.FILES or None,
                                        instance=tipo_produto)
    produto_formset = ProdutoFormSet(data=request.POST or None,
                                     files=request.FILES or None,
                                     instance=tipo_produto)

    if request.method == 'POST':
        if tipo_produto_form.is_valid() and produto_formset.is_valid():
            tipo_produto_form.save()
            produto_formset.save()
            messages.add_message(request, messages.INFO, 'Cadastro realizado com sucesso')
            return redirect('modo_manual_tipo_produto_add_or_edit', id=tipo_produto.id)

    return render(request,
                  'estoque/modo_manual/tipo_produto/add_or_edit.html',
                  {'tipo_produto_form': tipo_produto_form, 'produto_formset': produto_formset,
                   'tipo_produto_id': tipo_produto_id, 'xxx':xxx})


def json_avaliacao_form(request):
    ETAPA_SESSION_ID = 'etapa3'

    # Montando o objeto etapas na memória.
    if not request.session.get(ETAPA_SESSION_ID):
        formulario = [
            {'name': 'nome_mae', 'label': 'Nome da Mãe', 'value': 'Maria José'},
            {'name': 'nome_pai', 'label': 'Nome do Pai', 'value': 'José Otávio'},
        ]
        formulario_avaliacao = {
            'nome_mae': {'status': 'OK', 'status_msg': None},
            'nome_pai': {'status': None, 'status_msg': None}
        }

        etapa_1 = {'etapa_atual': 1, 'formulario': formulario, 'formulario_avaliacao': formulario_avaliacao}
        etapa_2 = {'etapa_atual': 2, 'formulario': formulario, 'formulario_avaliacao': formulario_avaliacao}

        etapas = [etapa_1, etapa_2]

        for etapa in etapas:
            formulario = etapa['formulario']
            formulario_avaliacao = etapa['formulario_avaliacao']

            formulario_unificado = formulario.copy()
            for campo in formulario_unificado:
                name = campo['name']
                campo_avaliacao = formulario_avaliacao[name]
                # Adicionando em cada campo as informações da avaliação.
                campo['status'] = campo_avaliacao['status']
                campo['status_msg'] = campo_avaliacao['status_msg']

            etapa['formulario_unificado'] = formulario_unificado

        request.session[ETAPA_SESSION_ID] = etapas


    etapas = request.session[ETAPA_SESSION_ID]
    if (request.POST):
        existe_campo_aguardando_avaliacao = False
        for etapa in etapas:
            formulario_unificado = etapa['formulario_unificado']
            formulario_avaliacao = etapa['formulario_avaliacao']
            for campo in formulario_unificado:
                name = campo['name']
                status_name = 'etapa_{}____{}____status'.format(etapa['etapa_atual'], name)
                status_msg_name = '{}_msg'.format(status_name)

                status = request.POST[status_name]
                status = status if status else None
                status_msg = request.POST[status_msg_name]
                status_msg =status_msg if status == 'ERROR' and status_msg else None

                if not status and not existe_campo_aguardando_avaliacao:
                    existe_campo_aguardando_avaliacao = True
                    messages.add_message(request, messages.WARNING, 'Exitem campos aguardando avaliação.')

                # Atualizando em cada campo as informações da avaliação.
                # formulario_unificado
                campo['status'] = status
                campo['status_msg'] = status_msg

                # Atualizano a avaliação em si.
                # formulario_avaliacao
                avaliacao = formulario_avaliacao[name]
                avaliacao['status'] = status
                avaliacao['status_msg'] = status_msg


        request.session[ETAPA_SESSION_ID] = etapas

    return render(request,
                  'estoque/json_avaliacao_form/json_avaliacao_form.html',
                  {'etapas': etapas})