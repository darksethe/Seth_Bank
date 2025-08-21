from django.contrib import admin
from .models import Contas, Pix, Caxinha, Investir, Movimentacao


# Register your models here.

class List_Contas(admin.ModelAdmin):
    list_display = ('Nome', 'Saldo', 'Conta')


class List_Pix(admin.ModelAdmin):
    list_display = ('Nome', 'Chave')


class List_Caxinha(admin.ModelAdmin):
    list_display = ('Nome', 'Caxinha', 'Valor', 'Datas')

class List_Investir(admin.ModelAdmin):
    list_display = ('Nome', 'Invest', 'Datas')

class List_Movimentacao(admin.ModelAdmin):
    list_display = ('Conta', 'Valor', 'Data','Descricao','Tipo')

admin.site.register(Contas, List_Contas)
admin.site.register(Pix, List_Pix)
admin.site.register(Caxinha, List_Caxinha)
admin.site.register(Investir,List_Investir)
admin.site.register(Movimentacao,List_Movimentacao)