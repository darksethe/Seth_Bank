# 💳 Sistema Bancário em Django

Um sistema estilo **internet banking** desenvolvido com Django, simulando operações financeiras como depósito, pagamento, transferência, PIX, caixinha (poupança) e investimento.

---

## 🚀 Funcionalidades

- Cadastro e login de usuários.
- Conta bancária com número gerado automaticamente.
- Depósitos e pagamentos.
- Transferências entre contas.
- PIX com chave cadastrada.
- Caixinhas (poupança para metas financeiras).
- Investimentos com prazo e rendimento.
- Histórico de movimentações.
- Dashboard financeiro.

---

## 🛠️ Tecnologias Utilizadas
- Python 3
- Django
- SQLite (padrão do Django, pode ser trocado por PostgreSQL/MySQL)
- HTML + CSS (templates)

---

## 📂 Estrutura Principal
- `models.py` → tabelas (conta, movimentação, PIX, caixinha, investimento)
- `views.py` → regras de negócio (cadastro, login, depósito, etc.)
- `urls.py` → rotas da aplicação
- `templates/` → páginas HTML

---

## 📸 Demonstração
![Index](https://github.com/user-attachments/assets/c13322b0-60ca-4bd2-a7e7-1d48db11b675)
![Login](https://github.com/user-attachments/assets/0f74c6e4-488e-4057-bf95-6cc21a1227c2)
![Dashbord](https://github.com/user-attachments/assets/687eaf31-658b-4cc4-97b1-3f67dc1f5659)
![Deposito](https://github.com/user-attachments/assets/aad3017b-76bd-417c-afc5-38b7747611e3)
![Boleto](https://github.com/user-attachments/assets/ae35f153-29b5-4a36-ad0d-d05de89ed495)
![Caixinha](https://github.com/user-attachments/assets/17a058c0-e239-4081-b857-c168a82fc8c3)
![Investimento](https://github.com/user-attachments/assets/70289bb4-015c-4731-bdec-29fdd1a639b4)
![Trasferencia](https://github.com/user-attachments/assets/423fdb03-e80f-49d6-a8c5-d31b6e65847b)
![Pix](https://github.com/user-attachments/assets/4183ae20-5b9b-410c-b597-ce51b7ffe076)








---

## ▶️ Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/sistema-banco-django.git

   cd sistema-banco-django

   pip install -r requirements.txt

   python manage.py migrate

   python manage.py createsuperuser

   python manage.py runserver
´´´




