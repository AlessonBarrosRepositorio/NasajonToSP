import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import re
import PyPDF2

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
        
        # Variáveis
        self.caminho_arquivo = tk.StringVar()
        self.caminho_salvar = tk.StringVar()
        self.data_pagamento = tk.StringVar()
        
        # Dicionário de meses
        self.meses_ano = {
            "Janeiro": '01', "Fevereiro": '02', "Março": '03', 
            "Abril": '04', "Maio": '05', "Junho": '06',
            "Julho": '07', "Agosto": '08', "Setembro": '09',
            "Outubro": '10', "Novembro": '11', "Dezembro": '12'
        }
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
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
            
            # PASSO 2: Separar blocos por Persona
            self.rotulo_status.config(text="Separando blocos por Persona...")
            self.root.update()
            
            with open(caminho_txt, 'r', encoding='utf-8') as file:
                texto = file.read()
            
            blocos_persona = self.separar_blocos_por_persona(texto)
            
            # PASSO 3: Processar cada bloco e extrair dados
            self.rotulo_status.config(text="Processando dados dos funcionários...")
            self.root.update()
            
            funcionarios = []
            for bloco in blocos_persona:
                funcionarios.extend(self.extrair_dados_funcionarios(bloco, data_pagamento))
            
            # Preparar resultado final
            self.funcionarios_processados = funcionarios
            self.caminho_temp_dir = temp_dir
            
            resumo = (f"Processamento concluído!\n\n"
                     f"Total de funcionários processados: {len(funcionarios)}\n"
                     f"Blocos Persona encontrados: {len(blocos_persona)}\n\n"
                     f"Data de pagamento usada: {data_pagamento}\n"
                     f"Pronto para exportar o resultado.")
            
            self.rotulo_status.config(text=resumo)
            self.botao_salvar.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao processar arquivo:\n{str(e)}")
            self.rotulo_status.config(text=f"Erro durante o processamento: {str(e)}")

    def pdf_para_txt(self, pdf_path, txt_path):
        """Converter PDF para arquivo TXT"""
        with open(pdf_path, 'rb') as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            texto = ""
            
            for pagina in leitor.pages:
                texto += pagina.extract_text() or ''
        
        with open(txt_path, 'w', encoding='utf-8') as arquivo_txt:
            arquivo_txt.write(texto)
    
    def separar_blocos_por_persona(self, texto):
        """Separar o texto em blocos por Persona"""
        blocos = re.split(r'(?=Persona\b)', texto)
        return [bloco.strip() for bloco in blocos if bloco.strip()]
    
    def extrair_dados_funcionarios(self, bloco, data_pagamento):
        """Extrair dados dos funcionários de um bloco Persona"""
        funcionarios = []
        
        # Extrair código do condomínio
        match_cond = re.search(r'Empresa\s*:\s*(\d{4})', bloco)
        cod_condominio = match_cond.group(1) if match_cond else "0000"
        
        # Extrair data de referência (mês e ano)
        match_data = re.search(r'Relação de Salários Líquidos em (\w+) de (\d{4})', bloco)
        if match_data:
            nome_mes = match_data.group(1)
            ano = match_data.group(2)
            numero_mes = self.meses_ano.get(nome_mes, '00')
            
            # Determinar tipo de pagamento
            tipo_pagamento = "A" if "(Adiant. de Salário)" in bloco else "M"
            
            # Extrair dados dos funcionários
            codigos_func = re.findall(r'(\d{6})\s+-', bloco)
            nomes_func = re.findall(r'\d{6}\s+-\s+([A-Z\sÇÃÕÉÁÍÚÊÂÔ]+)\s+\d{3}\.\d{3}\.\d{3}-\d{2}', bloco)
            salarios = re.findall(r'-\s*0\s*([\d\.]+,\d{2})', bloco)
            
            for cod, nome_func, salario in zip(codigos_func, nomes_func, salarios):
                funcionarios.append({
                    "cod_condominio": cod_condominio,
                    "data_pagamento": data_pagamento,
                    "mes_referencia": numero_mes,
                    "ano_referencia": ano,
                    "cod_funcionario": cod,
                    "nome_funcionario": nome_func.strip(),
                    "salario_func": salario,
                    "tPagamento": tipo_pagamento
                })
        
        return funcionarios

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
                    # Verifica se mudou de condomínio
                    if cod_condominio_atual != funcionario['cod_condominio']:
                        if not primeiro_funcionario:
                            f.write('\n')  # Pula linha entre condomínios diferentes
                        cod_condominio_atual = funcionario['cod_condominio']
                        primeiro_funcionario = False
                    
                    salario_num = funcionario['salario_func'].replace('.', '').replace(',', '')
                    salario_formatado = salario_num.zfill(12)
                    linha = (
                        funcionario['cod_condominio'] +
                        funcionario['data_pagamento'] +
                        funcionario['mes_referencia'] +
                        funcionario['ano_referencia'] +
                        funcionario['cod_funcionario'] +
                        funcionario['nome_funcionario'].ljust(40) +
                        salario_formatado +
                        funcionario['tPagamento']
                    )
                    f.write('1'+linha + '\n')
            
            # Limpar pasta temporária
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