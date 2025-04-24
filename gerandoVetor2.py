import re

# Pede o caminho do arquivo para o usuário
caminho_arquivo = input("./exemplos/ADIANTAMENTO ABRIL 2025.txt: ")

# Lista para armazenar os codFuncionarios
funcionarios = []

# Regex para pegar os 5 primeiros dígitos começando com 10
padrao = r'^(1\d{4})'

# Lê e processa o arquivo
try:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            match = re.match(padrao, linha)
            if match:
                codFuncionario = match.group(1)
                funcionarios.append(codFuncionario)

    print("Códigos de funcionários encontrados:")
    print(funcionarios)

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
