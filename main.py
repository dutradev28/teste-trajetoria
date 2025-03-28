from tasks.consulta_cep import ConsultaCEP
from tasks.enviar_email import EnviarEmail
from tasks.criar_relatorio import RelatorioPDF

def executar_consulta_ceps():
    """
    Executa a consulta de CEPs usando o driver Selenium.
    """
    try:
        consulta_cep = ConsultaCEP()
        driver = consulta_cep.criar_driver()
        consulta_cep.interar_ceps(driver)
        print("Consulta de CEPs concluída com sucesso.")        
    except Exception as e:
        raise Exception(f"Erro ao consultar CEPs: {e}")
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
            print("Driver encerrado com sucesso.")

def executar_envio_emails():
    """
    Executa o envio de e-mails com base nos dados consultados.
    """
    try:
        envio_email = EnviarEmail()
        envio_email.enviar_emails()
        print("Envio de e-mails concluído com sucesso.")
    except Exception as e:
        raise Exception(f"Erro ao enviar e-mails: {e}")

def executar_criacao_relatorio():
    """
    Gera o relatório PDF consolidado.
    """
    try:
        relatorio = RelatorioPDF()
        relatorio.gerar_relatorio_pdf()
        print("Relatório PDF gerado com sucesso.")
    except Exception as e:
        raise Exception(f"Erro ao gerar relatório PDF: {e}")

def main():
    try:
        executar_consulta_ceps()

        executar_envio_emails()

        executar_criacao_relatorio()

    except Exception as e:
        print(f"Erro ao iniciar o programa: {e}")

if __name__ == "__main__":
    main()