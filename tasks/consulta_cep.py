import os
import re
import pandas as pd
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ConsultaCEP:
    
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
            raise Exception(f"Erro ao carregar arquivo .env {e}")
        
    def criar_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--enable-unsafe-swiftshader")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--log-level=3")            
            chrome_options.add_experimental_option("useAutomationExtension", False)  
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            return driver
        except Exception as e:
            raise Exception(f"Erro ao criar webdriver: {e}")
        
    def consultar_cep(self, driver, cep):        
        try:
            print(f"Iniciando consulta para o cep: {cep}")
            
            driver.get(self.LINK_CONSULTACEP)
            
            input_cep = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH_INPUT_CEP))
            )
            input_cep.send_keys(cep)
            
            btn_buscar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_BTN_BUSCAR))
            )
            btn_buscar.click()
            
            if self.cep_invalido(driver):
                raise ValueError(f"CEP {cep} inválido! Buscando próximo...")            
            print(f"CEP {cep} buscado com sucesso!")            
        except Exception as e:
            raise Exception(f"Erro ao realizar consulta CEP: {e}")
        
    def extrair_dados(self, driver, cep):
        try:
            estado = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_ESTADO))
            ).text.strip() 
                        
            cidade = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_CIDADE))
            ).text.strip()
            
            bairro = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_BAIRRO))
            ).text.strip()
            
            rua = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CSS_RUA))
            ).text.strip()
            rua_limpa, numero = self.limpar_rua(rua)
            
            dados_cep = {
                "CEP": cep,
                "Estado": estado,
                "Cidade": cidade,
                "Bairro": bairro,
                "Rua": rua_limpa,
                "Numero": numero
            }
            
            self.salvar_em_csv(dados_cep)
            
            print(f"Dados extraídos para o CEP {cep}:")
            print(f"Estado: {estado}")
            print(f"Cidade: {cidade}")
            print(f"Rua: {rua_limpa}")
            print(f"Número: {numero}")
            
        except Exception as e:
            raise Exception(f"Erro ao extrair os dados do CEP: {e}")
    
    
    def interar_ceps(self, driver):
    
        try:
            print(f"Iniciando leitura do arquivo CSV: {self.CSV_PATH}")
            
            df = pd.read_csv(self.CSV_PATH)
            
            if 'CEP' not in df.columns:
                raise ValueError("O Arquivo CSV deve conter a coluna CEP.")
            
            for index, row in df.iterrows():
                
                cep_original = str(row['CEP']).strip()
                cep = cep_original.replace("-", "").replace(".", "").replace(" ", "")
                try:
                    print(f"\nProcessando linha {index + 1}: CEP {cep}")
                    
                    self.consultar_cep(driver, cep)
                    self.extrair_dados(driver, cep)
                except ValueError as ve:
                    print(ve)
                except Exception as e:
                    print(f"Erro ao processar o CEP {cep}: {e}")
        
        except FileNotFoundError:
            print(f"Arquivo CSV não encontrado: {self.CSV_PATH}")
        except pd.errors.EmptyDataError:
            print("O arquivo CSV está vazio.")
        except pd.errors.ParserError:
            print("Erro ao analisar o arquivo CSV. Verifique o formato do arquivo.")
        except Exception as e:
            print(f"Erro ao processar o arquivo CSV: {e}")
            
    def salvar_em_csv(self, dados_cep):        
        try:
            os.makedirs("docs", exist_ok=True)

            try:
                df = pd.read_csv(self.CSV_PATH_EXTRAIDOS, encoding="ansi")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["CEP", "Estado", "Cidade", "Bairro", "Rua", "Numero"])

            novo_dado = pd.DataFrame([dados_cep])
            df = pd.concat([df, novo_dado], ignore_index=True)

            df.to_csv(self.CSV_PATH_EXTRAIDOS, index=False, encoding="ansi")

            print(f"Dados salvos no arquivo CSV: {self.CSV_PATH_EXTRAIDOS}")

        except Exception as e:
            raise Exception(f"Erro ao salvar os dados no arquivo CSV: {e}")
        
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
            raise Exception(f"Erro ao processar o texto da rua: {e}")
                
    def cep_invalido(self, driver):        
        try:
            cep_invalido = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, self.XPATH_CEP_INVALIDO))
            )
            return cep_invalido.is_displayed()
        except:
            return False 