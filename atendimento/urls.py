from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('index2', views.index2, name='index2'),
    path('index3', views.index3, name='index3'),
    path('index4a', views.index4a, name='index4a'),
    path('index4b', views.index4b, name='index4b'),
    path('index4b/<int:idade>', views.index4b, name='index4b'),
]

