def somar_e_dividir(nome_arquivo):
    total = 0
    
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:  # Ignora linhas vazias
                # Verifica se a linha termina com 'A' ou 'B'
                if linha.endswith('A') or linha.endswith('B'):
                    # Pega os 11 caracteres antes do último caractere
                    valor_str = linha[-12:-1].strip()  # -12 até -1 (excluindo o último caractere)
                    try:
                        valor = int(valor_str)
                        total += valor
                    except ValueError:
                        print(f"Valor inválido encontrado na linha: {linha}")
    
    resultado = total / 100
    return resultado

# Nome do arquivo (substitua pelo caminho correto se necessário)
nome_arquivo = 'tabela.txt'

# Calcula o resultado
resultado = somar_e_dividir(nome_arquivo)

# Exibe os resultados
#print(f"Soma total dos valores: {resultado * 100}")
print(f"Total dividido por 100: {resultado:.2f}")