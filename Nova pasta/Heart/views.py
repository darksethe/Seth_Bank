import random
import time
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contas, Pix, Caxinha, Investir, Movimentacao
from .form import Foto
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def Cadatro(request):
    if request.method == 'POST':
        Nome = request.POST['Nome']
        Email = request.POST['Email']
        Senha = request.POST['Senha']
        Senha_1 = request.POST['Senha_1']
        Fotos = request.FILES['foto']
        Conta = random.randrange(10000, 60000, 3)
        
        forms = Foto(request.POST,request.FILES)
        if forms.is_valid():
            test = request.FILES['foto']

        if User.objects.filter(email=Email).exists():
            print('Email ja cadastrado')
        
        if Senha != Senha_1:
            print('senha nao confere')

        user = User.objects.create_user(username=Nome,email=Email, password=Senha)
        user.save()

        conta = Contas.objects.create(Nome = user,Conta=Conta,Saldo = 0, Img=test)
        conta.save()
        return redirect('Dashbord')

    else:
        forms = Foto()

    return render(request, 'Cadastro.html',{'forms':forms})



def Login(request):
    if request.method == 'POST':
        Email = request.POST['Email']
        Senha = request.POST['Senha']
        if Email ==  ' ' or Senha == '':
            return redirect('Login')
        if User.objects.filter(email=Email).exists():
            nome = User.objects.filter(email=Email).values_list('username',flat=True).get()
            user = auth.authenticate(request,username=nome,password=Senha)
            if user is not None:
                auth.login(request,user)
                return redirect('Dashbord')
    return render(request,'Login.html')


def Dashbord(request):
    if request.user.is_authenticated:
        
        ids = request.user.id
        cliente = Contas.objects.all().filter(Nome = ids)
        Gran_Dinhero = Movimentacao.objects.all().filter(Conta = ids)
        dados_ag = {}
      

        
        context = {'cliente':cliente}
    
        return render(request,'Dashbord.html',context)
    else:
        return redirect('Cadastro')
    
    
#Aqui começla as viwes das funções do banco.
def Deposito(request):
    if request.user.is_authenticated:
        ids = request.user.id
        cliente = Contas.objects.all().filter(Nome = ids)
        if request.method == 'POST':
            Valor = request.POST['Dep']
            for Clin in cliente:
                Clin.Saldo = Clin.Saldo + int(Valor)
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor =Clin.Saldo)
                time.sleep(5)
                Clin.save()
                Gra_dinheiro.save()
                
            return redirect('Dashbord')
    else:
        return redirect('Login')
    

def Pagar(request):
    if request.user.is_authenticated:
        ids = request.user.id
        cliente = Contas.objects.all().filter(Nome = ids)
        
        if request.method == 'POST':
            Boleto = request.POST['Boleto']
            for Clin in cliente:
                Clin.Saldo = Clin.Saldo - 100
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor =Clin.Saldo)
                time.sleep(10)
                Clin.save()
                Gra_dinheiro.save()
            return redirect('Dashbord')
    else:
        return redirect('Login')
    

