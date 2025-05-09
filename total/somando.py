def somar_valores_txt(caminho_entrada, caminho_saida):
    total = 0.0
    valores_formatados = []
    contador = 0

    with open(caminho_entrada, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

        # Remove quebras de linha e espaços
        conteudo = conteudo.replace('\n', '').replace(' ', '')

        # Separa os valores
        valores = conteudo.split(';')

        for i, valor in enumerate(valores, start=1):
            if valor == '':
                continue  # Ignora valores vazios no final
            try:
                # Corrige formato: remove pontos e troca vírgula por ponto
                valor_limpo = valor.replace('.', '').replace(',', '.')
                numero = float(valor_limpo)
                total += numero
                contador += 1
                valores_formatados.append(f"{numero:.2f}")
            except ValueError:
                raise ValueError(f"Valor inválido na posição {i}: '{valor}'")

    # Grava os valores formatados em um novo arquivo
    with open(caminho_saida, 'w', encoding='utf-8') as saida:
        saida.write(';'.join(valores_formatados))

    print(f"Total de valores somados: {contador}")
    print(f"Total somado: R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Arquivo gerado com valores limpos: {caminho_saida}")


# Exemplo de uso
entrada = 'valores_totais.txt'            # Seu arquivo original
saida = 'valores_formatados.txt'  # Arquivo de saída
somar_valores_txt(entrada, saida)
