import re

MesesAno = {
    'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
    'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
    'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
}

with open('blococorrigido.txt', 'r', encoding='utf-8') as file:
    texto = file.read()

# Extrair os blocos
blocos = re.findall(r'(Persona Sql .*?)(?:\n\d{1,3}(?:\.\d{3})*,\d{2})', texto, re.DOTALL)

funcionario_uni = []
diaPagamento = input('Informe o dia de pagamento: ')

for bloco in blocos:
    # Extrair código do condomínio
    match_cond = re.search(r'Empresa\s*:\s*(\d{4})', bloco, re.IGNORECASE)
    cod_condominio = match_cond.group(1) if match_cond else "0000"

    # Extrair data de referência
    match_data = re.search(r'Relação de Salários Líquidos em (\w+) de (\d{4})', bloco)
    if match_data:
        nome_mes = match_data.group(1)
        ano = match_data.group(2)
        numero_mes = MesesAno.get(nome_mes)
        if numero_mes:
            data_formatada = f"{numero_mes.zfill(2)}{ano}"

            # Verifica se o tipo de pagamento aparece no bloco
            tipo_pagamento = "A" if "(Adiant. de Salário)" in bloco else "M"

            # Procurar todos os funcionários no bloco - REGEX ATUALIZADA
            funcionarios = re.findall(
                r'(\d+)\s+-\s+([A-Z\sÇÃÕÉÁÍÚÊÂÔ]+?)\s+\d{3}\.\d{3}\.\d{3}-\d{2}.*?-\s*\d*\s*([\d\.,]+)',
                bloco, re.DOTALL)

            for cod, nome_func, salario in funcionarios:
                # Limpar e formatar os dados
                cod_funcionario = cod.strip().zfill(6)  # Garante 6 dígitos
                nome_funcionario = ' '.join(nome_func.strip().split())
                salario_limpo = salario.replace('.', '').replace(',', '').zfill(12)
                
                funcionario_uni.append({
                    "cod_condominio": cod_condominio,
                    "diaPagamento": diaPagamento,
                    "dataReferencia": data_formatada,
                    "cod_funcionario": cod_funcionario,
                    "nome_funcionario": nome_funcionario,
                    "salario_func": salario.replace('.', '').replace(',', '.'),
                    "tPagamento": tipo_pagamento
                })

def exportar_funcionarios_txt(funcionarios, caminho):
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            for funcionario in funcionarios:
                salario_num = funcionario['salario_func'].replace('.', '').replace(',', '')
                salario_formatado = salario_num.zfill(12)
                linha = (
                    funcionario['cod_condominio'] +
                    funcionario['diaPagamento'] +
                    funcionario['dataReferencia'] +
                    funcionario['cod_funcionario'] +
                    funcionario['nome_funcionario'].ljust(40)[:40] +  # Garante máximo de 40 caracteres
                    salario_formatado +
                    funcionario['tPagamento']
                )
                f.write("1" + linha + '\n')
        print(f'Funcionários exportados com sucesso para: {caminho}')
    except Exception as e:
        print(f'Erro ao exportar: {e}')

# Imprimir resultado para verificação
for f in funcionario_uni:
    print(f"{f['cod_condominio']}{f['diaPagamento']}{f['dataReferencia']}{f['cod_funcionario']}{f['nome_funcionario']}{f['salario_func']}{f['tPagamento']}")

# Definindo o nome do arquivo de saída
caminho = 'tabela.txt'

# Chamando a função
exportar_funcionarios_txt(funcionario_uni, caminho)