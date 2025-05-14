import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re
import PyPDF2

class ValidadorArquivo:
    MESES_ANO = {
        'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
        'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
        'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
    }

    @staticmethod
    def normalizar_nome(nome):
        substituicoes = {
            "Á": "A", "À": "A", "Â": "A", "Ã": "A",
            "É": "E", "Ê": "E", "È": "E",
            "Í": "I", "Ì": "I",
            "Ó": "O", "Ò": "O", "Ô": "O", "Õ": "O",
            "Ú": "U", "Ù": "U", "Ü": "U",
            "Ç": "C",
            "Ñ": "N"
        }
        nome_normalizado = nome.upper()
        for original, substituto in substituicoes.items():
            nome_normalizado = nome_normalizado.replace(original, substituto)
        return nome_normalizado.strip()

    def processar_arquivo(self, input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            texto = f.read()

        blocos = re.split(r'-{80,}', texto)
        
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for bloco in blocos:
                bloco = bloco.strip()
                if not bloco:
                    continue

                cabecalho = re.search(r'^(.*?Página \d+ de \d+\n\(Adiant\. de Salário\))', bloco, re.DOTALL)
                if not cabecalho:
                    cabecalho = re.search(r'^(.*?Página \d+ de \d+)', bloco, re.DOTALL)
                    if not cabecalho:
                        continue
                cabecalho = cabecalho.group(1).strip()

                funcionarios = re.findall(
                    r'(?m)^(\d{6} - .*? \d{3}\.\d{3}\.\d{3}-\d{2} \d{3} \d{4} - \d .*? \d+ - \d)$',
                    bloco
                )

                total = re.search(r'(?s)Conta Salário.*?(\d[\d.]*,\d+)$', bloco)
                total = total.group(1) if total else ""

                f_out.write(f"{cabecalho}\n")
                f_out.write("Conta Salário\n")
                f_out.write("Funcionário CPF Banco Agência Valor Conta\n")
                
                for func in funcionarios:
                    f_out.write(f"{func}\n")
                
                if total:
                    f_out.write(f"{total}\n")
                
                f_out.write("\n" + "-" * 80 + "\n")

    def extrair_dados(self, arquivo_txt, dia_pagamento):
        with open(arquivo_txt, 'r', encoding='utf-8') as file:
            texto = file.read()

        blocos = re.findall(r'(Persona Sql .*?)(?:\n\d{1,3}(?:\.\d{3})*,\d{2})', texto, re.DOTALL)
        funcionarios = []

        for bloco in blocos:
            match_cond = re.search(r'Empresa\s*:\s*(\d{4})', bloco, re.IGNORECASE)
            cod_condominio = match_cond.group(1) if match_cond else "0000"

            match_data = re.search(r'Relação de Salários Líquidos em (\w+) de (\d{4})', bloco)
            if match_data:
                nome_mes = match_data.group(1)
                ano = match_data.group(2)
                numero_mes = self.MESES_ANO.get(nome_mes)
                if numero_mes:
                    data_formatada = f"{numero_mes.zfill(2)}{ano}"
                    tipo_pagamento = "A" if "(Adiant. de Salário)" in bloco else "M"

                    funcionarios_bloco = re.findall(
                        r'(\d+)\s+-\s+([A-Z\sÇÃÕÉÁÍÚÊÂÔ]+?)\s+\d{3}\.\d{3}\.\d{3}-\d{2}.*?-\s*\d*\s*([\d\.,]+)',
                        bloco, re.DOTALL)

                    for cod, nome_func, salario in funcionarios_bloco:
                        cod_funcionario = cod.strip().zfill(6)
                        nome_funcionario = ' '.join(self.normalizar_nome(nome_func).split())
                        salario_limpo = salario.replace('.', '').replace(',', '.')
                        
                        funcionarios.append({
                            "cod_condominio": cod_condominio,
                            "diaPagamento": dia_pagamento,
                            "dataReferencia": data_formatada,
                            "cod_funcionario": cod_funcionario,
                            "nome_funcionario": nome_funcionario,
                            "salario_func": salario_limpo,
                            "tPagamento": tipo_pagamento
                        })
        return funcionarios

    def calcular_total(self, arquivo_saida):
        total = 0
        
        with open(arquivo_saida, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    if linha.endswith('A') or linha.endswith('B'):
                        valor_str = linha[-12:-1].strip()
                        try:
                            valor = int(valor_str)
                            total += valor
                        except ValueError:
                            print(f"Valor inválido encontrado na linha: {linha}")
        
        return total / 100

class EntradaDataPagamento(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.formatar_data)
        self.bind('<FocusIn>', self.mostrar_placeholder)
        self.bind('<FocusOut>', self.mostrar_placeholder)
        self.placeholder = True
        
    def mostrar_placeholder(self, event=None):
        if not self.get() and not self.placeholder:
            self.insert(0, 'DDMMAAAA')
            self.placeholder = True
            self.config(fg='gray')
        elif self.get() == 'DDMMAAAA' and not self.placeholder:
            self.placeholder = True
            self.config(fg='gray')
    
    def formatar_data(self, event):
        if event.keysym in ('BackSpace', 'Delete'):
            return
            
        conteudo = self.get().replace('DDMMAAAA', '').replace('/', '')[:8]
        novo_valor = ''
        
        for i in range(len(conteudo)):
            if i < 8:  # DDMMAAAA - 8 dígitos
                novo_valor += conteudo[i] if i < len(conteudo) else '_'
        
        self.delete(0, tk.END)
        self.insert(0, novo_valor)
        self.placeholder = False
        self.config(fg='black')
        
        posicao_cursor = len(self.get())
        self.icursor(posicao_cursor)
    
    def obter_data_sem_formatacao(self):
        valor = self.get().replace('_', '0')
        return valor if len(valor) == 8 else None

class AplicativoProcessadorArquivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Nasajom para Superlogica")
        self.root.geometry("500x500")
        
        self.caminho_arquivo = tk.StringVar()
        self.caminho_salvar = tk.StringVar()
        self.data_pagamento = tk.StringVar()
        self.validador = ValidadorArquivo()
        
        self.criar_interface()
    
    def criar_interface(self):
        frame_principal = tk.Frame(self.root, padx=20, pady=20)
        frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # Seleção de arquivo
        tk.Label(frame_principal, text="Selecione o arquivo PDF:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        frame_arquivo = tk.Frame(frame_principal)
        frame_arquivo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        tk.Entry(frame_arquivo, textvariable=self.caminho_arquivo, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_arquivo, text="Procurar", command=self.selecionar_arquivo).pack(side=tk.LEFT, padx=(5, 0))
        
        # Data de pagamento
        tk.Label(frame_principal, text="Data completa de pagamento (DDMMAAAA):").grid(row=2, column=0, sticky="w", pady=(10, 5))
        self.entrada_data_pagamento = EntradaDataPagamento(frame_principal, width=12, font=('Arial', 12))
        self.entrada_data_pagamento.grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.entrada_data_pagamento.mostrar_placeholder()
        
        # Botão de processamento
        tk.Button(frame_principal, text="Processar Arquivo", command=self.processar_arquivo, 
                 bg="#4CAF50", fg="white").grid(row=4, column=0, pady=(20, 20))
        
        # Área de status/alertas
        self.rotulo_status = tk.Label(frame_principal, text="", fg="blue", wraplength=400, justify="left")
        self.rotulo_status.grid(row=5, column=0, pady=(0, 20))
        
        # Seleção de pasta para salvar
        tk.Label(frame_principal, text="Salvar resultado final em:").grid(row=6, column=0, sticky="w", pady=(0, 5))
        frame_salvar = tk.Frame(frame_principal)
        frame_salvar.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        tk.Entry(frame_salvar, textvariable=self.caminho_salvar, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_salvar, text="Procurar", command=self.selecionar_pasta).pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão de salvar
        self.botao_salvar = tk.Button(frame_principal, text="Salvar Resultado", command=self.salvar_arquivo, 
                                   state=tk.DISABLED, bg="#2196F3", fg="white")
        self.botao_salvar.grid(row=8, column=0, pady=(10, 0))
    
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(title="Selecione o arquivo PDF", filetypes=[("Arquivos PDF", "*.pdf")])
        if arquivo:
            self.caminho_arquivo.set(arquivo)
    
    def selecionar_pasta(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar resultado como",
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")],
            initialfile="resultado_final.txt"
        )
        if caminho:
            self.caminho_salvar.set(caminho)
    
    def pdf_para_txt(self, pdf_path, txt_path):
        with open(pdf_path, 'rb') as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            texto = ""
            
            for pagina in leitor.pages:
                texto += pagina.extract_text() or ''
        
        with open(txt_path, 'w', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write(texto)
    
    def exportar_para_txt(self, funcionarios, caminho):
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
                        funcionario['nome_funcionario'].ljust(40)[:40] +
                        salario_formatado +
                        funcionario['tPagamento']
                    )
                    f.write("1" + linha + '\n')
            return True
        except Exception as e:
            print(f'Erro ao exportar: {e}')
            return False
    
    def processar_arquivo(self):
        arquivo_pdf = self.caminho_arquivo.get()
        data_pagamento = self.entrada_data_pagamento.obter_data_sem_formatacao()
        
        if not arquivo_pdf:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo PDF.")
            return
        
        if not data_pagamento or len(data_pagamento) != 8:
            messagebox.showerror("Erro", "Por favor, insira uma data completa no formato DDMMAAAA.")
            return
        
        try:
            # Criar pasta temporária
            temp_dir = os.path.join(os.path.dirname(arquivo_pdf), "temp_nasajom")
            os.makedirs(temp_dir, exist_ok=True)
            
            # PASSO 1: Converter PDF para TXT
            self.rotulo_status.config(text="Convertendo PDF para texto...")
            self.root.update()
            
            caminho_txt = os.path.join(temp_dir, "temp_pdf.txt")
            self.pdf_para_txt(arquivo_pdf, caminho_txt)
            
            # PASSO 2: Processar arquivo com validações
            self.rotulo_status.config(text="Validando e corrigindo dados...")
            self.root.update()
            
            caminho_corrigido = os.path.join(temp_dir, "arquivo_corrigido.txt")
            self.validador.processar_arquivo(caminho_txt, caminho_corrigido)
            
            # PASSO 3: Extrair dados
            self.rotulo_status.config(text="Extraindo dados dos funcionários...")
            self.root.update()
            
            dia_pagamento = data_pagamento[:2]  # DD do DDMMAAAA
            self.funcionarios_processados = self.validador.extrair_dados(caminho_corrigido, dia_pagamento)
            
            # PASSO 4: Calcular total
            caminho_final_temp = os.path.join(temp_dir, "temp_resultado.txt")
            self.exportar_para_txt(self.funcionarios_processados, caminho_final_temp)
            total = self.validador.calcular_total(caminho_final_temp)
            
            # Preparar resultado final
            self.caminho_temp_dir = temp_dir
            
            resumo = (f"Processamento concluído!\n\n"
                     f"Total de funcionários processados: {len(self.funcionarios_processados)}\n"
                     f"Valor total calculado: R$ {total:.2f}\n\n"
                     f"Pronto para exportar o resultado.")
            
            self.rotulo_status.config(text=resumo)
            self.botao_salvar.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar arquivo:\n{str(e)}")
            self.rotulo_status.config(text=f"Erro durante o processamento: {str(e)}")

    def salvar_arquivo(self):
        if not hasattr(self, 'funcionarios_processados'):
            messagebox.showerror("Erro", "Nenhum dado processado para salvar.")
            return
        
        caminho_completo = self.caminho_salvar.get()
        if not caminho_completo:
            messagebox.showerror("Erro", "Por favor, selecione onde salvar o arquivo.")
            return
        
        try:
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                cod_condominio_atual = None
                primeiro_funcionario = True
                
                for funcionario in self.funcionarios_processados:
                    if cod_condominio_atual != funcionario['cod_condominio']:
                        if not primeiro_funcionario:
                            f.write('\n')
                        cod_condominio_atual = funcionario['cod_condominio']
                        primeiro_funcionario = False
                    
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
            
            if hasattr(self, 'caminho_temp_dir'):
                shutil.rmtree(self.caminho_temp_dir)
            
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_completo}")
            self.botao_salvar.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoProcessadorArquivos(root)
    root.mainloop()