import datetime

from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from django.views import generic

from .models import Cliente
from .forms import ClienteManualForm


# Create your views here.

# Exemplo de controle que retorna como resposta um texto simples.
def index(request):
    return HttpResponse('Hi Houston! It s all right!')


# Exemplo de controle que retorna como resposta um html simples.
def index2(request):
    html = '<html><body style="color: red">Hi Houston! It s all right!</body></html>'
    return HttpResponse(html)


# Exemplo de controle que retorna como resposta um html simples através de um template criado em tempo de execução.
def index3(request):
    now = datetime.datetime.now()

    # Obs: A data já é exibida de acordo com a configuração realizada no
    # Django: It timeeeeeee 3 de Julho de 2014 às 11:59.
    template = Template('<html><body>Houston, now is {{ current_date }}.</body></html>')
    # Contexto representa o conjunto de variáveis que serão processadas pelo template.
    context = Context({'current_date': now})
    html = template.render(context)

    return HttpResponse(html)


# Exemplo de controle que retorna como resposta um html simples através de um template armazenado em arquivo.
def index4a(request):
    # Obs: Para o loader funcionar, se faz necessário que a aplicação esteja listada no settings.INSTALLED_APPS.
    template = loader.get_template('atendimento/index4.html')
    context = {
        'current_date': datetime.datetime.now(),
    }
    return HttpResponse(template.render(context, request))


# Exemplo de controle, que recebe opcionalmente o parâmetro idade retorna como resposta um html simples através de um
# template armazenado em arquivo.
def index4b(request, idade=None):
    current_date = datetime.datetime.now()
    # locals() retorna um dicionário contento todos as variáveis locais disponíveis.
    # print(locals())
    return render(request, 'atendimento/index4.html', locals())


'''
- - - - - - - - - - - - - - 
Controle Manual de Clientes
- - - - - - - - - - - - - - 
'''


def modo_manual_cliente_list(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'atendimento/modo_manual/cliente/list.html', context)


class ModoManualClienteListView(generic.ListView):
    template_name = 'atendimento/modo_manual/cliente/list.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        return Cliente.objects.all()


def modo_manual_client_add(request):
    if request.method == 'POST':
        # Quando o form é populado, ele é chamado de Bound Form (método is_bound retorna True)
        # request.POST traz todos os dados submetidos no formulário que tiverem o atributo "name" definido, inclusive
        # botões.
        form = ClienteManualForm(request.POST)

        # Pecorrendo todos os fields, na perspectiva html (classe django.forms.boundfield.BoundField), de um form.
        # Obs: Não confundir com os fields definidos no Form. Aí a classe é outra (django.forms.field.Field)
        # https://docs.djangoproject.com/pt-br/3.0/ref/forms/api/#django.forms.BoundField
        for boundfield in form:
            print(boundfield, boundfield.id_for_label,  boundfield.data, boundfield.errors, boundfield.field)



        # Ao chamar o "is_valid", as validações a nível de form são chamadas. O retorno será True caso esteja tudo certo,
        # caso contrário será false e haverá dentro do objeto form dados sobre os erros encontrados.
        if form.is_valid():
            try:
                cliente = Cliente(nome=form.cleaned_data['nome'],
                                  estado_civil=form.cleaned_data['estado_civil'],
                                  cpf=form.cleaned_data['cpf'],
                                  data_nascimento=form.cleaned_data['data_nascimento'],
                                  email=form.cleaned_data['email'])
                cliente.clean()
                cliente.save()
                return HttpResponse('Cadastro realizado com sucesso.')
            except Exception as e:
                return HttpResponse(str(e))
    else:
        # Quando o form está zerado, ele é chamado de Unound Form (método is_bound retorna False)
        form = ClienteManualForm()

    return render(request, 'atendimento/modo_manual/cliente/add/add.html', {'form': form})
