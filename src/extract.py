import pandas as pd
import os

def extract_data(raw_data_path="data/raw"):
    """
    Extrai dados dos arquivos CSV brutos.

    Args:
        raw_data_path (str): Caminho para a pasta onde os arquivos CSV brutos estão localizados.

    Returns:
        tuple: Uma tupla contendo DataFrames do pandas para vendas, clientes e produtos.
               Retorna (None, None, None) se algum arquivo não for encontrado.
    """
    print(f"Iniciando a extração de dados da pasta: {raw_data_path}")

    # O path do script (src/) até a pasta raw/data é '../data/raw'
    # ou se você vai rodar o script da raiz do projeto, é 'data/raw'
    # Vamos assumir que você rodará da raiz do projeto, então o caminho é 'data/raw'
    vendas_path = os.path.join(raw_data_path, "vendas.csv")
    clientes_path = os.path.join(raw_data_path, "clientes.csv")
    produtos_path = os.path.join(raw_data_path, "produtos.csv")

    try:
        df_vendas = pd.read_csv(vendas_path)
        print(f"Arquivo '{os.path.basename(vendas_path)}' lido com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{vendas_path}' não foi encontrado. Verifique o caminho.")
        df_vendas = None
    except Exception as e:
        print(f"ERRO ao ler '{vendas_path}': {e}")
        df_vendas = None

    try:
        df_clientes = pd.read_csv(clientes_path)
        print(f"Arquivo '{os.path.basename(clientes_path)}' lido com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{clientes_path}' não foi encontrado. Verifique o caminho.")
        df_clientes = None
    except Exception as e:
        print(f"ERRO ao ler '{clientes_path}': {e}")
        df_clientes = None

    try:
        df_produtos = pd.read_csv(produtos_path)
        print(f"Arquivo '{os.path.basename(produtos_path)}' lido com sucesso.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{produtos_path}' não foi encontrado. Verifique o caminho.")
        df_produtos = None
    except Exception as e:
        print(f"ERRO ao ler '{produtos_path}': {e}")
        df_produtos = None

    return df_vendas, df_clientes, df_produtos

if __name__ == "__main__":
    # Quando este script é executado diretamente, ele testa a função extract_data
    # O caminho 'data/raw' é relativo à raiz do projeto quando executado de lá.
    df_vendas_raw, df_clientes_raw, df_produtos_raw = extract_data()

    if df_vendas_raw is not None:
        print("\n--- Dados Brutos de Vendas (primeiras 5 linhas) ---")
        print(df_vendas_raw.head())
        print(f"Total de linhas em vendas: {len(df_vendas_raw)}")
        print("\n--- Informações de Vendas ---")
        df_vendas_raw.info()

    if df_clientes_raw is not None:
        print("\n--- Dados Brutos de Clientes (primeiras 5 linhas) ---")
        print(df_clientes_raw.head())
        print(f"Total de linhas em clientes: {len(df_clientes_raw)}")
        print("\n--- Informações de Clientes ---")
        df_clientes_raw.info()

    if df_produtos_raw is not None:
        print("\n--- Dados Brutos de Produtos (primeiras 5 linhas) ---")
        print(df_produtos_raw.head())
        print(f"Total de linhas em produtos: {len(df_produtos_raw)}")
        print("\n--- Informações de Produtos ---")
        df_produtos_raw.info()

    if df_vendas_raw is None or df_clientes_raw is None or df_produtos_raw is None:
        print("\nAlguns arquivos não foram carregados. Verifique os caminhos e os nomes dos arquivos.")