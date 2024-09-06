import textwrap
from datetime import datetime

# Classe Cliente
class Cliente:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Subclasse PessoaFisica (herança de Cliente)
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, cpf, endereco)

# Classe Conta
class Conta:
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        pass  # Implementação específica em ContaCorrente

    def saldo_conta(self):
        return self.saldo

# Subclasse ContaCorrente (herança de Conta)
class ContaCorrente(Conta):
    LIMITE_SAQUES = 3
    LIMITE = 500

    def __init__(self, numero, agencia, cliente):
        super().__init__(numero, agencia, cliente)
        self.numero_saques = 0

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > self.LIMITE:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.numero_saques += 1
            self.historico.adicionar_transacao(Saque(valor))
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Interface Transacao
class Transacao:
    def registrar(self, conta):
        pass

# Classe Deposito (implementa Transacao)
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

# Classe Saque (implementa Transacao)
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

# Funções de Interface para o Menu
class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente número): ")
        if self.filtrar_usuario(cpf):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        usuario = PessoaFisica(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)
        if not usuario:
            print("\n@@@ Usuário não encontrado, criação de conta encerrada. @@@")
            return
        numero_conta = len(self.contas) + 1
        conta = ContaCorrente(numero_conta, '0001', usuario)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        for conta in self.contas:
            print(f"Agência: {conta.agencia}, C/C: {conta.numero}, Titular: {conta.cliente.nome}")

    def exibir_extrato(self, conta):
        print("\n================ EXTRATO ================")
        if not conta.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in conta.historico.transacoes:
                if isinstance(transacao, Deposito):
                    print(f"Depósito:\tR$ {transacao.valor:.2f}")
                elif isinstance(transacao, Saque):
                    print(f"Saque:\t\tR$ {transacao.valor:.2f}")
        print(f"\nSaldo:\t\tR$ {conta.saldo_conta():.2f}")
        print("==========================================")

# Função Menu
def menu():
    banco = Banco()

    while True:
        opcao = input(textwrap.dedent("""\n
        ================ MENU ================
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nc] Nova conta
        [lc] Listar contas
        [nu] Novo usuário
        [q] Sair
        => """))

        if opcao == 'd':
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("\n@@@ Usuário não encontrado ou não possui conta. @@@")

        elif opcao == 's':
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("\n@@@ Usuário não encontrado ou não possui conta. @@@")

        elif opcao == 'e':
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            if usuario and usuario.contas:
                conta = usuario.contas[0]
                banco.exibir_extrato(conta)
            else:
                print("\n@@@ Usuário não encontrado ou não possui conta. @@@")

        elif opcao == 'nu':
            banco.criar_usuario()

        elif opcao == 'nc':
            banco.criar_conta()

        elif opcao == 'lc':
            banco.listar_contas()

        elif opcao == 'q':
            break

        else:
            print("\n@@@ Operação inválida. Tente novamente. @@@")

menu()
