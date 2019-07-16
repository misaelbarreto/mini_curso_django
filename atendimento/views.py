import datetime

from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
from django.views import generic

from .models import Cliente

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