# Projeto de Automação: Consulta de CEP e Geração de Relatórios

Este projeto automatiza a consulta de informações de CEPs (Estado, Cidade, Bairro, Rua e Número) em um site específico, envia e-mails com os dados extraídos e gera relatórios consolidados em PDF. Ele utiliza tecnologias como **Python**, **Selenium**, **RPA (TagUI)**, **Mailjet API**, **Pandas** e **Reportlab**.

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Configuração do Ambiente](#configuração-do-ambiente)
4. [Execução do Projeto](#execução-do-projeto)
5. [Melhorias e Limitações](#melhorias-e-limitações)

---

## Visão Geral

O objetivo deste projeto é automatizar tarefas repetitivas relacionadas à consulta de CEPs, envio de e-mails e geração de relatórios. Ele foi desenvolvido para:

1. **Consultar CEPs** em um site específico e extrair informações como Estado, Cidade, Bairro, Rua e Número.
2. **Enviar e-mails** com os dados extraídos para um destinatário específico.
3. **Gerar relatórios consolidados** em PDF com os dados coletados e o status de envio dos e-mails.

---

## Funcionalidades

- **Consulta de CEPs**:
  - Leitura de uma lista de CEPs a partir de um arquivo CSV.
  - Consulta automatizada de cada CEP em um site específico.
  - Extração e armazenamento das informações em um arquivo CSV.
  
- **Envio de E-mails**:
  - Envio de e-mails com os detalhes dos endereços extraídos.
  - Atualização do status de envio (Enviado/Falha) no arquivo CSV.

- **Geração de Relatórios**:
  - Criação de um relatório consolidado em PDF com os dados extraídos e o status de envio.

---

## Configuração do Ambiente

### Pré-requisitos

1. **Python**:
   - Certifique-se de ter o Python 3.x instalado. Você pode baixá-lo em [python.org](https://www.python.org/).

2. **Dependências**:
   - Instale as bibliotecas necessárias executando o seguinte comando:
     ```bash
     pip install -r requirements.txt
     ```

3. **Arquivo `.env`**:
   - Utilize o arquivo `.env_sample` como modelo. Renomeie-o para `.env` e configure as variáveis de ambiente necessárias (por exemplo, credenciais da API Mailjet).

4. **Arquivos de Entrada**:
   - Certifique-se de que o arquivo `cep_listas_30.csv` esteja presente na pasta `docs`.

---

## Execução do Projeto

O projeto pode ser executado de duas formas:

1. **Usando Selenium**:
   - Execute o script `main.py`:
     ```bash
     python main.py
     ```

2. **Usando TagUI**:
   - Execute o script `main_tagUI.py`:
     ```bash
     python main_tagUI.py
     ```

---

## Melhorias e Limitações

### Limitações Identificadas

1. **Dependência do Site**:
   - O script depende da estrutura HTML e dos seletores do site de consulta de CEP. Se o site for atualizado, os seletores precisarão ser revisados.

2. **Tratamento de Erros**:
   - CEPs inválidos são ignorados, mas o script não tenta corrigir erros de formatação (ex.: CEPs com menos de 8 dígitos).

3. **Performance**:
   - A execução pode ser lenta para grandes volumes de CEPs, pois cada consulta é realizada sequencialmente.

### Possíveis Melhorias

1. **Paralelização**:
   - Implementar consultas paralelas para melhorar a performance.

2. **Validação de CEPs**:
   - Adicionar validação adicional para garantir que os CEPs tenham o formato correto antes da consulta.

3. **Suporte a Outros Formatos**:
   - Permitir entrada e saída em outros formatos, como XLSX ou JSON.

4. **Logs Detalhados**:
   - Implementar logs mais detalhados para facilitar a depuração.

---