from django.urls import path

from . import views

urlpatterns = [
    path('load_preco_produto/', views.load_preco_produto, name='load_preco_produto'),

]

