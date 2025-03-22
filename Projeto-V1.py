import sqlite3
from pathlib import Path

# Definindo o caminho do banco
ROOT_PATH = Path(__file__).parent
conexao = sqlite3.connect(ROOT_PATH / "AvaliacaoDB.sqlite")
cursor = conexao.cursor()

cursor.execute("PRAGMA foregn_Keys = ON;")

#criando as tabelas do banco
cursor.execute(
    "CREATE TABLE IF NOT EXISTS cliente ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
    "nome TEXT,"
    "data_nascimento TEXT,"
    "altura INTEGER,"
    "sexo TEXT,"
    "cpf TEXT NOT NULL)"
)
conexao.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS avaBio ("
    "num_ava INTEGER PRIMARY KEY AUTOINCREMENT,"
    "cpf TEXT NOT NULL,"
    "peso TEXT,"
    "massa TEXT,"
    "bodyfat TEXT,"
    "idade_corp TEXT,"
    "gord_visc TEXT,"
    "tmb TEXt,"
    "data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
    "FOREIGN KEY (cpf) REFERENCES cliente (cpf))"
)
conexao.commit()

class Cliente:
    def __init__(self, nome, data_nasci, altura, sexo, cpf):
        self.nome = nome
        self.data_nasci = data_nasci
        self.altura = altura
        self.sexo = sexo
        self.cpf = cpf
    
    def __str__(self):
        return f"nome {self.nome}, Data de Nascimento: {self.data_nasci}, Altura: {self.altura}, Sexo: {self.sexo}, CPF: {self.cpf}"

class Avaliacao:
    def __init__(self, id_user, cpf):
        self.id_user = id_user
        self.cpf = cpf

    def ava_dobras(self):
        pass

    def ava_medidas(self):
        pass

    def ava_bio(self, conexao, cursor, peso, bf, massa, idade_corp, imc, g_visc, tmb):
        self.peso = peso
        self.bf = bf
        self.massa = massa
        self.idade = idade_corp
        self.imc = imc
        self.gvisc = g_visc
        self.tmb = tmb
        cursor.execute(
            "INSERT INTO avaBio (cpf, peso, massa, bodyfat, idade_corp, gord_visc, tmb)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)", (self.cpf, self.peso, self.massa, self.bf, self.idade, self.gvisc, self.tmb)
        )
        conexao.commit()
        print(f"\n Avaliação Bioimpedandica criada para o cliente {self.cpf}.")

class Operacao:
    def __init__(self):
        self.conexao = sqlite3.connect(ROOT_PATH / "AvaliacaoDB.sqlite")
        self.cursor = self.conexao.cursor()

    def buscar_cpf(self, cpf):
        cursor.execute("SELECT cpf FROM cliente WHERE cpf=?",(cpf,))
        return cursor.fetchone() is not None
    
    def buscar_cliente(self, cpf):
        cursor.execute("SELECT id FROM cliente WHERE cpf=?", (cpf,))
        return cursor.fetchone()

    def criar_user(self):
        print("\n" + "=" * 30)
        print("Criar novo cliente: ")
        print("\n" + "=" * 30)
        cpf_user = input("Informe o CPF (somente números): ")
        if self.buscar_cpf(cpf_user):
            print("CPF já cadastrado, confira os dados e tente novamente.")
            return
        nome_user = input("Informe o nome do Cliente: ")
        data_nac = input("Informe a data de nascimento(Formato: xx/xx/xxxx): ")
        altura = input("Informe a altura em centímetros: ")
        sexo = input("Informe o sexo (masculino ou feminino): ")
        cursor.execute(
            "INSERT INTO cliente (nome, data_nascimento, altura, sexo, cpf)"
            "VALUES (?, ?, ?, ? , ?)", (nome_user, data_nac, altura, sexo, cpf_user)
        )
        conexao.commit()
        print("Cliente criado.")
    
    def criar_bio(self):
        print("\n" + "=" * 30)
        print("Criar nova avaliação BioImpedância: ")
        print("\n" + "=" * 30)
        cpf_user = input("Informe o CPF (somente números): ")
        if not self.buscar_cpf(cpf_user):
            print("Cliente não encontrado. Verifique o CPF e tente novamente.")
            return
        id_user = self.buscar_cliente(cpf_user)
        peso = input("Informe o peso registrado na balança: ")
        bf = input("Informe o percentua de gordura (BF): ")
        massa = input("Informe a massa muscular: ")
        idade_corp = input("Informe a idade corporal: ")
        imc = input("Informe o IMC: ")
        g_visc = input("Informe a gordura Visceral: ")
        tmb = input("Informe a Taxa Metabólica Corporal: ")
        #instanciando a classe
        conta = Avaliacao(id_user, cpf_user)
        conta.ava_bio(self.conexao, self.cursor, peso, bf, massa, idade_corp, imc, g_visc, tmb)
    
    def menu(self):
        print("\n" + "=" * 30)
        print("Bem vindo ao sistema de Avaliação Física")
        print("=" * 30)
        print("1 - Avaliação BioImpedância")
        print("2 - Avaliação Dobras")
        print("3 - Avaliação Medidas Corporais")
        print("4 - Criar novo cliente")
        print("5 - Sair")

    def main(self):
        while True:
            self.menu()
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                self.criar_bio()
            elif opcao == "2": # Implementar
                self.ava_dobras()
            elif opcao == "3": # Implementar
                self.ava_medida()
            elif opcao == "4":
                self.criar_user()
            elif opcao == "5":
                print("Saindo do sistema")
                self.fechar_conexão()
                conexao.close()
                break
            else:
                print("Opção inválida, favor selecionar uma opção válida.")

    def fechar_conexão(self):
        conexao.close()
        print("Conexão com o banco fechada.")


if __name__ == "__main__":
   operacao = Operacao()
   operacao.main()
  
    
