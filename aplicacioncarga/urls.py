from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consumirServicio/', views.consumirServicio, name='consumirServicio'),
    path('resultadoServicio/', views.resultadoServicio, name='resultadoServicio'),
]
