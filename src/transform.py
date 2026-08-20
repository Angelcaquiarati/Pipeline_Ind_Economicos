# src/transform.py - VERSÃO FINAL TESTADA
import pandas as pd
from datetime import datetime

def transform_dolar(df):
    """
    Padroniza e enriquece os dados do Dólar
    """
    if df.empty:
        return df
    
    # Criar colunas derivadas
    df['data_coleta'] = datetime.now().strftime('%Y-%m-%d')
    df['spread'] = df['venda'] - df['compra']
    df['variacao_percentual'] = ((df['venda'] - df['compra']) / df['compra']) * 100
    
    # Renomear colunas
    df = df.rename(columns={
        'data': 'timestamp',
        'compra': 'dolar_compra',
        'venda': 'dolar_venda'
    })
    
    # Garantir colunas corretas
    colunas_necessarias = ['timestamp', 'data_coleta', 'moeda', 'dolar_compra', 
                          'dolar_venda', 'maximo', 'minimo', 'spread', 'variacao_percentual']
    
    for col in colunas_necessarias:
        if col not in df.columns:
            df[col] = None
    
    return df[colunas_necessarias]

def transform_indicadores(df, tipo):
    """
    Padroniza dados de Selic ou IPCA
    """
    if df.empty:
        return df
    
    # Criar DataFrame com estrutura fixa
    dados = {
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'data_coleta': [datetime.now().strftime('%Y-%m-%d')],
        'indicador': [tipo],
        'valor': [float(df['valor'].iloc[0]) if not df.empty and 'valor' in df.columns else 0.0],
        'fonte': ['BCB'],
        'detalhes': [str(df['detalhes'].iloc[0]) if not df.empty and 'detalhes' in df.columns else None]
    }
    
    df_resultado = pd.DataFrame(dados)
    return df_resultado

if __name__ == "__main__":
    from extract import extract_selic, extract_ipca
    
    print("Testando transformação de indicadores...")
    
    df_selic = extract_selic()
    if not df_selic.empty:
        df_trans = transform_indicadores(df_selic, 'Selic')
        print("\n✅ Selic transformada:")
        print(df_trans)
        print(f"Colunas: {list(df_trans.columns)}")
        print(f"Tipos: {df_trans.dtypes}")