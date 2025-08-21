import random
import time
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contas, Pix, Caxinha, Investir, Movimentacao
from .form import Foto
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def Index(request):
    return render(request, 'index.html')




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
        return redirect('Login')

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

def Sair(request):
    auth.logout(request)
    return redirect('Index')

def Dashbord(request):
    if request.user.is_authenticated:
        
        ids = request.user.id
        cliente = Contas.objects.all().filter(Nome = ids)
        Con_Financeiro = Movimentacao.objects.all().filter(Conta = ids)
        Con_pix = Caxinha.objects.all().filter(Nome = ids)
        Con_invest = Investir.objects.all().filter(Nome = ids)
      

        
        context = {'cliente':cliente,'Con_Financeiro':Con_Financeiro,'Con_pix':Con_pix,'Con_invest':Con_invest}
    
        return render(request,'Dashbord.html',context)
    else:
        return redirect('Cadastro')
    
    
#Aqui começla as viwes das funções do banco.
def Deposito(request):
    if request.user.is_authenticated:
        ids = request.user.id
        cliente = Contas.objects.all().filter(Nome = ids)
        if request.method == 'POST':
            Dinheiro = request.POST['Dep']
            for Clin in cliente:
                Clin.Saldo = Clin.Saldo + int(Dinheiro)
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor =float(Dinheiro), Descricao='deposito',Tipo='Entrada')
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
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor = 100, Descricao= 'Pagamento', Tipo = 'saida')
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
            Dinheiro = request.POST['Valor']
            
            Cliente_rec = Contas.objects.all().filter(Conta=Numero_conta)
            for Clin in Cliente_rec:
                Clin.Saldo = Clin.Saldo + int(Dinheiro)
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor =float(Dinheiro), Descricao='Trasferencia',Tipo='Entrada')
            Clin.save()
            Gra_dinheiro.save()
            
            for Clin_T in cliente_Transf:
                Clin_T.Saldo = Clin_T.Saldo - int(Dinheiro)
                Gra_dinheiro = Movimentacao.objects.create(Conta = Clin_T.Nome,Valor =float(Dinheiro), Descricao='Trasferencia',Tipo='Saida')
            Clin_T.save()
            Gra_dinheiro.save()
            
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
            Dinheiro = request.POST['Valor']

            Chave_rec = get_object_or_404(Pix,Chave = Chave)
            print(f'Chave_receber {Chave_rec}')
            if Chave_rec == None:
                return redirect('Confirmar_pix')
            else:
                Cliente_rec = Contas.objects.all().filter(Nome = Chave_rec.Nome)
                Cliente_env = Contas.objects.all().filter(Nome = ids)
                for Clin in Cliente_rec:
                    Clin.Saldo = Clin.Saldo + int(Dinheiro)
                    Gra_dinheiro = Movimentacao.objects.create(Conta = Clin.Nome,Valor =float(Dinheiro), Descricao='Pix',Tipo='Entrada')
                Clin.save()
                Gra_dinheiro.save()
                
                for Clin_env in Cliente_env:
                    Clin_env.Saldo = Clin_env.Saldo - int(Dinheiro)
                    Gra_dinheiro = Movimentacao.objects.create(Conta = Clin_env.Nome,Valor =float(Dinheiro), Descricao='Pix',Tipo='saida')
                Clin_env.save()
                Gra_dinheiro.save()

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
            Dinheiro = request.POST['Valor']
            for Cli in Nome_cli:
                if Cli.Saldo >= int(Dinheiro):
                    Caixa = Caxinha.objects.create(Nome = Cli.Nome, Caxinha=Nome_caxinha, Valor = int(Dinheiro), Datas = tep)
                    Cli.Saldo = Cli.Saldo-int(Dinheiro)
                    Gra_dinheiro = Movimentacao.objects.create(Conta = Cli.Nome,Valor =float(Dinheiro), Descricao='Caixinha',Tipo='saida')
            Caixa.save()
            Cli.save()
            Gra_dinheiro.save()
            return redirect('Dashbord')
    else:
        return redirect('Login')
    

def Caixinha_deposito(request):
    if request.user.is_authenticated:
        ids = request.user.id
        tep = datetime.date.today()
        clin_ = Contas.objects.get(Nome=ids)
        if request.method == 'POST':
            nome_caixinha = request.POST['Caixinha']
            print(nome_caixinha)
            valor = request.POST['Valor']
            Depositar_Caxinha = Caxinha.objects.all().filter(id = nome_caixinha)
            clin_.Saldo = clin_.Saldo - int(valor)
            clin_.save()
            for Dep in Depositar_Caxinha:
                Dep.Valor = Dep.Valor + int(valor)
                Dep.Datas = tep
                Dep.save()
            return redirect('Dashbord')


def Retirada(request,id):
    if request.user.is_authenticated:
        ids = request.user.id
        caixa_ret = Caxinha.objects.get(id = id)
        Nome_cli = Contas.objects.get(Nome =ids)
        Nome_cli.Saldo = Nome_cli.Saldo + caixa_ret.Valor
        Nome_cli.save()
        caixa_ret.delete()
        return redirect('Dashbord')
def Invest(request):
    if request.user.is_authenticated:
        temp = datetime.date.today()
        ids = request.user.id
        Nome_cli = Contas.objects.all().filter(Nome = ids)
        if request.method == 'POST':
            Inv = request.POST['Tipo']
            Dinheiro = request.POST['Valor']
            Post = request.POST['Porcentagem']
            Datas = request.POST['Datas']
            Ano = f'{temp.day}/{temp.month}/{temp.year + int(Datas)}'
            Ano_final = datetime.datetime.strptime(Ano,'%d/%m/%Y')
            for Cli in Nome_cli:
                if Cli.Saldo >= int(Dinheiro):
                    Cli.Saldo = Cli.Saldo - int(Dinheiro)
                    Gra_dinheiro = Movimentacao.objects.create(Conta = Cli.Nome,Valor =float(Dinheiro), Descricao='Investimento',Tipo='Saida')
            Cli.save()
            Invt = Investir.objects.create(Nome = Cli.Nome,Invest = Inv,Valor = int(Dinheiro),Porcetagem=Post,Datas = Ano_final)
            Invt.save()
            Gra_dinheiro.save()
            return redirect('Dashbord')
    else:
        return redirect('Login')
    
    
def Grafico(request):
    if request.user.is_authenticated:
        ids = request.user.id
        gaf = Contas.objects.all().filter(Nome=id)
        dados = {gaf:'gad'}
        return render(request,'Graficos.html',dados)
        