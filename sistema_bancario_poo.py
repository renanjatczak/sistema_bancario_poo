import os
import sys

# Limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

class Usuario:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

class Conta:
    def __init__(self, numero_conta, usuario):
        self.agencia = '0001'
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""
        self.saques_diarios = 0

def obter_contas_disponiveis(contas):
    return [conta.numero_conta for conta in contas]

def deposito(valor, contas):
    for i, conta in enumerate(contas, start=1):
        print(f"{i}. Conta número: {conta.numero_conta}")
    escolha_conta = int(input("Escolha a conta para depósito: ")) - 1
    if 0 <= escolha_conta < len(contas):
        conta_escolhida = contas[escolha_conta]
        if valor > 0:
            conta_escolhida.saldo += valor
            conta_escolhida.extrato += f"Depósito: +R${valor:.2f}\n"
            print(f"Depósito de R${valor:.2f} realizado com sucesso na conta número {conta_escolhida.numero_conta}.")
        else:
            print("Valor de depósito deve ser positivo.")
    else:
        print("Conta Inexistente.")

def saque(valor, contas, LIMITE_SAQUES, LIMITE_SAQUE_VALOR):
    for i, conta in enumerate(contas, start=1):
        print(f"{i}. Conta número: {conta.numero_conta}")
    escolha_conta = int(input("Escolha a conta para saque: ")) - 1
    if 0 <= escolha_conta < len(contas):
        conta_escolhida = contas[escolha_conta]
        if conta_escolhida.saques_diarios < LIMITE_SAQUES:
            if valor > 0:
                if valor <= LIMITE_SAQUE_VALOR:
                    if valor <= conta_escolhida.saldo:
                        conta_escolhida.saldo -= valor
                        conta_escolhida.extrato += f"Saque: -R${valor:.2f}\n"
                        conta_escolhida.saques_diarios += 1
                        print(f"Saque de R${valor:.2f} realizado com sucesso na conta número {conta_escolhida.numero_conta}.")
                    else:
                        print("Saldo insuficiente para saque.")
                else:
                    print(f"O valor máximo para saque é R${LIMITE_SAQUE_VALOR:.2f}.")
            else:
                print("Valor de saque deve ser positivo.")
        else:
            print(f"Limite de 3 saques diários atingido para a conta número {conta_escolhida.numero_conta}.")
    else:
        print("Conta Inexistente.")

def exibir_extrato(contas):
    for i, conta in enumerate(contas, start=1):
        print(f"{i}. Conta número: {conta.numero_conta}")
    escolha_conta = int(input("Escolha a conta para extrato: ")) - 1
    if 0 <= escolha_conta < len(contas):
        conta_escolhida = contas[escolha_conta]
        print("\n--- Extrato ---")
        if conta_escolhida.extrato:
            print(conta_escolhida.extrato)
        else:
            print("Nenhuma operação realizada.")
        print(f"Saldo atual da conta número {conta_escolhida.numero_conta}: R${conta_escolhida.saldo:.2f}")
    else:
        print("Conta Inexistente.")

def transferencia(contas):
    for i, conta in enumerate(contas, start=1):
        print(f"{i}. Conta número: {conta.numero_conta}")
    escolha_conta_origem = int(input("Escolha a conta de origem para transferência: ")) - 1
    escolha_conta_destino = int(input("Escolha a conta de destino para transferência: ")) - 1
    valor = float(input("Digite o valor a ser transferido: "))
    if 0 <= escolha_conta_origem < len(contas) and 0 <= escolha_conta_destino < len(contas):
        conta_origem = contas[escolha_conta_origem]
        conta_destino = contas[escolha_conta_destino]
        if valor > 0 and valor <= conta_origem.saldo:
            conta_origem.saldo -= valor
            conta_destino.saldo += valor
            conta_origem.extrato += f"Transferência para conta {conta_destino.numero_conta}: -R${valor:.2f}\n"
            conta_destino.extrato += f"Transferência da conta {conta_origem.numero_conta}: +R${valor:.2f}\n"
            print("Transferência realizada com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")
    else:
        print("Conta Inexistente.")

def cadastrar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Usuário com este CPF já cadastrado.")
            return usuarios
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Digite o endereço (logradouro - nº - bairro - cidade/UF): ")
    usuarios.append(Usuario(nome, cpf, data_nascimento, endereco))
    print("Usuário cadastrado com sucesso.")
    return usuarios

