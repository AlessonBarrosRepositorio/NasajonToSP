def ler_dados_arquivo(caminho_arquivo):
    funcionarios = []

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if len(linha) < 75:  # Ignora linhas vazias ou incompletas
                continue

            try:
                empresa = linha[2:6]
                data_pagamento = linha[6:13]       # dia mês ano = 5042025
                mes_referencia = linha[13:19]      # mês e ano = 042025
                cod_funcionario = linha[19:25]
                nome_funcionario = linha[25:61].strip()
                salario_str = linha[61:74]
                tipo = linha[74]

                salario = int(salario_str) / 100  # converte de inteiro para float com 2 casas decimais

                funcionario = {
                    'empresa': empresa,
                    'data_pagamento': data_pagamento,
                    'mes_referencia': mes_referencia,
                    'codigo_funcionario': cod_funcionario,
                    'nome': nome_funcionario,
                    'salario': salario,
                    'tipo_pagamento': tipo
                }

                funcionarios.append(funcionario)

            except ValueError as e:
                print(f"Erro ao processar linha: {linha}")
                print(f"Detalhes do erro: {e}")
                continue  # pula pra próxima linha

    return funcionarios


# Exemplo de uso:
if __name__ == "__main__":
    caminho = "./exemplos/ADIANTAMENTO ABRIL 2025.txt"  # Nome do arquivo .txt
    lista_funcionarios = ler_dados_arquivo(caminho)

    for f in lista_funcionarios:
        print(f)

