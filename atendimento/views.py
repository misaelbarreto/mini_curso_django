import datetime

from django.http import HttpResponse
from django.template import Template, Context, loader


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
def index4(request):
    # Obs: Para o loader funcionar, se faz necessário que a aplicação esteja listada no settings.INSTALLED_APPS.
    template = loader.get_template('atendimento/index4.html')
    context = {
        'current_date': datetime.datetime.now(),
    }
    return HttpResponse(template.render(context, request))
