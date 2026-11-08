from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Fornecedor, Produto, NotaFiscal, ItemNota, Cliente
from .forms import FornecedorForm, ClienteForm, ProdutoForm, InventarioForm, NotaEntradaForm, ItemEntradaForm, NotaSaidaForm, ItemSaidaForm


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
    q = request.GET.get('q', '').strip()
    fornecedores = Fornecedor.objects.all().order_by('-id')
    if q:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=q) | Q(cnpj__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'estoque/fornecedores.html', {'fornecedores': fornecedores, 'q': q})

def lista_produtos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    q = request.GET.get('q', '').strip()
    produtos = Produto.objects.all().order_by('-id')
    if q:
        produtos = produtos.filter(
            Q(nome__icontains=q) | Q(codigo__icontains=q) | Q(fornecedor__nome__icontains=q)
        )
    return render(request, 'estoque/produtos.html', {'produtos': produtos, 'q': q})

def lista_notas(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Pega o que foi digitado na barra de pesquisa (se estiver vazio, pega None)
    busca = request.GET.get('q')
    
    if busca:
        # Filtra pelo número da nota (icontains significa "contém", e ignora maiúsculas/minúsculas)
        notas = NotaFiscal.objects.filter(numero__icontains=busca).order_by('-data_emissao')
    else:
        # Se não tiver busca, mostra todas
        notas = NotaFiscal.objects.all().order_by('-data_emissao')
        
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
    q = request.GET.get('q', '').strip()
    clientes = Cliente.objects.all().order_by('-id')
    if q:
        clientes = clientes.filter(
            Q(nome__icontains=q) | Q(cpf_cnpj__icontains=q) | Q(email__icontains=q)
        )
    return render(request, 'estoque/clientes.html', {'clientes': clientes, 'q': q})

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

from django.db.models import ProtectedError, Q

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

def produto_novo(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm()
    return render(request, 'estoque/produto_form.html', {'form': form, 'titulo': 'Novo Produto'})


def produto_editar(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)

        if produto.fornecedor:
            form.fields['fornecedor'].queryset = Fornecedor.objects.filter(
                Q(ativo=True) | Q(id=produto.fornecedor.id)
            )
    return render(request, 'estoque/produto_form.html', {'form': form, 'titulo': 'Editar Produto'})


def produto_excluir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, 'Produto excluído com sucesso!')
        except ProtectedError:
            messages.error(request, 'Este produto não pode ser excluído porque está vinculado a uma nota fiscal. Remova o vínculo antes de excluir.')
        return redirect('produtos')
    return render(request, 'estoque/confirmar_exclusao.html', {'objeto': produto, 'tipo': 'Produto'})


def detalhe_produto(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    produto = get_object_or_404(Produto, id=id)
    itens = ItemNota.objects.filter(produto=produto).order_by('-nota__data_emissao')
    context = {
        'produto': produto,
        'itens': itens,
    }
    return render(request, 'estoque/produto_detalhe.html', context)

def produto_inventario(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            quantidade_anterior = produto.quantidade_estoque
            produto.quantidade_estoque = form.cleaned_data['quantidade_estoque']
            produto.save()
            messages.success(
                request,
                f'Estoque de "{produto.nome}" ajustado de {quantidade_anterior} para {produto.quantidade_estoque} unidades.'
            )
            return redirect('detalhe_produto', id=produto.id)
    else:
        form = InventarioForm(initial={'quantidade_estoque': produto.quantidade_estoque})
    return render(request, 'estoque/produto_inventario.html', {
        'form': form,
        'produto': produto,
        'titulo': f'Ajuste de Inventário — {produto.nome}'
    })

def nota_entrada_nova(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = NotaEntradaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.tipo = 'E'  
            
            nota.save()
            messages.success(request, f'Nota de Entrada nº {nota.numero} registrada! Agora adicione os produtos.')
            return redirect('nota_entrada_detalhe', id=nota.id)
    else:
        form = NotaEntradaForm()
    return render(request, 'estoque/nota_entrada_form.html', {'form': form, 'titulo': 'Nova Nota de Entrada'})


def nota_entrada_detalhe(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    nota = get_object_or_404(NotaFiscal, id=id, tipo='E')
    
    if request.method == 'POST':
        item_form = ItemEntradaForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.nota = nota
            item.save()

            produto = item.produto
            
            valor_total_atual = float(produto.quantidade_estoque) * float(produto.preco_compra)
            
            valor_total_novo = float(item.quantidade) * float(item.preco_unitario)
            
            nova_qtd = produto.quantidade_estoque + item.quantidade
            
           
            if nova_qtd > 0:
                novo_preco = (valor_total_atual + valor_total_novo) / nova_qtd
                produto.preco_compra = round(novo_preco, 2)
            
            produto.quantidade_estoque = nova_qtd
            produto.save()
            
            messages.success(request, f'Produto "{produto.nome}" adicionado! Estoque atualizado para {nova_qtd} un.')
            return redirect('nota_entrada_detalhe', id=nota.id)
    else:
        item_form = ItemEntradaForm()
        
    itens = nota.itens.all()
    return render(request, 'estoque/nota_entrada_detalhe.html', {
        'nota': nota,
        'itens': itens,
        'item_form': item_form
    })

def detalhe_nota(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    nota = get_object_or_404(NotaFiscal, id=id)
    # Pega todos os itens que pertencem a essa nota
    itens = nota.itens.all()
    
    total_geral = sum(item.quantidade * item.preco_unitario for item in itens)
    
    context = {
        'nota': nota,
        'itens': itens,
        'total_geral': total_geral,
    }
    return render(request, 'estoque/nota_detalhe.html', context)

def lista_notas_saida(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    q = request.GET.get('q', '').strip()
    notas = NotaFiscal.objects.filter(tipo='S').order_by('-data_emissao')
    
    # Se o usuário digitou algo na busca, filtra pelo número da nota ou nome do cliente
    if q:
        notas = notas.filter(
            Q(numero__icontains=q) | Q(cliente__nome__icontains=q)
        )
        
    return render(request, 'estoque/notas_saida.html', {'notas': notas, 'q': q})

def nota_saida_nova(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = NotaSaidaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.tipo = 'S'
            
            # Gera o número automático de 9 dígitos (ex: 000000001)
            count = NotaFiscal.objects.filter(tipo='S').count() + 1
            nota.numero = str(count).zfill(9)
            
            nota.save()
            messages.success(request, f'Nota de Saída nº {nota.numero} iniciada! Agora adicione os produtos.')
            return redirect('nota_saida_adicionar_item', id=nota.id)
    else:
        form = NotaSaidaForm()
    return render(request, 'estoque/nota_saida_form.html', {'form': form, 'titulo': 'Nova Nota de Saída'})

def nota_saida_detalhe(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    nota = get_object_or_404(NotaFiscal, id=id, tipo='S')
    itens = nota.itens.all()
    
    # Apenas mostra os dados
    return render(request, 'estoque/nota_saida_detalhe.html', {
        'nota': nota,
        'itens': itens
    })

def imprimir_nota(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    numero = request.GET.get('numero')
    if not numero:
        messages.error(request, 'Digite o número da nota.')
        return redirect('notas_saida')
        
    try:
        # Busca a nota (seja de entrada ou saída) pelo número exato
        nota = NotaFiscal.objects.get(numero=numero)
    except NotaFiscal.DoesNotExist:
        messages.error(request, f'Nota número "{numero}" não encontrada.')
        return redirect('notas_saida')
        
    return render(request, 'estoque/imprimir_nota.html', {'nota': nota})

def nota_saida_excluir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    nota = get_object_or_404(NotaFiscal, id=id, tipo='S')
    
    if request.method == 'POST':
        # A MÁGICA DA BORRACHA: Devolve os produtos para o estoque antes de apagar
        for item in nota.itens.all():
            produto = item.produto
            produto.quantidade_estoque += item.quantidade
            produto.save()
            
        nota.delete()
        messages.success(request, f'Nota de Saída {nota.numero} excluída. Os produtos voltaram para o estoque.')
        return redirect('notas_saida')
        
    return render(request, 'estoque/confirmar_exclusao.html', {'objeto': nota, 'tipo': 'Nota de Saída'})

def nota_saida_adicionar_item(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    nota = get_object_or_404(NotaFiscal, id=id, tipo='S')
    
    if request.method == 'POST':
        item_form = ItemSaidaForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.nota = nota
            produto = item.produto
            
            if item.quantidade > produto.quantidade_estoque:
                messages.error(request, f'Estoque insuficiente! O produto "{produto.nome}" só tem {produto.quantidade_estoque} un.')
                return redirect('nota_saida_adicionar_item', id=nota.id)
            
            item.save()
            produto.quantidade_estoque -= item.quantidade
            produto.save()
            
            messages.success(request, f'Produto "{produto.nome}" adicionado! Estoque atualizado.')
            return redirect('nota_saida_adicionar_item', id=nota.id)
    else:
        item_form = ItemSaidaForm()
        
    itens = nota.itens.all()
    return render(request, 'estoque/nota_saida_adicionar_item.html', {
        'nota': nota,
        'itens': itens,
        'item_form': item_form
    })