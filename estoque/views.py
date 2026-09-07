from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Fornecedor, Produto, NotaFiscal, ItemNota, Cliente
from .forms import FornecedorForm, ClienteForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'estoque/login.html')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'estoque/registro.html')
        
        if len(password1) < 8:
            messages.error(request, 'A senha deve ter pelo menos 8 caracteres.')
            return render(request, 'estoque/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já existe.')
            return render(request, 'estoque/registro.html')

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)  
        return redirect('dashboard')

    return render(request, 'estoque/registro.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    total_fornecedores = Fornecedor.objects.count()
    total_produtos = Produto.objects.count()
    total_notas = NotaFiscal.objects.count()
    produtos_baixo_estoque = Produto.objects.filter(quantidade_estoque__lt=10)
    ultimos_produtos = Produto.objects.order_by('-id')[:5]

    context = {
        'total_fornecedores': total_fornecedores,
        'total_produtos': total_produtos,
        'total_notas': total_notas,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'ultimos_produtos': ultimos_produtos,
    }
    return render(request, 'estoque/dashboard.html', context)

def lista_fornecedores(request):
    if not request.user.is_authenticated:
        return redirect('login')
    fornecedores = Fornecedor.objects.all()
    return render(request, 'estoque/fornecedores.html', {'fornecedores': fornecedores})

def lista_produtos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    produtos = Produto.objects.all()
    return render(request, 'estoque/produtos.html', {'produtos': produtos})

def lista_notas(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notas = NotaFiscal.objects.all()
    return render(request, 'estoque/notas.html', {'notas': notas})

from django.shortcuts import get_object_or_404  
def detalhe_fornecedor(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    fornecedor = get_object_or_404(Fornecedor, id=id)
    

    notas = NotaFiscal.objects.filter(fornecedor=fornecedor).order_by('-data_emissao')
    
  
    ultima_compra = notas.filter(tipo='E').first()
    
    context = {
        'fornecedor': fornecedor,
        'notas': notas,
        'ultima_compra': ultima_compra,
    }
    return render(request, 'estoque/fornecedor_detalhe.html', context)

from django.shortcuts import render

def em_breve(request):
    return render(request, 'estoque/em_breve.html')

def lista_clientes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    clientes = Cliente.objects.all() 
    return render(request, 'estoque/clientes.html', {'clientes': clientes})

def detalhe_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    cliente = get_object_or_404(Cliente, id=id)

    context = {
        'cliente': cliente,
    }
    return render(request, 'estoque/cliente_detalhe.html', context)

def fornecedor_novo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'estoque/fornecedor_form.html', {'form': form, 'titulo': 'Novo Fornecedor'})

def fornecedor_editar(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'estoque/fornecedor_form.html', {'form': form, 'titulo': 'Editar Fornecedor'})

from django.db.models import ProtectedError

def fornecedor_excluir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        try:
            fornecedor.delete()
            messages.success(request, 'Fornecedor excluído com sucesso!')
            return redirect('fornecedores')
        except ProtectedError:
            messages.error(request, 'Este fornecedor não pode ser excluído porque está vinculado a produtos ou notas fiscais. Remova os vínculos antes de excluir.')
            return redirect('fornecedores')
    return render(request, 'estoque/confirmar_exclusao.html', {'objeto': fornecedor, 'tipo': 'Fornecedor'})

def cliente_novo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'estoque/cliente_form.html', {'form': form, 'titulo': 'Novo Cliente'})

def cliente_editar(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'estoque/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})

def cliente_excluir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('clientes')
    return render(request, 'estoque/confirmar_exclusao.html', {'objeto': cliente, 'tipo': 'Cliente'})

def admin_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_superuser:
        return redirect('/admin-secreto/')
    else:
        messages.error(request, 'Acesso negado. Você não possui permissão para acessar este recurso. Por favor, solicite liberação ao administrador.')
        return redirect('dashboard')

def fornecedor_bloquear(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        fornecedor.ativo = False
        fornecedor.save()
        messages.success(request, f'Fornecedor {fornecedor.nome} bloqueado com sucesso!')
        return redirect('fornecedores')
    return render(request, 'estoque/confirmar_bloqueio.html', {
        'objeto': fornecedor,
        'tipo': 'Fornecedor',
        'acao': 'bloquear'
    })

def fornecedor_desbloquear(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    fornecedor = get_object_or_404(Fornecedor, id=id)
    if request.method == 'POST':
        fornecedor.ativo = True
        fornecedor.save()
        messages.success(request, f'Fornecedor {fornecedor.nome} desbloqueado com sucesso!')
        return redirect('fornecedores')
    return render(request, 'estoque/confirmar_bloqueio.html', {
        'objeto': fornecedor,
        'tipo': 'Fornecedor',
        'acao': 'desbloquear'
    })

def cliente_bloquear(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.ativo = False
        cliente.save()
        messages.success(request, f'Cliente {cliente.nome} bloqueado com sucesso!')
        return redirect('clientes')
    return render(request, 'estoque/confirmar_bloqueio.html', {
        'objeto': cliente,
        'tipo': 'Cliente',
        'acao': 'bloquear'
    })

def cliente_desbloquear(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.ativo = True
        cliente.save()
        messages.success(request, f'Cliente {cliente.nome} desbloqueado com sucesso!')
        return redirect('clientes')
    return render(request, 'estoque/confirmar_bloqueio.html', {
        'objeto': cliente,
        'tipo': 'Cliente',
        'acao': 'desbloquear'
    })