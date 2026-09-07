from django.contrib import admin
from django.urls import path
from estoque import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('fornecedores/', views.lista_fornecedores, name='fornecedores'),
    path('fornecedores/novo/', views.fornecedor_novo, name='fornecedor_novo'),
    path('fornecedores/editar/<int:id>/', views.fornecedor_editar, name='fornecedor_editar'),
    path('fornecedores/excluir/<int:id>/', views.fornecedor_excluir, name='fornecedor_excluir'),
    path('fornecedores/<int:id>/', views.detalhe_fornecedor, name='detalhe_fornecedor'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('clientes/editar/<int:id>/', views.cliente_editar, name='cliente_editar'),
    path('clientes/excluir/<int:id>/', views.cliente_excluir, name='cliente_excluir'),
    path('clientes/<int:id>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('produtos/', views.lista_produtos, name='produtos'),
    path('notas/', views.lista_notas, name='notas'),
    path('em-breve/', views.em_breve, name='em_breve'),
    path('admin/', views.admin_redirect, name='admin_redirect'),
    path('admin-secreto/', admin.site.urls),
    path('fornecedores/bloquear/<int:id>/', views.fornecedor_bloquear, name='fornecedor_bloquear'),
    path('fornecedores/desbloquear/<int:id>/', views.fornecedor_desbloquear, name='fornecedor_desbloquear'),
    path('clientes/bloquear/<int:id>/', views.cliente_bloquear, name='cliente_bloquear'),
    path('clientes/desbloquear/<int:id>/', views.cliente_desbloquear, name='cliente_desbloquear'),
]