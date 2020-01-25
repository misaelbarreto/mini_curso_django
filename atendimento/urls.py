from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),
    path('index4a/', views.index4a, name='index4a'),
    path('index4b/', views.index4b, name='index4b'),
    path('index4b/<int:idade>/', views.index4b, name='index4b'),

    # Modo Manual
    path('cliente/manual/list/', views.modo_manual_cliente_list, name='modo_manual_cliente_list'),
    path('cliente/manual/list2/', views.ModoManualClienteListView.as_view(), name='modo_manual_cliente_list_view'),
    path('cliente/manual/add/', views.modo_manual_client_add, name='modo_manual_client_add'),
]

