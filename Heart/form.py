from django import forms
from django.forms import ModelForm
from .models import Contas, Investir

class Foto(forms.Form):
    model = Contas
    fields = [ 'Img']

class Investir(forms.Form):
    opt = [('1','CDB'),('2','Tesouro Direto')]
    datas = [('1','1 ano'),('2','3 Anos'),('3','5 Anos')]
    model = Investir
    fields = ['Invest', 'Valor', 'Datas', 'Porcetagem']
    widgets = {
        "Invest" : forms.CharField(label='Invetir',widget=forms.Select(choices=opt)),
        "Valor"  : forms.IntegerField(label='Valor',widget=forms.NumberInput),
        "Datas"  : forms.DateField(label='Datas', widget=forms.Select(choices=datas)),
        
    }