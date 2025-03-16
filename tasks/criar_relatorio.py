from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
import os
import pandas as pd

class RelatorioPDF:
    def __init__(self):
        load_dotenv()
        self.CSV_PATH_EXTRAIDOS = os.getenv("CSV_PATH_EXTRAIDOS")
        self.PDF_PATH = os.getenv("PDF_PATH")
        self.titulo = "Relatório Consolidado de Endereços"

    def rodape(self, canvas, doc):
        """ Adiciona rodapé com numeração de página """
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        page_num = canvas.getPageNumber()
        text = f"Página {page_num}"
        canvas.drawRightString(540, 20, text)
        canvas.restoreState()

    def gerar_relatorio_pdf(self):
        try:
            df = pd.read_csv(self.CSV_PATH_EXTRAIDOS, encoding="ansi")

            doc = SimpleDocTemplate(
                self.PDF_PATH,
                pagesize=letter,
                rightMargin=30,
                leftMargin=30,
                topMargin=40,
                bottomMargin=40
            )

            elementos = []
            estilos = getSampleStyleSheet()

            titulo_style = ParagraphStyle(
                "TituloCustom",
                parent=estilos["Title"],
                fontSize=16,
                spaceAfter=14,
                alignment=1 
            )

            titulo = Paragraph(self.titulo, titulo_style)
            elementos.append(titulo)
            elementos.append(Spacer(1, 12))

            colunas = ["CEP", "Estado", "Cidade", "Bairro", "Rua", "Numero", "Status Envio"]
            dados = [colunas]

            for _, row in df.iterrows():
                linha = []
                for coluna in colunas:
                    valor = str(row[coluna]).strip() if not pd.isna(row[coluna]) else "N/A"
                    if valor == "N/A":
                        linha.append(Paragraph(f'<para align="center"><font color="red">{valor}</font></para>', estilos["BodyText"]))
                    else:
                        linha.append(Paragraph(f'<para align="center">{valor}</para>', estilos["BodyText"]))
                dados.append(linha)

            largura_pagina = letter[0] - 60
            larguras_colunas = [70, 70, 100, 100, 120, 50, 100]

            tabela = Table(dados, colWidths=larguras_colunas)

            estilo_tabela = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue), 
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke), 
                ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12), 
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige), 
                ("GRID", (0, 0), (-1, -1), 1, colors.black), 
            ])
            tabela.setStyle(estilo_tabela)

            elementos.append(tabela)

            doc.build(elementos, onFirstPage=self.rodape, onLaterPages=self.rodape)
            print(f"Relatório gerado com sucesso: {self.PDF_PATH}")

        except Exception as e:
            raise Exception(f"Erro ao gerar relatório PDF: {e}")
