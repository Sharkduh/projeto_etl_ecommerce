import pandas as pd
import os

def load_data(df_transformed, processed_data_path="data/processed"):
    """
    Carrega o DataFrame transformado para um arquivo CSV na pasta de dados processados.

    Args:
        df_transformed (pd.DataFrame): O DataFrame já limpo e transformado.
        processed_data_path (str): Caminho para a pasta onde os dados processados serão salvos.
    """
    print(f"\nIniciando a carga dos dados processados para: {processed_data_path}")

    # Garante que o diretório de destino exista
    os.makedirs(processed_data_path, exist_ok=True)

    output_file = os.path.join(processed_data_path, "ecommerce_dados_processados.csv")

    try:
        # Salva o DataFrame como CSV
        # index=False evita que o pandas escreva o índice do DataFrame como uma coluna no CSV
        df_transformed.to_csv(output_file, index=False)
        print(f"Dados processados salvos com sucesso em: {output_file}")
    except Exception as e:
        print(f"ERRO ao salvar os dados processados: {e}")

if __name__ == "__main__":
    # IMPORTANTE: Para testar o 'load.py' diretamente, ele precisa dos dados transformados.
    # Vamos importar as funções de 'extract.py' e 'transform.py' para simular o pipeline completo.
    from extract import extract_data
    from transform import transform_data

    print("Simulando o pipeline completo para teste de carga...")

    # 1. Extração
    df_vendas_raw, df_clientes_raw, df_produtos_raw = extract_data()

    if df_vendas_raw is not None and df_clientes_raw is not None and df_produtos_raw is not None:
        # 2. Transformação
        df_transformed, aggregated_data = transform_data(df_vendas_raw, df_clientes_raw, df_produtos_raw)

        # 3. Carga
        if df_transformed is not None:
            load_data(df_transformed)
            print("\nPipeline ETL completo (Extração -> Transformação -> Carga) executado com sucesso!")
        else:
            print("Não foi possível carregar os dados. O DataFrame transformado está vazio ou nulo.")
    else:
        print("Não foi possível carregar os dados. A extração não foi bem-sucedida para todos os arquivos.")