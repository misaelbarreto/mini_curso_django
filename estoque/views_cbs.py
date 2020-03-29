from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProdutoFormSet
from .models import TipoProduto


class TipoProdutoList(ListView):
    model = TipoProduto


class TipoProdutoCreate(CreateView):
    model = TipoProduto
    fields = ['descricao',]


class TipoProdutoProdutoCreate(CreateView):
    model = TipoProduto
    fields = ['descricao',]
    success_url = reverse_lazy('tipo_produto-list')

    def get_context_data(self, **kwargs):
        data = super(TipoProdutoProdutoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['produtos'] = ProdutoFormSet(self.request.POST)
        else:
            data['produtos'] = ProdutoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        produtos = context['produtos']
        with transaction.atomic():
            self.object = form.save()

            if produtos.is_valid():
                produtos.instance = self.object
                produtos.save()
        return super(TipoProdutoProdutoCreate, self).form_valid(form)


class TipoProdutoUpdate(UpdateView):
    model = TipoProduto
    success_url = '/'
    fields = ['descricao',]


class TipoProdutoProdutoUpdate(UpdateView):
    model = TipoProduto
    fields = ['descricao',]
    success_url = reverse_lazy('tipo_produto-list')

    def get_context_data(self, **kwargs):
        data = super(TipoProdutoProdutoUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['produtos'] = ProdutoFormSet(self.request.POST, instance=self.object)
        else:
            data['produtos'] = ProdutoFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        produtos = context['produtos']
        with transaction.atomic():
            self.object = form.save()

            if produtos.is_valid():
                produtos.instance = self.object
                produtos.save()
        return super(TipoProdutoProdutoUpdate, self).form_valid(form)


class TipoProdutoDelete(DeleteView):
    model = TipoProduto
    success_url = reverse_lazy('tipo_produto-list')
