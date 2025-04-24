import re

# Texto de exemplo (você pode substituir por leitura de arquivo)
with open('resultado.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Expressão regular para capturar os blocos que começam com "Persona"
blocos = re.split(r'(?=Persona\b)', texto)

# Imprime os blocos separando com uma linha em branco, exceto o primeiro
for i, bloco in enumerate(blocos):
    if i > 0:
        print("\n" + "-"*80 + "\n")  # separador opcional visual
    print(bloco.strip())
