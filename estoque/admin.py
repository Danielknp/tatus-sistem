from django.contrib import admin
from .models import Fornecedor, Produto, NotaFiscal, ItemNota, Cliente


class ItemNotaInline(admin.TabularInline):
    model = ItemNota
    extra = 1


class NotaFiscalAdmin(admin.ModelAdmin):
    inlines = [ItemNotaInline]
    list_display = ('numero', 'data_emissao', 'tipo', 'fornecedor')
    list_filter = ('tipo',)


class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'telefone', 'rua', 'bairro', 'cep')


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo', 'preco_venda', 'quantidade_estoque', 'fornecedor')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf_cnpj', 'telefone', 'rua', 'bairro', 'cep')


admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(NotaFiscal, NotaFiscalAdmin)
admin.site.register(Cliente, ClienteAdmin)