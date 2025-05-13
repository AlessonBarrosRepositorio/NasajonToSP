import re

def processar_arquivo(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        texto = f.read()

    blocos = re.split(r'-{80,}', texto)
    
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for bloco in blocos:
            bloco = bloco.strip()
            if not bloco:
                continue

            # Extrai o cabeçalho (incluindo "(Adiant. de Salário)")
            cabecalho = re.search(r'^(.*?Página \d+ de \d+\n\(Adiant\. de Salário\))', bloco, re.DOTALL)
            if not cabecalho:
                cabecalho = re.search(r'^(.*?Página \d+ de \d+)', bloco, re.DOTALL)
                if not cabecalho:
                    continue
            cabecalho = cabecalho.group(1).strip()

            # Extrai TODOS os funcionários (de Conta Corrente e Conta Salário)
            funcionarios = re.findall(
                r'(?m)^(\d{6} - .*? \d{3}\.\d{3}\.\d{3}-\d{2} \d{3} \d{4} - \d .*? \d+ - \d)$',
                bloco
            )

            # Extrai o último valor monetário (total da Conta Salário)
            total = re.search(r'(?s)Conta Salário.*?(\d[\d.]*,\d+)$', bloco)
            total = total.group(1) if total else ""

            # Escreve o bloco formatado
            f_out.write(f"{cabecalho}\n")
            f_out.write("Conta Salário\n")
            f_out.write("Funcionário CPF Banco Agência Valor Conta\n")
            
            for func in funcionarios:
                f_out.write(f"{func}\n")
            
            if total:
                f_out.write(f"{total}\n")
            
            f_out.write("\n" + "-" * 80 + "\n")
# Uso:
processar_arquivo("aqrivoteste.txt", "blococorrigido.txt")