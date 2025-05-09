import re

def extrair_valores_totais(nome_arquivo_entrada, nome_arquivo_saida):
    valores = []
    
    with open(nome_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
        
        for i, linha in enumerate(linhas):
            if linha.strip().startswith('----'):  # Encontrou separador
                # Procura o valor na linha anterior à linha vazia (2 linhas acima)
                if i >= 2:
                    linha_valor = linhas[i-2].strip()  # Pega a linha do valor
                    # Regex melhorada para capturar valores como "2.806,29" ou "706,52"
                    match = re.search(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', linha_valor)
                    if match:
                        valores.append(match.group())
    
    # Gera o arquivo de saída com TODOS os valores, incluindo duplicados
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write('; '.join(valores))
    
    print(f"Total de valores encontrados: {len(valores)}")
    print(f"Valores extraídos (com duplicados): {', '.join(valores)}")
    print(f"Arquivo gerado: {nome_arquivo_saida}")

# Executa o script
extrair_valores_totais('ARQUIVO.txt', 'valores_totais.txt')