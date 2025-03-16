import rpa as r
import pandas as pd
import os
import re 
from dotenv import load_dotenv

class ConsultaCEPtagUI():
    def __init__(self):
        try:
            load_dotenv()
            self.LINK_CONSULTACEP = os.getenv("LINK_CONSULTACEP")
            self.XPATH_INPUT_CEP = os.getenv("XPATH_INPUT_CEP")
            self.XPATH_BTN_BUSCAR = os.getenv("XPATH_BTN_BUSCAR")
            self.XPATH_CEP_INVALIDO = os.getenv("XPATH_CEP_INVALIDO")
            self.CSS_ESTADO = os.getenv("CSS_ESTADO")
            self.CSS_CIDADE = os.getenv("CSS_CIDADE")
            self.CSS_BAIRRO = os.getenv("CSS_BAIRRO")
            self.CSS_RUA = os.getenv("CSS_RUA")
            self.CSV_PATH = os.getenv("CSV_PATH")
            self.CSV_PATH_EXTRAIDOS = os.getenv("CSV_PATH_EXTRAIDOS")
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo .env: {e}")

    def consultar_ceps(self):
        try:
            r.init()

            ceps_df = pd.read_csv(self.CSV_PATH, encoding="ansi")

            resultados = []

            for cep in ceps_df['CEP']:
                r.url(self.LINK_CONSULTACEP)

                r.type(self.XPATH_INPUT_CEP, cep)

                r.click(self.XPATH_BTN_BUSCAR)               

                if r.present(self.XPATH_CEP_INVALIDO):
                    resultados.append([cep, "CEP inválido", "", "", "", ""])  
                else:
                    estado = r.read(self.CSS_ESTADO)
                    cidade = r.read(self.CSS_CIDADE)
                    bairro = r.read(self.CSS_BAIRRO)
                    rua = r.read(self.CSS_RUA)

                    rua_limpa, numero = self.limpar_rua(rua)

                    resultados.append([cep, estado, cidade, bairro, rua_limpa, numero])

            r.close()

            resultados_df = pd.DataFrame(resultados, columns=['CEP', 'Estado', 'Cidade', 'Bairro', 'Rua', 'Número'])
            resultados_df.to_csv(self.CSV_PATH_EXTRAIDOS, index=False, encoding='ansi')

            print(f"Processo concluído! Resultados salvos em {self.CSV_PATH_EXTRAIDOS}")

        except Exception as e:
            r.close()  
            raise Exception(f"Erro durante a execução do RPA: {e}")
        
    def limpar_rua(self, rua):        
        try:
            rua_limpa = re.sub(r"(\w+)-\s*", r"\1 ", rua)

            match = re.search(r"\d+\s*a\s*\d+|\d+[/\-\d]*", rua_limpa)
            if match:
                numero = match.group(0)  
                rua_limpa = re.sub(r"\d+\s*a\s*\d+|\d+[/\-\d]*", "", rua_limpa).strip()  
            else:
                numero = ""

            rua_limpa = re.sub(r"\b(de\s*-\s*lado\s*par|até)\b", "", rua_limpa, flags=re.IGNORECASE)

            rua_limpa = re.sub(r"\s+", " ", rua_limpa).strip()
            return rua_limpa, numero

        except Exception as e:
            raise Exception(f"Erro ao limpar a rua: {e}")   