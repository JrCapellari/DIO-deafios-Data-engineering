import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self.contas):
            raise StopIteration
        conta = self.contas[self._index]
        self._index += 1
        return f"""\
        Agência:\t{conta.agencia}
        Número:\t\t{conta.numero}
        Titular:\t{conta.cliente.nome}
        Saldo:\t\tR$ {conta.saldo:.2f}
        """


class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
        else:
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, endereco)
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero, limite=500, limite_saques=3):
        return cls(numero, cliente, limite, limite_saques)

    def sacar(self, valor):
        numero_saques = sum(1 for t in self.historico.transacoes if t["tipo"] == "Saque")
        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        return [t for t in self._transacoes if datetime.strptime(t["data"], "%d-%m-%Y %H:%M:%S").date() == data_atual]


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return wrapper


def menu():
    return input(textwrap.dedent("""\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """))


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if cliente.contas:
        return cliente.contas[0]
    print("\n@@@ Cliente não possui conta! @@@")
    return None


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        valor = float(input("Informe o valor do depósito: "))
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, Deposito(valor))
    else:
        print("\n@@@ Cliente não encontrado! @@@")

@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        valor = float(input("Informe o valor do saque: "))
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, Saque(valor))
    else:
        print("\n@@@ Cliente não encontrado! @@@")

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = recuperar_conta_cliente(cliente)
        if conta:
            print("\n================ EXTRATO ================")
            transacoes = "\n".join(
                f"\n{t['data']}\n{t['tipo']}:\n\tR$ {t['valor']:.2f}"
                for t in conta.historico.gerar_relatorio()
            )
            print(transacoes if transacoes else "Não foram realizadas movimentações")
            print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
            print("==========================================")
    else:
        print("\n@@@ Cliente não encontrado! @@@")

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
    else:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        clientes.append(PessoaFisica(nome, data_nascimento, cpf, endereco))
        print("\n=== Cliente criado com sucesso! ===")

@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente, numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
    else:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes, contas = [], []
    while True:
        opcao = menu()
        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()
