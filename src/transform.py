import pandas as pd
import numpy as np
import os # Importe 'os' para usar os.path.join, se necessário para caminhos

# Nota: A função extract_data será importada se este script for executado diretamente,
# ou os DataFrames brutos serão passados se for chamada de outro script.

def transform_data(df_vendas, df_clientes, df_produtos):
    """
    Realiza a transformação e limpeza dos DataFrames brutos.

    Args:
        df_vendas (pd.DataFrame): DataFrame de vendas bruto.
        df_clientes (pd.DataFrame): DataFrame de clientes bruto.
        df_produtos (pd.DataFrame): DataFrame de produtos bruto.

    Returns:
        pd.DataFrame: DataFrame unificado e transformado com todos os dados prontos para análise.
        dict: Um dicionário de DataFrames agregados/resumidos.
    """
    print("\nIniciando a transformação dos dados...")

    # --- 1. Transformações no DataFrame de Vendas (df_vendas) ---

    # 1.1 Tratar a coluna 'Data'
    # Tenta converter para datetime, lidando com diferentes formatos e erros
    # 'coerce' transforma datas inválidas em NaT (Not a Time)
    df_vendas['Data'] = pd.to_datetime(df_vendas['Data'], errors='coerce', dayfirst=False)
    # Remover linhas onde a data é inválida (NaT)
    # df_vendas.dropna(subset=['Data'], inplace=True) # Mantive este comentado pois na fase anterior havíamos resolvido
    # mas se surgir novas datas inválidas, pode descomentar.
    df_vendas = df_vendas.dropna(subset=['Data']).copy() # Usar .copy() para evitar SettingWithCopyWarning
    print("  - Coluna 'Data' em vendas tratada e inválidas removidas.")

    # 1.2 Tratar a coluna 'Preco_Unitario'
    # Substituir vírgula por ponto (para formatos brasileiros)
    df_vendas['Preco_Unitario'] = df_vendas['Preco_Unitario'].astype(str).str.replace(',', '.', regex=False)
    # Converter para numérico, transformando erros em NaN
    df_vendas['Preco_Unitario'] = pd.to_numeric(df_vendas['Preco_Unitario'], errors='coerce')
    # Preencher NaNs com zero (para este caso, zero parece mais lógico para preço inválido)
    df_vendas['Preco_Unitario'].fillna(0, inplace=True)
    # Remover vendas com preço unitário <= 0 (preço inválido)
    df_vendas = df_vendas[df_vendas['Preco_Unitario'] > 0].copy() # Usar .copy()
    print("  - Coluna 'Preco_Unitario' em vendas tratada.")

    # 1.3 Tratar a coluna 'Quantidade'
    df_vendas['Quantidade'] = pd.to_numeric(df_vendas['Quantidade'], errors='coerce')
    df_vendas['Quantidade'].fillna(1, inplace=True) # Preenche NaN com 1 (quantidade mínima razoável)
    # Remover vendas com quantidade <= 0
    df_vendas = df_vendas[df_vendas['Quantidade'] > 0].copy() # Usar .copy()
    print("  - Coluna 'Quantidade' em vendas tratada.")

    # Remover linhas com IDs de produto/cliente ausentes, pois são essenciais para junção
    df_vendas.dropna(subset=['ID_Produto', 'ID_Cliente'], inplace=True)
    print("  - IDs de Produto/Cliente ausentes em vendas removidos.")

    # --- 2. Transformações no DataFrame de Clientes (df_clientes) ---

    # 2.1 Padronizar 'Nome_Cliente' (Capitalizar a primeira letra de cada palavra)
    # Trata NaNs antes de aplicar str.title()
    df_clientes['Nome_Cliente'] = df_clientes['Nome_Cliente'].astype(str).apply(lambda x: x.title() if pd.notnull(x) else x)
    print("  - Coluna 'Nome_Cliente' em clientes padronizada.")

    # 2.2 Padronizar 'Cidade' e 'Estado'
    df_clientes['Cidade'] = df_clientes['Cidade'].astype(str).apply(lambda x: x.title() if pd.notnull(x) else x)
    df_clientes['Estado'] = df_clientes['Estado'].astype(str).apply(lambda x: x.upper() if pd.notnull(x) else x)
    # Tratar inconsistências específicas (ex: "Sao Paulo" -> "São Paulo")
    df_clientes['Cidade'] = df_clientes['Cidade'].replace('Sao Paulo', 'São Paulo')
    print("  - Colunas 'Cidade' e 'Estado' em clientes padronizadas.")

    # Remover clientes com IDs ausentes
    df_clientes.dropna(subset=['ID_Cliente'], inplace=True)
    print("  - IDs de Cliente ausentes removidos.")

    # --- 3. Transformações no DataFrame de Produtos (df_produtos) ---

    # 3.1 Tratar a coluna 'Custo_Unitario'
    df_produtos['Custo_Unitario'] = pd.to_numeric(df_produtos['Custo_Unitario'], errors='coerce')
    df_produtos['Custo_Unitario'].fillna(0, inplace=True) # Preencher NaN com zero
    # Remover produtos com custo unitário negativo (assumindo que não faz sentido)
    df_produtos = df_produtos[df_produtos['Custo_Unitario'] >= 0].copy() # Usar .copy()
    print("  - Coluna 'Custo_Unitario' em produtos tratada.")

    # 3.2 Padronizar 'Categoria'
    df_produtos['Categoria'] = df_produtos['Categoria'].astype(str).apply(lambda x: x.title() if pd.notnull(x) else x)
    # Tratar valores 'null' que viraram 'Null' após .title()
    df_produtos['Categoria'].replace('Null', np.nan, inplace=True) # Converter 'Null' para NaN
    df_produtos['Categoria'].fillna('Outros', inplace=True) # Preencher NaNs com 'Outros'
    # Tratar inconsistências de grafia
    df_produtos['Categoria'] = df_produtos['Categoria'].replace('Eletronicos', 'Eletrônicos')
    print("  - Coluna 'Categoria' em produtos padronizada.")

    # Remover produtos com IDs ausentes
    df_produtos.dropna(subset=['ID_Produto'], inplace=True)
    print("  - IDs de Produto ausentes removidos.")

    # --- 4. Junção (Merge) dos DataFrames ---

    # 4.1 Juntar vendas com produtos
    # Usar um merge de 'left', para manter todas as vendas mesmo que o produto não seja encontrado (ficaria NaN)
    # Mas como removemos IDs ausentes, esperamos que tudo se junte.
    df_final = pd.merge(df_vendas, df_produtos, on='ID_Produto', how='left')
    print("  - Vendas unidas com Produtos.")

    # 4.2 Juntar o resultado com clientes
    df_final = pd.merge(df_final, df_clientes, on='ID_Cliente', how='left')
    print("  - Dados unificados com Clientes.")

    # Preencher NaNs após os merges, caso haja (ex: um ID de cliente/produto que não exista na tabela dimensão)
    # Para clientes/produtos não encontrados, podemos preencher com "Desconhecido"
    df_final['Nome_Cliente'].fillna('Desconhecido', inplace=True)
    df_final['Email'].fillna('desconhecido@email.com', inplace=True)
    df_final['Cidade'].fillna('Desconhecida', inplace=True)
    df_final['Estado'].fillna('XX', inplace=True) # Estado Desconhecido

    df_final['Nome_Produto'].fillna('Produto Desconhecido', inplace=True)
    df_final['Categoria'].fillna('Outros', inplace=True)
    df_final['Custo_Unitario'].fillna(0, inplace=True) # Custo 0 para produto desconhecido
    print("  - Valores ausentes após junção tratados.")


    # --- 5. Cálculo de Novas Colunas ---

    df_final['Valor_Total_Venda'] = df_final['Quantidade'] * df_final['Preco_Unitario']
    df_final['Custo_Total_Venda'] = df_final['Quantidade'] * df_final['Custo_Unitario']
    df_final['Margem_Lucro'] = df_final['Valor_Total_Venda'] - df_final['Custo_Total_Venda']

    # Extrair ano, mês e dia para análises temporais
    df_final['Ano'] = df_final['Data'].dt.year
    df_final['Mes'] = df_final['Data'].dt.month
    df_final['Dia'] = df_final['Data'].dt.day
    print("  - Novas colunas 'Valor_Total_Venda', 'Custo_Total_Venda', 'Margem_Lucro', 'Ano', 'Mes', 'Dia' criadas.")

    # --- 6. Agregações e Resumos (para demonstrar mais conhecimento) ---
    aggregated_data = {}

    # Vendas por Categoria
    vendas_por_categoria = df_final.groupby('Categoria')['Valor_Total_Venda'].sum().sort_values(ascending=False)
    aggregated_data['vendas_por_categoria'] = vendas_por_categoria
    print("  - Agregação: Vendas por Categoria.")

    # Top 5 Clientes por Valor de Venda
    top_clientes = df_final.groupby('Nome_Cliente')['Valor_Total_Venda'].sum().nlargest(5)
    aggregated_data['top_clientes'] = top_clientes
    print("  - Agregação: Top 5 Clientes.")

    # Vendas por Mês e Ano
    vendas_mensais = df_final.groupby(['Ano', 'Mes'])['Valor_Total_Venda'].sum()
    aggregated_data['vendas_mensais'] = vendas_mensais
    print("  - Agregação: Vendas Mensais.")

    print("Transformação de dados concluída.")
    return df_final, aggregated_data

