from tkinter import *
from tkinter import messagebox
import pymysql

# Cria janela de Administrador
class AdminWindow():
    def __init__(self):
        self.root = Tk()
        self.root.title('ADMINISTRADOR')
        self.root.geometry('500x500')

        self.root.mainloop()

#----------------------------------------------------------------------------------------------------------------------

# Função para Logar no sistema
class LoginWindow():

    # Cria conexão com DB e verifica se o login foi efetuado...
    # Precisa ser declarado no 'command=' do botão Login como 'self.VerificaLogin'
    def VerificaLogin(self):
        autenticado = False
        usuarioMaster = False

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='erp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            # Colocar este print em MessageBox, ao compilar em '.EXE'
            print('Erro ao conectar ao Banco de Dados ERP')

        # Recebe os dados de '__init__(self)
        usuario = self.login.get().lower()
        senha = self.password.get()

        # Pega todas as linha da Tabela Cadastro e armazena na variável resultado
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastro')
                resultados = cursor.fetchall()
        except:
            print('Erro na consulta')

        # Compara os campos das linha da tabela cadastro com o dados inseridos pelo usuário e verifica se é master não
        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuarioMaster = False
                    print(usuarioMaster)
                elif linha['nivel'] == 2:
                    usuarioMaster = True
                    print(usuarioMaster)
                autenticado = True
                break
            else:
                # autenticado continua sendo False
                autenticado = False

        if not autenticado:
            # O primeiro parametro é o título da messagebox e o segundo a mensagem.
            messagebox.showinfo('Login', 'E-mail ou senha invalido')

        if autenticado:
            self.root.destroy()
            if usuarioMaster:
                # Chama/Abre a janela de Administrdor após login efetuado com sucesso como Master.
                AdminWindow()

#----------------------------------------------------------------------------------------------------------------------

    # Cria a Janela do App
    def __init__(self):
        self.root = Tk()
        self.root.title('Login')

        # Nomes dos campos
        Label(self.root, text='Faça o login').grid(row=0, column=0, columnspan=2, padx=7)

        Label(self.root, text='Usuário').grid(row=1, column=0, padx=4)

        Label(self.root, text='Senha').grid(row=2, column=0, padx=4)

        # Instancia o campo de entrada Usuário na variável "self.login"
        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=4, pady=4)

        # instancia o campo de entrada Senha na váriável "self.password"
        self.password = Entry(self.root, show='*')
        self.password.grid(row=2, column=1, padx=4, pady=4)

        # Cria o Botões para logar/entrar, cadastrar e ver cadastros no sistema
        botaoEntrar = Button(self.root, text='Entrar', bg='Dark Gray', height=1, width=8, command=self.VerificaLogin)
        botaoEntrar.grid(row=3, column=0, padx=5, pady=5)
        #---
        botaoCadastrar = Button(self.root, text='Cadastrar', bg='Dark Gray', height=1, width=8, command='')
        botaoCadastrar.grid(row=3, column=1, padx=5, pady=5)
        #--
        botaoViewCadastro = Button(self.root, text='Visualizar Cadastros', bg='White', height=1, width=18, command='')
        botaoViewCadastro.grid(row=4, column=0, columnspan=2, padx=5, pady=8)



        self.root.mainloop()

LoginWindow()