import re

def separar_blocos_por_persona(texto):
    blocos = re.split(r'(?=Persona\b)', texto)
    blocos = [bloco.strip() for bloco in blocos if bloco.strip()]
    return blocos

def exportar_blocos_para_txt(blocos, caminho_arquivo):
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            for bloco in blocos:
                f.write(bloco + '\n\n' + '-'*80 + '\n\n')
        print(f'✅ Blocos exportados com sucesso para: {caminho_arquivo}')
    except Exception as e:
        print(f'❌ Erro ao exportar: {e}')

# Leitura do texto original
with open('resultado2.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Separa os blocos
blocos_persona = separar_blocos_por_persona(texto)

# Mostra os blocos no terminal (opcional)
for bloco in blocos_persona:
    print(bloco)
    print('\n' + '-'*80 + '\n')

# Solicita ao usuário o caminho e nome do arquivo
caminho_arquivo = input("Digite o caminho e nome do arquivo para salvar (ex: C:/meus_blocos.txt): ")

# Exporta para o caminho informado
exportar_blocos_para_txt(blocos_persona, caminho_arquivo)