if __name__ == "__main__":
    # Importa a função de extração para usar os dados brutos aqui
    # Garante que o Python possa encontrar 'extract.py' na mesma pasta 'src'
    from extract import extract_data

    # Extrai os dados brutos
    df_vendas_raw, df_clientes_raw, df_produtos_raw = extract_data()

    # Verifica se a extração foi bem-sucedida antes de transformar
    if df_vendas_raw is not None and df_clientes_raw is not None and df_produtos_raw is not None:
        # Transforma os dados
        df_transformed, aggregated_data = transform_data(df_vendas_raw, df_clientes_raw, df_produtos_raw)

        print("\n--- Dados Transformados (primeiras 5 linhas) ---")
        print(df_transformed.head())
        print(f"\nTotal de linhas no DataFrame transformado: {len(df_transformed)}")
        print("\n--- Informações dos Dados Transformados ---")
        df_transformed.info()

        print("\n--- Resumo: Vendas por Categoria ---")
        print(aggregated_data['vendas_por_categoria'])

        print("\n--- Resumo: Top 5 Clientes ---")
        print(aggregated_data['top_clientes'])

        print("\n--- Resumo: Vendas Mensais ---")
        print(aggregated_data['vendas_mensais'])
    else:
        print("\nNão foi possível transformar os dados. A extração não foi bem-sucedida para todos os arquivos.")