class Banco:
    def __init__(self):
        self.saldo = 0.0
        self.extrato = []
        self.saques_diarios = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito deve ser positivo!")

    def sacar(self, valor):
        if self.saques_diarios >= 3:
            print("Limite diário de saques atingido.")
        elif valor > 500:
            print("Limite máximo por saque é de R$ 500.00.")
        elif valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f}")
            self.saques_diarios += 1
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