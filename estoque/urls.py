from django.urls import path

from . import views

urlpatterns = [
    path('tipo_produto/manual/add/', views.modo_manual_tipo_produto_add, name='modo_manual_tipo_produto_add'),
    path('tipo_produto/manual/add_2/', views.modo_manual_tipo_produto_add_2, name='modo_manual_tipo_produto_add_2'),
    path('tipo_produto/manual/add_or_edit/', views.modo_manual_tipo_produto_add_or_edit, name='modo_manual_tipo_produto_add_or_edit'),
    path('tipo_produto/manual/add_or_edit/<int:id>/', views.modo_manual_tipo_produto_add_or_edit, name='modo_manual_tipo_produto_add_or_edit'),
]

