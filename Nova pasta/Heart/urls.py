from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('Cadastro', views.Cadatro,name='Cadastro'),
    path('Dashbord',views.Dashbord,name='Dashbord'),
    path('Login', views.Login, name='Login'),
    
    #Url do grafio
    path('grafico',views.Grafico, name='gafrico'),
    
    #Aqui vai as urls das funções do banco
    path('Deposito', views.Deposito, name='Deposito'),
    path('Pagar',views.Pagar,name='Pagar'),
    path('Confirmar',views.Confirmar,name='Confirmar'),
    path('Transferir',views.Transferir , name='Transferir'),
    path('Criar_pix',views.Criar_pix, name='Criar_pix'),
    path('Confirmar_pix',views.Confirmar_pix, name='Confirmar_pix'),
    path('Enviar',views.Transferir_pix, name='Enviar'),
    path('Caxinha',views.Caxinhas,name='Caxinha'),
    path('Investir',views.Invest, name='Investir'),
]