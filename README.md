# 📊 Pipeline ETL de E-commerce com Python e Pandas

Este projeto implementa um pipeline completo de ETL (Extract, Transform, Load) para processar dados de vendas, clientes e produtos de um e-commerce. Desenvolvido em Python, utilizando a poderosa biblioteca Pandas, o pipeline é capaz de extrair dados brutos de arquivos CSV, limpá-los, padronizá-los, enriquecê-los e carregá-los em um formato limpo e unificado, pronto para análise e geração de insights.

## ✨ Visão Geral do Projeto

O objetivo principal deste pipeline é transformar dados desorganizados e inconsistentes em um conjunto de dados limpo e estruturado. Ele simula um cenário real onde as informações de vendas vêm em formatos variados e com erros, necessitando de um tratamento robusto antes de serem utilizadas para tomadas de decisão.

## 🚀 Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Pandas:** Biblioteca essencial para manipulação e análise de dados.
* **Ambiente Virtual (`venv`):** Para gerenciamento de dependências do projeto.
* **CSV:** Formato dos arquivos de entrada e saída.

## 📁 Estrutura do Projeto

A organização do projeto segue uma estrutura modular e clara:


## ⚙️ Como Executar o Pipeline

Siga os passos abaixo para clonar o repositório, configurar o ambiente e executar o pipeline ETL completo:

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/Sharkduh/projeto_etl_ecommerce.git](https://github.com/Sharkduh/projeto_etl_ecommerce.git)
    cd projeto_etl_ecommerce # Navegue para a pasta do projeto
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Se você estiver usando um sistema Debian/Ubuntu e tiver problemas com `venv`, pode ser necessário instalar o pacote `python3-venv` ou `python3.11-venv`:*
    ```bash
    sudo apt update
    sudo apt install python3.11-venv # Ou python3-venv, dependendo da sua versão do Python
    ```
    *Após a instalação do pacote, recrie e ative o ambiente virtual.*

3.  **Instale as Dependências:**
    ```bash
    pip install pandas numpy
    ```
    *(`numpy` é uma dependência de `pandas` e também foi utilizada em `transform.py` para `np.nan`)*

4.  **Execute o Pipeline ETL Completo:**
    ```bash
    python3 src/load.py
    ```
    Este comando executará sequencialmente as etapas de Extração, Transformação e Carga.

## 📊 Resultados e Insights (Exemplos)

Após a execução bem-sucedida do pipeline, um arquivo `ecommerce_dados_processados.csv` será gerado na pasta `data/processed/` contendo os dados limpos, unificados e prontos para análise.

O console também exibirá mensagens de progresso e resumos importantes dos dados transformados, como:

### Exemplo do DataFrame Final Transformado (primeiras linhas):

| ID_Venda | Data       | ID_Produto | Quantidade | Preco_Unitario | ... | Custo_Total_Venda | Margem_Lucro | Ano  | Mes | Dia |
| -------- | ---------- | ---------- | ---------- | -------------- | --- | ----------------- | ------------ | ---- | --- | --- |
| 1        | 2023-01-05 | P001       | 2          | 10.5           | ... | 1600.0            | -1579.0      | 2023 | 1   | 5   |
| 3        | 2023-01-07 | P001       | 3          | 10.0           | ... | 2400.0            | -2370.0      | 2023 | 1   | 7   |
| 7        | 2023-01-11 | P005       | 1          | 30.0           | ... | 400.0             | -370.0       | 2023 | 1   | 11  |
| 9        | 2023-01-13 | P001       | 2          | 10.5           | ... | 1600.0            | -1579.0      | 2023 | 1   | 13  |
| 11       | 2023-01-15 | P008       | 1          | 75.0           | ... | 100.0             | -25.0        | 2023 | 1   | 15  |


## 🚀 Competências Demonstradas

* **Engenharia de Dados (Data Engineering):** Design e implementação de um pipeline ETL de ponta a ponta.
* **Manipulação e Limpeza de Dados (Data Wrangling/Data Cleansing):** Tratamento de inconsistências, nulos, e padronização de formatos.
* **Programação em Python:** Desenvolvimento modular e eficiente de scripts para processamento de dados.
* **Uso de Pandas:** Proficiência na utilização da biblioteca para transformações complexas, junções e agregações de DataFrames.
* **Automação de Processos:** Criação de um fluxo de trabalho automatizado para processamento de dados.
* **Controle de Versão (Git/GitHub):** Gerenciamento e colaboração de código-fonte.

## 🤝 Contribuições

Sinta-se à vontade para abrir issues ou pull requests caso tenha sugestões, melhorias ou queira reportar algum problema.

---
