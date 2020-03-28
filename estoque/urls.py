from django.urls import path

from . import views

urlpatterns = [
    path('tipo_produto/manual/add/', views.modo_manual_tipo_produto_add, name='modo_manual_tipo_produto_add'),
]

