import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv

class EnviarEmail:
    
    def __init__(self):
        try:
            load_dotenv()

            self.SMTP_SERVER = os.getenv("SMTP_SERVER")
            self.SMTP_PORT = int(os.getenv("SMTP_PORT"))  
            self.EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")            
            self.CSV_PATH_EXTRAIDOS = os.getenv("CSV_PATH_EXTRAIDOS")
            self.EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")
            self.MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
            self.MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")            

        except Exception as e:
            raise Exception(f"Erro ao carregar o arquivo .env: {e}")
        
        
    def enviar_emails(self):
        try:
            df = pd.read_csv(self.CSV_PATH_EXTRAIDOS, encoding="ansi")
            
            for index, row in df.iterrows():
                cep = row["CEP"]
                estado = row["Estado"]
                cidade = row["Cidade"]
                bairro = row["Bairro"]
                rua = row["Rua"]
                numero = row["Numero"]
                
               
                assunto = f"Confirmação de Endereço - CEP {cep}"
                corpo_email = self.criar_corpo_email(cep, estado, cidade, bairro, rua, numero)
                
               
                self.enviar_email(self.EMAIL_DESTINATARIO, assunto, corpo_email)
                
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mails: {e}")
        
    def criar_corpo_email(self, cep, estado, cidade, bairro, rua, numero):
                
        corpo_email = f"""
        <html>
            <body>
                <h2>Olá!</h2>
                <p>Gostaríamos de confirmar os detalhes do seu endereço:</p>
                <ul>
                    <li><strong>CEP:</strong> {cep}</li>
                    <li><strong>Estado:</strong> {estado}</li>
                    <li><strong>Cidade:</strong> {cidade}</li>
                    <li><strong>Bairro:</strong> {bairro}</li>
                    <li><strong>Rua:</strong> {rua}</li>
                    <li><strong>Número:</strong> {numero if numero else 'Não informado'}</li>
                </ul>
                <p>Se você identificar algum erro nos dados acima, entre em contato conosco.</p>
                <p>Atenciosamente,<br>Trajetória Consultoria</p>
            </body>
        </html>
        """
        return corpo_email
    
    def enviar_email(self, destinatario, assunto, corpo_email):        
        try:            
            if not self.MAILJET_API_KEY or not self.MAILJET_SECRET_KEY:
                raise ValueError("As variáveis MAILJET_API_KEY e MAILJET_SECRET_KEY não estão definidas no .env")

            url = "https://api.mailjet.com/v3.1/send"

            data = {
                "Messages": [
                    {
                        "From": {"Email": self.EMAIL_REMETENTE, "Name": "Trajetória Consultoria"},
                        "To": [{"Email": destinatario, "Name": "Destinatário"}],
                        "Subject": assunto,
                        "HTMLPart": corpo_email
                    }
                ]
            }

            response = requests.post(
                url,
                auth=(self.MAILJET_API_KEY, self.MAILJET_SECRET_KEY),
                headers={"Content-Type": "application/json"},
                data=json.dumps(data),
            )

            if response.status_code == 200:
                print(f"E-mail enviado para {destinatario} com sucesso!")
            else:
                print(f"Falha ao enviar e-mail para {destinatario}: {response.text}")

        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail para {destinatario}: {e}")