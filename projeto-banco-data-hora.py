from datetime import datetime

class Banco:
    def __init__(self):
        self.saldo = 0.0
        self.extrato = []
        self.saques_diarios = 0
        self.transacoes_diarias = 0
        self.limite_transacoes_diarias = 10

    def registrar_transacao(self, tipo, valor):
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.extrato.append(f"{data_hora} - {tipo}: R$ {valor:.2f}")

    def depositar(self, valor):
        if self.transacoes_diarias >= self.limite_transacoes_diarias:
            print("Limite diário de transações atingido.")
        elif valor > 0:
            self.saldo += valor
            self.registrar_transacao("Depósito", valor)
            self.transacoes_diarias += 1
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito deve ser positivo!")

    def sacar(self, valor):
        if self.transacoes_diarias >= self.limite_transacoes_diarias:
            print("Limite diário de transações atingido.")
        elif self.saques_diarios >= 3:
            print("Limite diário de saques atingido.")
        elif valor > 500:
            print("Limite máximo por saque é de R$ 500.00.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self.saldo -= valor
            self.registrar_transacao("Saque", valor)
            self.saques_diarios += 1
            self.transacoes_diarias += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor de saque deve ser positivo!")

    def exibir_extrato(self):
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            print("\nExtrato:")
            for movimentacao in self.extrato:
                print(movimentacao)
            print(f"Saldo atual: R$ {self.saldo:.2f}\n")

    def resetar_saques_diarios(self):
        self.saques_diarios = 0
        self.transacoes_diarias = 0

def menu():
    conta = Banco()

    while True:
        print("\n[d] Depositar")
        print("[s] Sacar")
        print("[e] Extrato")
        print("[q] Sair")
        
        opcao = input("Escolha uma opção: ").lower()

        if opcao == 'd':
            valor = float(input("Digite o valor para depósito: R$ "))
            conta.depositar(valor)

        elif opcao == 's':
            valor = float(input("Digite o valor para saque: R$ "))
            conta.sacar(valor)

        elif opcao == 'e':
            conta.exibir_extrato()

        elif opcao == 'q':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Escolha uma opção válida.")

# Chamando o menu para o cliente
menu()