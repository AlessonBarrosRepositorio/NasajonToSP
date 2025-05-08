import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import shutil

class EntradaData(tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.formatar_data)
        self.bind('<FocusIn>', self.mostrar_placeholder)
        self.bind('<FocusOut>', self.mostrar_placeholder)
        self.placeholder = True
        
    def mostrar_placeholder(self, event=None):
        if not self.get() and not self.placeholder:
            self.insert(0, '__/__/____')
            self.placeholder = True
            self.config(fg='gray')
        elif self.get() == '__/__/____' and not self.placeholder:
            self.placeholder = True
            self.config(fg='gray')
    
    def formatar_data(self, event):
        if event.keysym in ('BackSpace', 'Delete'):
            return
            
        conteudo = self.get().replace('/', '')[:8]
        novo_valor = ''
        
        for i in range(len(conteudo)):
            if i < 2:
                novo_valor += conteudo[i] if i < len(conteudo) else '_'
            elif i == 2:
                novo_valor += '/' + (conteudo[i] if i < len(conteudo) else '_')
            elif i < 4:
                novo_valor += conteudo[i] if i < len(conteudo) else '_'
            elif i == 4:
                novo_valor += '/' + (conteudo[i] if i < len(conteudo) else '_')
            elif i < 8:
                novo_valor += conteudo[i] if i < len(conteudo) else '_'
        
        self.delete(0, tk.END)
        self.insert(0, novo_valor)
        self.placeholder = False
        self.config(fg='black')
        
        # Posiciona o cursor corretamente
        posicao_cursor = len(self.get())
        if posicao_cursor in (2, 5):
            posicao_cursor += 1
        self.icursor(posicao_cursor)
    
    def obter_data_sem_formatacao(self):
        valor = self.get().replace('/', '').replace('_', '0')
        return valor if len(valor) == 8 else None

class AplicativoProcessadorArquivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Nasajom para Superlogica")
        self.root.geometry("500x450")
        
        # Variáveis
        self.caminho_arquivo = tk.StringVar()
        self.caminho_salvar = tk.StringVar()
        
        # Criar interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        frame_principal = tk.Frame(self.root, padx=20, pady=20)
        frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # Seleção de arquivo
        tk.Label(frame_principal, text="Selecione o arquivo:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        frame_arquivo = tk.Frame(frame_principal)
        frame_arquivo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        tk.Entry(frame_arquivo, textvariable=self.caminho_arquivo, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_arquivo, text="Procurar", command=self.selecionar_arquivo).pack(side=tk.LEFT, padx=(5, 0))
        
        # Data de referência
        tk.Label(frame_principal, text="Data de referência:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.entrada_data = EntradaData(frame_principal, width=12, font=('Arial', 12))
        self.entrada_data.grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.entrada_data.mostrar_placeholder()
        
        # Botão de processamento
        tk.Button(frame_principal, text="Processar Arquivo", command=self.processar_arquivo, 
                 bg="#4CAF50", fg="white").grid(row=4, column=0, pady=(10, 20))
        
        # Área de status/alertas
        self.rotulo_status = tk.Label(frame_principal, text="", fg="blue")
        self.rotulo_status.grid(row=5, column=0, pady=(0, 20))
        
        # Seleção de pasta para salvar
        tk.Label(frame_principal, text="Salvar arquivo processado em:").grid(row=6, column=0, sticky="w", pady=(0, 5))
        frame_salvar = tk.Frame(frame_principal)
        frame_salvar.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        tk.Entry(frame_salvar, textvariable=self.caminho_salvar, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(frame_salvar, text="Procurar", command=self.selecionar_pasta).pack(side=tk.LEFT, padx=(5, 0))
        
        # Botão de salvar
        self.botao_salvar = tk.Button(frame_principal, text="Salvar Arquivo", command=self.salvar_arquivo, 
                                   state=tk.DISABLED, bg="#2196F3", fg="white")
        self.botao_salvar.grid(row=8, column=0, pady=(10, 0))
    
    def selecionar_arquivo(self):
        arquivo = filedialog.askopenfilename(title="Selecione o arquivo")
        if arquivo:
            self.caminho_arquivo.set(arquivo)
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta para salvar")
        if pasta:
            self.caminho_salvar.set(pasta)
    
    def processar_arquivo(self):
        arquivo = self.caminho_arquivo.get()
        data_bruta = self.entrada_data.obter_data_sem_formatacao()
        
        if not arquivo:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo.")
            return
        
        if not data_bruta or len(data_bruta) != 8:
            messagebox.showerror("Erro", "Por favor, insira uma data completa no formato DDMMAAAA.")
            return
        
        try:
            # Converter a data para o formato interno
            dia = int(data_bruta[:2])
            mes = int(data_bruta[2:4])
            ano = int(data_bruta[4:8])
            data_ref = datetime(ano, mes, dia)
            hoje = datetime.now()
            
            # Simular processamento
            tamanho_arquivo = os.path.getsize(arquivo) / 1024  # KB
            nome_arquivo = os.path.basename(arquivo)
            
            # Criar mensagem de alerta
            mensagem = f"Arquivo processado com sucesso!\n\n" \
                       f"Detalhes:\n" \
                       f"- Nome: {nome_arquivo}\n" \
                       f"- Tamanho: {tamanho_arquivo:.2f} KB\n" \
                       f"- Data de referência: {data_ref.strftime('%d/%m/%Y')}\n" \
                       f"- Dias desde a referência: {(hoje - data_ref).days} dias\n" \
                       f"- Data no formato interno: {data_bruta}"
            
            self.rotulo_status.config(text=mensagem)
            self.botao_salvar.config(state=tk.NORMAL)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Data inválida: {str(e)}")
    
    def salvar_arquivo(self):
        origem = self.caminho_arquivo.get()
        pasta_destino = self.caminho_salvar.get()
        
        if not origem:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado para salvar.")
            return
        
        if not pasta_destino:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta para salvar.")
            return
        
        try:
            nome_arquivo = os.path.basename(origem)
            data_bruta = self.entrada_data.obter_data_sem_formatacao()
            caminho_destino = os.path.join(pasta_destino, f"processado_{data_bruta}_{nome_arquivo}")
            
            # Copiar arquivo (simulando processamento)
            shutil.copy2(origem, caminho_destino)
            
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_destino}")
            self.botao_salvar.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar arquivo:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoProcessadorArquivos(root)
    root.mainloop()