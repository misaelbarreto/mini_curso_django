from django.http import HttpResponse
import datetime
from django.template import Template, Context


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
    template = Template('<html><body>It timeeeeeee {{ current_date }}.</body></html>')
    context = Context({'current_date': now})
    html = template.render(context)

    return HttpResponse(html)