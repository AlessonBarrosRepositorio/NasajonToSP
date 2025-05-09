def somar_e_dividir(nome_arquivo):
    total = 0
    
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:  # Ignora linhas vazias
                # Encontra a posição do 'A' no final da linha
                pos_a = linha.rfind('A')
                if pos_a != -1:
                    # Pega os 11 caracteres antes do 'A' (assumindo que são sempre 11 dígitos)
                    valor_str = linha[pos_a-11:pos_a].strip()
                    try:
                        valor = int(valor_str)
                        total += valor
                    except ValueError:
                        print(f"Valor inválido encontrado na linha: {linha}")
    
    resultado = total / 100
    return resultado

# Nome do arquivo (substitua pelo caminho correto se necessário)
nome_arquivo = 'ADIANTAMENTO ABRIL 2025.txt'

# Calcula o resultado
resultado = somar_e_dividir(nome_arquivo)

# Exibe os resultados
print(f"Soma total dos valores: {resultado * 100}")
print(f"Total dividido por 100: {resultado:.2f}")