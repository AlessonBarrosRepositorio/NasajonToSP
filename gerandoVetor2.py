from datetime import datetime

def ler_dados_arquivo(caminho_arquivo):
    funcionarios = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or len(linha) < 75:
                continue  # Ignora linhas em branco ou incompletas

            linha = linha[1:]  # Ignora o primeiro caractere (ex: o número "1")

            empresa = linha[0:4]                          # 4 caracteres
            data_pagamento_str = linha[4:12]              # 8 caracteres
            mes_referencia = linha[12:18]                 # 6 caracteres
            cod_funcionario = linha[18:24]                # 6 caracteres
            nome_funcionario = linha[24:60].strip()       # 36 caracteres
            salario_str = linha[60:73]                    # 13 caracteres (sem incluir tipo)
            tipo_pagamento = linha[73] if len(linha) > 73 else ''  # 1 caractere

            try:
                data_pagamento = datetime.strptime(data_pagamento_str, "%d%m%Y").strftime("%d/%m/%Y")
            except ValueError:
                data_pagamento = data_pagamento_str

            try:
                salario = int(salario_str) / 100
            except ValueError:
                salario = 0.0

            funcionario = {
                'empresa': empresa,
                'data_pagamento': data_pagamento,
                'mes_referencia': mes_referencia,
                'codigo_funcionario': cod_funcionario,
                'nome': nome_funcionario,
                'salario': salario,
                'tipo_pagamento': tipo_pagamento
            }

            funcionarios.append(funcionario)

    return funcionarios


# Exemplo de uso
if __name__ == "__main__":
    caminho = "./exemplos/ADIANTAMENTO ABRIL 2025.txt"
    lista_funcionarios = ler_dados_arquivo(caminho)

    for f in lista_funcionarios:
        print(f)
