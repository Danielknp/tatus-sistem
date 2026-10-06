from django import forms
from .models import Fornecedor, Cliente, Produto

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'telefone', 'email', 'cep', 'rua', 'numero', 'bairro']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fornecedor'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0001-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@empresa.com'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }
        labels = {
            'nome': 'Nome do Fornecedor',
            'cnpj': 'CNPJ',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'cep': 'CEP',
            'rua': 'Rua',
            'numero': 'Número',
            'bairro': 'Bairro',
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'telefone', 'email', 'cep', 'rua', 'numero', 'bairro']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00 ou 00.000.000/0001-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@email.com'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }
        labels = {
            'nome': 'Nome do Cliente',
            'cpf_cnpj': 'CPF/CNPJ',
            'telefone': 'Telefone',
            'email': 'E-mail',
            'cep': 'CEP',
            'rua': 'Rua',
            'numero': 'Número',
            'bairro': 'Bairro',
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco_compra', 'preco_venda', 'fornecedor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Descrição do Produto',
            'preco_compra': 'Preço de Compra Inicial (R$)',
            'preco_venda': 'Preço de Venda (R$)',
            'fornecedor': 'Fornecedor',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
        self.fields['fornecedor'].empty_label = "Selecione um fornecedor ativo"

    def save(self, commit=True):
        produto = super().save(commit=False)

        
        if not produto.codigo:
            codigos = Produto.objects.values_list('codigo', flat=True)
            numeros = [int(c) for c in codigos if c and c.isdigit()]
            proximo = max((max(numeros) + 1) if numeros else 0, 7)
            produto.codigo = str(proximo).zfill(7)

        if commit:
            produto.save()
        return produto


class InventarioForm(forms.Form):
    quantidade_estoque = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Nova Quantidade em Estoque'
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Motivo do Ajuste (opcional)'
    )