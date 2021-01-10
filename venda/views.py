from django.shortcuts import render
from venda.models import Produto
from django.http import JsonResponse

# Create your views here.

def load_preco_produto(request):
    produto_id = request.GET.get('produto_id')
    produto = Produto.objects.get(id=produto_id)
    return JsonResponse({'preco': produto.preco,})