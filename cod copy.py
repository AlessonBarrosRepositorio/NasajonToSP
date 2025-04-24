import re

caminho_arquivo = input("cole aqui caminho.txt: ")
funcionarios = []

# Regex com largura fixa no nome (até 40 caracteres)
padrao = r'^(1\d{4})(\d{8})(\d{6})(\d{6})(.{1,40})(0\d{12})([A-Z]?)\s*'

try:
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            match = re.match(padrao, linha)
            if match:
                codCondominio = match.group(1)
                data_de_pagamento = match.group(2)
                mes_referencia = match.group(3)
                cod_Funcionario = match.group(4)
                nome_funcionario = match.group(5)
                salario = match.group(6)
                tipo_Pagamento = match.group(7)
                funcionarios.append((codCondominio, data_de_pagamento, mes_referencia, cod_Funcionario, nome_funcionario, salario, tipo_Pagamento))

    for cod, dataPG, dataRef, codFun, nomeF, salario, tipo_Pagamento in funcionarios:
        print(f"codFuncionario: {cod} | data_de_pagamento: {dataPG} | data_de_referencia: {dataRef} | cod_Funcionario: {codFun} | nome: {nomeF} | salario: {salario} | tipo_pagamento: {tipo_Pagamento}")

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