def Confirmar(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Numero_conta = request.POST['Conta']
            Valor = request.POST['Trasf']
            Vars = Valor
            Cliente_receber = Contas.objects.all().filter(Conta = Numero_conta)
            context = {'Cliente':Cliente_receber,'Vars':Vars}
            
            return render(request,'Confirmar.html',context)
    else:
        return redirect('Dashbord')
    

def Transferir(request):
    if request.user.is_authenticated:
        ids = request.user.id
        cliente_Transf = Contas.objects.all().filter(Nome = ids)
        if request.method == 'POST':
            Numero_conta = request.POST['Trasf']
            Valor = request.POST['Valor']
            
            Cliente_rec = Contas.objects.all().filter(Conta=Numero_conta)
            for Clin in Cliente_rec:
                Clin.Saldo = Clin.Saldo + int(Valor)
            Clin.save()
            
            for Clin_T in cliente_Transf:
                Clin_T.Saldo = Clin_T.Saldo - int(Valor)
            Clin_T.save()
            
            return redirect('Dashbord')
    else:
        return redirect('Login')
    
    
def Criar_pix(request):
    if request.user.is_authenticated:
        ids = request.user.id
        Nome_cli = get_object_or_404(User, pk = ids)
        if request.method == 'POST':
            Chave = request.POST['Chave']
            Pix_criar = Pix.objects.create(Nome = Nome_cli, Chave = Chave)
            Pix_criar.save()
            
            return redirect('Dashbord')
    else:
        return redirect('Login')
    

def Confirmar_pix(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Chave = request.POST['Chave']
            Valor = request.POST['Valor']
            Vars = Valor
            Chave_recb = get_object_or_404(Pix,Chave = Chave)
            context = {'Chave_recb':Chave_recb,'Vars':Vars}
            
            return render(request,'Pix.html',context)
    else:
        return redirect('Dashbord')

def Transferir_pix(request):
    if request.user.is_authenticated:
        ids = request.user.id
        if request.method == 'POST':
            Chave = request.POST['Chave']
            Valor = request.POST['Valor']

            Chave_rec = get_object_or_404(Pix,Chave = Chave)
            print(f'Chave_receber {Chave_rec}')
            if Chave_rec == None:
                return redirect('Confirmar_pix')
            else:
                Cliente_rec = Contas.objects.all().filter(Nome = Chave_rec.Nome)
                Cliente_env = Contas.objects.all().filter(Nome = ids)
                for Clin in Cliente_rec:
                    Clin.Saldo = Clin.Saldo + int(Valor)
                Clin.save()
                
                for Clin_env in Cliente_env:
                    Clin_env.Saldo = Clin_env.Saldo - int(Valor)
                Clin_env.save()

                return redirect('Dashbord')               
    else:
        return redirect('Login')
    

def Caxinhas(request):
    if request.user.is_authenticated:
        tep = datetime.date.today()
        ids = request.user.id
        Nome_cli = Contas.objects.all().filter(Nome = ids)
        if request.method =='POST':
            Nome_caxinha = request.POST['Nome_caxinha']
            Valor = request.POST['Valor']
            for Cli in Nome_cli:
                if Cli.Saldo >= int(Valor):
                    Caixa = Caxinha.objects.create(Nome = Cli.Nome, Caxinha=Nome_caxinha, Valor = int(Valor), Datas = tep)
                    Cli.Saldo = Cli.Saldo-int(Valor)
            Caixa.save()
            Cli.save()
            return redirect('Dashbord')
    else:
        return redirect('Login')
    
    
def Invest(request):
    if request.user.is_authenticated:
        temp = datetime.date.today()
        ids = request.user.id
        Nome_cli = Contas.objects.all().filter(Nome = ids)
        if request.method == 'POST':
            Inv = request.POST['Tipo']
            Valor = request.POST['Valor']
            Post = request.POST['Porcentagem']
            Datas = request.POST['Datas']
            Ano = f'{temp.day}/{temp.month}/{temp.year + int(Datas)}'
            Ano_final = datetime.datetime.strptime(Ano,'%d/%m/%Y')
            for Cli in Nome_cli:
                if Cli.Saldo >= int(Valor):
                    Cli.Saldo = Cli.Saldo - int(Valor)
            Cli.save()
            Invt = Investir.objects.create(Nome = Cli.Nome,Invest = Inv,Valor = int(Valor),Porcetagem=Post,Datas = Ano_final)
            Invt.save()
            return redirect('Dashbord')
    else:
        return redirect('Login')
    
    
def Grafico(request):
    if request.user.is_authenticated:
        ids = request.user.id
        gaf = Contas.objects.all().filter(Nome=id)
        dados = {gaf:'gad'}
        return render(request,'Graficos.html',dados)
        