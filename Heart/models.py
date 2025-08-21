'Senha:123456'
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contas(models.Model):
    Nome = models.ForeignKey(User, on_delete=models.CASCADE)
    Conta = models.IntegerField(blank=True)
    Saldo = models.DecimalField(max_digits=10,  decimal_places=2)

    Img = models.ImageField(upload_to=('imagem/%d/%m/%y'))

    def __int__(self):
        self.Nome


class Movimentacao(models.Model):
    Conta = models.ForeignKey(User, on_delete=models.CASCADE)
    Data = models.DateField(auto_now=True)
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    Descricao = models.CharField(max_length=100)
    Tipo = models.CharField(max_length=10)
    
    def __str__(self):
        return f'{self.Valor} em {self.Data}'
    
    
class Pix(models.Model):
    Nome = models.ForeignKey(User, on_delete=models.CASCADE)
    Chave = models.TextField(max_length=100, blank=True)

    def __int__(self):
        self.Nome

class Caxinha(models.Model):
    Nome = models.ForeignKey(User, on_delete=models.CASCADE)
    Caxinha = models.TextField(max_length=100,blank=True)
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    Datas = models.DateField()

    def __int__(self):
        self.Nome

class Investir(models.Model):
    Nome = models.ForeignKey(User, on_delete=models.CASCADE)
    Invest = models.TextField(max_length=100)
    Valor = models.DecimalField(max_digits=10,decimal_places=2)
    Datas = models.DateField()
    Porcetagem = models.TextField(max_length=10)

    def __int__(self):
        self.Nome
