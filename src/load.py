# src/load.py
from supabase import create_client, Client
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def load_to_supabase(df, table_name):
    """
    Carrega um DataFrame para uma tabela no Supabase
    """
    if df.empty:
        print("⚠️ DataFrame vazio - nada para carregar")
        return False
    
    try:
        # Conectar ao Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas!")
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Converter DataFrame para lista de dicionários
        records = df.to_dict(orient='records')
        
        # Inserir dados
        response = supabase.table(table_name).insert(records).execute()
        
        print(f"✅ {len(records)} registros inseridos na tabela '{table_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados no Supabase: {e}")
        return False

def save_local_backup(df, nome_arquivo):
    """
    Salva backup local dos dados (CSV)
    """
    try:
        # Criar pasta se não existir
        os.makedirs('data/raw', exist_ok=True)
        
        # Salvar com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        caminho = f"data/raw/{nome_arquivo}_{timestamp}.csv"
        
        df.to_csv(caminho, index=False, encoding='utf-8')
        print(f"💾 Backup salvo em: {caminho}")
        
    except Exception as e:
        print(f"⚠️ Erro ao salvar backup: {e}")

if __name__ == "__main__":
    # Teste com dados fictícios
    df_teste = pd.DataFrame([{
        'timestamp': '2024-08-19 14:30:00',
        'data_coleta': '2024-08-19',
        'moeda': 'USD',
        'dolar_compra': 5.45,
        'dolar_venda': 5.48,
        'maximo': 5.52,
        'minimo': 5.42,
        'spread': 0.03,
        'variacao_percentual': 0.55
    }])
    
    print("Testando conexão com Supabase...")
    load_to_supabase(df_teste, 'cambio')