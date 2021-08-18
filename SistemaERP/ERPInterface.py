from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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

# ----------------------------------------------------------------------------------------------------------------------
    def CadastroBackEnd(self):
        codigoPadrao = '123@h'

        if self.codigoSeguranca.get() == codigoPadrao:
            if len(self.login.get()) <= 20:
                if len(self.password.get()) <= 50:
                    nome = self.login.get().lower()

                    senha = self.password.get()

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
                        messagebox.showinfo('Conexão DB', 'Erro ao conecta ao BD')

                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('insert into cadastro values (%s, %s, %s)',(nome, senha, 1))
                            conexao.commit()
                        messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso.')
                        # Destroio a janela de cadastro/login para que o usuário entre com os novos dados cadastrados
                        self.root.destroy()
                    except:
                        messagebox.showinfo('Cadastro', 'Erro ao cadastrar usuário')
                else:
                    messagebox.showinfo('ERRO', 'Digite a senha com o máximo de 50 caracteres')
            else:
                messagebox.showinfo('ERRO', 'Digite um nome com o máximo de 20 caracteres')
        else:
            messagebox.showinfo('ERRO', 'Código de segurança incorreto')

# ---------------------------------------------------------------------------------------------------------------------
    # Mostra o campo Çhave de SEgurança' ao clicar no botão cadastrar na janela de login
    def Cadastro(self):
        Label(self.root, text='Chave de Segurança').grid(row=3, column=0, padx=5, pady=5)
        self.codigoSeguranca = Entry(self.root)
        self.codigoSeguranca.grid(row=3, column=1, padx=10, pady=5)
        # Efetua o cadastro após preenchido os campos e clicado no botão Confirmar cadastro/Cadastrar
        Button(self.root, text='Confirmar cadastro', width=15, bg='blue1', command=self.CadastroBackEnd).grid(row=4, column=0, columnspan=3, pady=5, padx=10)

#----------------------------------------------------------------------------------------------------------------------
    # Recupera
    def UpdateBackEnd(self):
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

        # Pega todas as linha da Tabela Cadastro e armazena na variável resultado
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from cadastro')
                resultados = cursor.fetchall()
        except:
            print('Erro na consulta')

        # Apaga tudo o que estiver na Treeview para atualização de novos dados.
        self.tree.delete(*self.tree.get_children())

        # Variável para armazenar os dasdos de cada linha/registro do Banco de Dados
        linhaV = []

        # Laço para recuperar os dados do BD, armazenar na variável do tipo lista "linhaV" e exibir na Treview.
        for linha in resultados:
            linhaV.append(linha['id'])
            linhaV.append(linha['nome'])
            linhaV.append(linha['senha'])
            linhaV.append(linha['nivel'])

            # O parametro 'iid=' identifica o registro utilizando o campo especificado neste parametro
            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')

            linhaV.clear()

#----------------------------------------------------------------------------------------------------------------------
    def VisualizarCadastros(self):
        # Cria a janela de visulaização de usuários cadastrados.
        # É como uma instancia de TK(), porém só abre a partir da janela abaixo do TK()/self.root
        # ser fechar a janela self.roo/login, a a janela self.vc/visualizar cadastro, também fecha, pois é Toplevel
        # depende da root.
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar Cadastros')

        # A self.tree/Treeview edita os campos onde os usuários cadastrados serão exibidos
        # Fica dentro da janela self.vc.
        self.tree = ttk.Treeview(self.vc, select="browse", column=("column1", "column2", "column3", "column4"),
                                 show='headings')
        self.tree.column("column1", width=30, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='ID')

        self.tree.column("column2", width=60, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')

        self.tree.column("column3", width=60, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column("column4", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        # Chama a função UpdateBackEnd() para atulizar a janela self.vc/Treeview.
        self.UpdateBackEnd()

        self.vc.mainloop()

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
        botaoEntrar.grid(row=5, column=0, padx=5, pady=5)
        #---
        botaoCadastrar = Button(self.root, text='Cadastrar', bg='Dark Gray', height=1, width=8, command=self.Cadastro)
        botaoCadastrar.grid(row=5, column=1, padx=5, pady=5)
        #--
        botaoViewCadastro = Button(self.root, text='Visualizar Cadastros', bg='White', height=1, width=18,
                                   command=self.VisualizarCadastros)
        botaoViewCadastro.grid(row=6, column=0, columnspan=2, padx=5, pady=8)



        self.root.mainloop()

LoginWindow()