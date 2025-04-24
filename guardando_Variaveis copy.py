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
"""

# Extrair os blocos
blocos = re.findall(r'(Persona Sql .*?)(?:\n\d{1,3}(?:\.\d{3})*,\d{2})', texto, re.DOTALL)

funcionarios = []

for bloco in blocos:
    # Extrair o nome do mês e o ano
    match_data = re.search(r'Relação de Salários Líquidos em (\w+) de (\d{4})', bloco)
    if match_data:
        nome_mes = match_data.group(1)
        ano = match_data.group(2)
        numero_mes = MesesAno.get(nome_mes)
        if numero_mes:
            data_formatada = f"{numero_mes.zfill(2)}{ano}"
            funcionarios.append({"dataReferencia": data_formatada})

# Imprimir o resultado
for funcionario in funcionarios:
    print(funcionario["dataReferencia"])