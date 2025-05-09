import PyPDF2

def pdf_para_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as arquivo_pdf:
        leitor = PyPDF2.PdfReader(arquivo_pdf)
        texto = ""

        for pagina in leitor.pages:
            texto += pagina.extract_text() or ''  # Adiciona o texto da página

    with open(txt_path, 'w', encoding='utf-8') as arquivo_txt:
        arquivo_txt.write(texto)

    print(f"Texto extraído e salvo em: {txt_path}")

# Exemplo de uso
pdf_para_txt('ADIANTAMENTO 05 2025_Relação de Salários líquidos.PDF', 'resultado2.txt')
