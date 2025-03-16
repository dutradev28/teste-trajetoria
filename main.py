from tasks.consulta_cep import ConsultaCEP 
from tasks.enviar_email import EnviarEmail

def main():
    try:
        consulta_cep = ConsultaCEP()

        driver = consulta_cep.criar_driver()      

        consulta_cep.interar_ceps(driver)
        envio_email = EnviarEmail()
        envio_email.enviar_emails()
        
    except Exception as e:
        print(f"Erro ao iniciar o programa: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("Driver encerrado com sucesso.")

if __name__ == "__main__":
    main()