def cadastrar_conta(contas, usuarios, numero_conta):
    cpf = input("Digite o CPF do usuário: ")
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario.cpf == cpf:
            usuario_encontrado = usuario
            break
    if not usuario_encontrado:
        print("Usuário não encontrado.")
        return contas, numero_conta
    for conta in contas:
        if conta.usuario == usuario_encontrado:
            print("Este usuário já possui uma conta cadastrada.")
            return contas, numero_conta
    nova_conta = Conta(numero_conta, usuario_encontrado)
    contas.append(nova_conta)
    usuario_encontrado.contas.append(nova_conta)
    print("Conta cadastrada com sucesso.")
    return contas, numero_conta + 1

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        usuario = conta.usuario
        print(f"Agência: {conta.agencia} - Número da Conta: {conta.numero_conta} - Usuário: {usuario.nome} - CPF: {usuario.cpf}")

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(f"Nome: {usuario.nome} - CPF: {usuario.cpf} - Endereço: {usuario.endereco}")
        if usuario.contas:
            print("Contas:")
            for conta in usuario.contas:
                print(f"- Conta número: {conta.numero_conta}")
        else:
            print("Nenhuma conta cadastrada para este usuário.")

def main():
    usuarios = []
    contas = []
    numero_conta = 1

    LIMITE_SAQUES = 3
    LIMITE_SAQUE_VALOR = 500.0

    while True:
        limpar_tela()
        print("\n--- Menu Inicial ---")
        print("1. Cadastros")
        print("2. Serviços Bancários")
        print("3. Sair")

        opcao_menu_inicial = input("Escolha uma opção: ")

        if opcao_menu_inicial == '1':
            while True:
                limpar_tela()
                print("\n--- Menu Cadastros ---")
                print("1. Cadastrar Usuário")
                print("2. Cadastrar Conta")
                print("3. Listar Contas")
                print("4. Usuários Cadastrados")
                print("5. Voltar para o menu anterior")

                opcao_cadastros = input("Escolha uma opção: ")

                if opcao_cadastros == '1':
                    usuarios = cadastrar_usuario(usuarios)
                elif opcao_cadastros == '2':
                    contas, numero_conta = cadastrar_conta(contas, usuarios, numero_conta)
                elif opcao_cadastros == '3':
                    listar_contas(contas)
                elif opcao_cadastros == '4':
                    listar_usuarios(usuarios)
                elif opcao_cadastros == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

        elif opcao_menu_inicial == '2':
            while True:
                limpar_tela()
                print("\n--- Menu Serviços Bancários ---")
                print("1. Depósito")
                print("2. Saque")
                print("3. Extrato")
                print("4. Transferência")
                print("5. Voltar para o menu anterior")

                opcao_servicos_bancarios = input("Escolha uma opção: ")

                if opcao_servicos_bancarios in ['1', '2', '3', '4'] and not contas:
                    print("Nenhuma conta cadastrada.")
                    input("Pressione Enter para continuar...")
                    continue

                if opcao_servicos_bancarios == '1':
                    valor_deposito = float(input("Digite o valor a ser depositado: "))
                    deposito(valor_deposito, contas)
                elif opcao_servicos_bancarios == '2':
                    valor_saque = float(input("Digite o valor a ser sacado: "))
                    saque(valor_saque, contas, LIMITE_SAQUES, LIMITE_SAQUE_VALOR)
                elif opcao_servicos_bancarios == '3':
                    exibir_extrato(contas)
                elif opcao_servicos_bancarios == '4':
                    transferencia(contas)
                elif opcao_servicos_bancarios == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

        elif opcao_menu_inicial == '3':
            while True:
                limpar_tela()
                print("Deseja realmente sair?")
                print("1. Sim")
                print("2. Não")
                opcao_sair = input("Escolha uma opção: ")
                if opcao_sair == '1':
                    print("Saindo do Programa...")
                    input("Pressione Enter para encerrar...")
                    sys.exit()
                elif opcao_sair == '2':
                    print("Voltando para o Menu Inicial...")
                    input("Pressione Enter para continuar...")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                    input("Pressione Enter para continuar...")
                    continue

        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
