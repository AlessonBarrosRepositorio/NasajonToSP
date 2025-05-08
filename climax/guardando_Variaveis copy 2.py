import re

MesesAno = {
    "Janeiro": '1',
    "Fevereiro": '2',
    "Março": '3',
    "Abril": '4',
    "Maio": '5',
    "Junho": '6',
    "Julho": '7',
    "Agosto": '8',
    "Setembro": '9',
    "Outubro": '10',
    "Novembro": '11',
    "Dezembro": '12'
}

texto = """
    Persona Sql INDIK ASSESSORIA IMOBILIARIA LTDA Nasajon Sistemas
CNPJ : 68.619.550/0001-27 Empresa : 0107COND EDIFICIO IBIAPABA
Relação de Salários Líquidos em Março de 2025Página 1 de 80
(Adiant. de Salário)
Conta Salário
Funcionário CPF Banco Agência Valor Conta
000030 - HMENON DE ASSIS 132.157.487-89 237 0135 - 0 935,43 0108936 - 6
000035 - FLAVIO SEVERINO DA SILVA 097.961.567-41 237 0135 - 0 935,43 3919 - 5
000055 - ALEXANDRO CONCEIÇÃO DOS SANTOS 136.257.547-03 237 0135 - 0 935,43 22764 - 1
000056 - MANOEL FERNANDES DA SILVA 082.583.197-01 237 0135 - 0 935,43 23640 - 3
000056 - MANOEL ANDRADE DA SILVA 082.583.192-01 237 0135 - 0 1935,43 23640 - 3
3.741,72

--------------------------------------------------------------------------------

Persona Sql INDIK ASSESSORIA IMOBILIARIA LTDA Nasajon Sistemas
CNPJ : 00.310.553/0001-40 Empresa : 0110COND EDIFICIO ARAÇATUBA
Relação de Salários Líquidos em Janeiro de 2025Página 3 de 80
(Adiant. de Salário)
Conta Salário
Funcionário CPF Banco Agência Valor Conta
000013 - ADALBERTO GOMES DA SILVA 011.806.237-97 237 0135 - 0 706,52 13725 - 1
706,52

--------------------------------------------------------------------------------

Persona Sql INDIK ASSESSORIA IMOBILIARIA LTDA Nasajon Sistemas
CNPJ : 68.696.897/0001-73 Empresa : 0123COND EDIFICIO ITAOCA
Relação de Salários Líquidos em Março de 2026Página 5 de 80
(Adiant. de Salário)
Conta Salário
Funcionário CPF Banco Agência Valor Conta
000001 - MANUEL FORTUNATO DOS SANTOS 075.785.797-38 237 0135 - 0 935,43 2406 - 6
000002 - JOSÉ RONALDO PAULINO DA SILVA 037.848.664-09 237 0135 - 0 935,43 2398 - 1
000030 - WELLINGTON HONORIO DOS SANTOS 185.933.047-96 237 0135 - 0 935,43 21375 - 6
000031 - CARLOS ALBERTO DE SOUSA JATAY 022.964.508-90 237 0135 - 0 935,43 24209 - 8
000033 - EUFRASIO BRITO DA SILVA 768.574.764-20 237 0135 - 0 935,43 27673 - 1
000034 - LUIZ CLAUDIO DA SILVA 971.243.547-49 237 0135 - 0 935,43 32198 - 2
5.612,58

--------------------------------------------------------------------------------

Persona Sql INDIK ASSESSORIA IMOBILIARIA LTDA Nasajon Sistemas
CNPJ : 03.875.685/0001-08 Empresa : 0182COND EDIFICIO URARY
Relação de Salários Líquidos em Março de 2025Página 1 de 2
(Folha)
Conta Salário
Funcionário CPF Banco Agência Valor Conta
000003 - LUIZ CARLOS PEREIRA DA COSTA 821.445.407-72 237 0135 - 0 1.371,66 15892 - 5
000010 - IVONALDO SOARES DO NASCIMENTO 933.403.384-34 237 0135 - 0 737,32 26731 - 7
000012 - JAIRO DA CONCEIÇÃO 073.452.844-25 237 0135 - 0 1.413,27 33223 - 2
3.522,25

--------------------------------------------------------------------------------
"""

# Extrair os blocos
blocos = re.findall(r'(Persona Sql .*?)(?:\n\d{1,3}(?:\.\d{3})*,\d{2})', texto, re.DOTALL)

funcionario_uni = []
diaPagamento = input('Informe o dia de pagemnto')
for bloco in blocos:
    # Extrair código do condomínio
    match_cond = re.search(r'Empresa\s*:\s*(\d{4})', bloco)
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


            # Procurar todos os códigos de funcionários no bloco
            codigos_func = re.findall(r'(\d{6})\s+-', bloco)
            nomes_func = re.findall(r'\d{6}\s+-\s+([A-Z\sÇÃÕÉÁÍÚÊÂÔ]+)\s+\d{3}\.\d{3}\.\d{3}-\d{2}', bloco)
            salarios = re.findall(r'-\s*0\s*([\d\.]+,\d{2})', bloco)
            adiantamentos = re.findall(r'(Adiant. de Salário)', bloco)
            folhas = re.findall(r'(Folha)', bloco)

 

            for cod, nome_func, salario in zip(codigos_func, nomes_func, salarios):
                funcionario_uni.append({
                    "cod_condominio": cod_condominio,
                    "diaPagamento":diaPagamento,
                    "dataReferencia": data_formatada,
                    "cod_funcionario": cod,
                    "nome_funcionario": nome_func.strip(),
                    "salario_func": salario,
                    "tPagamento": tipo_pagamento

                })



# Imprimir resultado
for f in funcionario_uni:

    print(f"{f['cod_condominio']}{f['diaPagamento']}{f['dataReferencia']}{f['cod_funcionario']}{f['nome_funcionario']}{f['salario_func']}{f['tPagamento']}")

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
                    funcionario['nome_funcionario'].ljust(40) +
                    salario_formatado +
                    funcionario['tPagamento']
                )
                f.write(linha + '\n')
        print(f'Funcionários exportados com sucesso para: {caminho}')
    except Exception as e:
        print(f'Erro ao exportar: {e}')

# Definindo o nome do arquivo de saída
caminho = 'tabela.txt'

# Chamando a função
exportar_funcionarios_txt(funcionario_uni, caminho)
