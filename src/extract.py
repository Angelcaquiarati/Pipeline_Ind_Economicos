# src/extract.py
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def extract_dolar(dias=7):
    """
    Busca a cotação do Dólar (USD/BRL) dos últimos N dias
    Dados REAIS da API AwesomeAPI
    """
    import time
    from datetime import datetime, timedelta
    
    try:
        # Calcular data de início (N dias atrás)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias)
        
        # Formatar datas para a API (YYYYMMDD)
        inicio_str = data_inicio.strftime('%Y%m%d')
        fim_str = data_fim.strftime('%Y%m%d')
        
        print(f"📊 Buscando {dias} dias de dados históricos do Dólar...")
        
        # URL para buscar dados históricos
        url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}?start_date={inicio_str}&end_date={fim_str}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 429:
            print("⚠️ Rate limit da API. Aguardando 10 segundos...")
            time.sleep(10)
            response = requests.get(url, timeout=10)
        
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("⚠️ Nenhum dado retornado pela API")
            return pd.DataFrame()
        
        # Processar os dados - CORRIGIDO!
        registros = []
        for item in data:
            # A API retorna 'create_date' com a data completa
            if 'create_date' in item:
                data_str = item['create_date']
            else:
                # Fallback: usar timestamp
                timestamp = int(item.get('timestamp', 0))
                data_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            registros.append({
                'data': data_str,
                'moeda': 'USD',
                'compra': float(item['bid']),
                'venda': float(item['ask']),
                'maximo': float(item['high']),
                'minimo': float(item['low']),
                'fonte': 'AwesomeAPI'
            })
        
        df = pd.DataFrame(registros)
        
        # Ordenar por data (mais recente primeiro)
        df = df.sort_values('data', ascending=False)
        
        print(f"✅ Dólar: {len(df)} dias REAIS extraídos (último: R$ {df['compra'].iloc[0]:.2f})")
        print(f"   Período: {df['data'].iloc[-1]} até {df['data'].iloc[0]}")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao extrair Dólar: {e}")
        print("📊 Usando dados mockados para teste...")
        
        # Fallback: dados mockados
        registros = []
        hoje = datetime.now()
        for i in range(dias):
            data = hoje - timedelta(days=i)
            valor_base = 5.45 + (i * 0.02)
            registros.append({
                'data': data.strftime('%Y-%m-%d %H:%M:%S'),
                'moeda': 'USD',
                'compra': round(valor_base, 2),
                'venda': round(valor_base + 0.03, 2),
                'maximo': round(valor_base + 0.07, 2),
                'minimo': round(valor_base - 0.03, 2),
                'fonte': 'Mock'
            })
        
        df = pd.DataFrame(registros)
        print(f"✅ Dólar (mock): {len(df)} dias gerados")
        return df

def extract_selic():
    """
    Busca a taxa Selic atual do Banco Central (SGS)
    API pública - série 11 = Selic over
    """
    try:
        # API do BCB - série 11 (Selic)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            # O BCB retorna: [{"data": "01/08/2024", "valor": "10.50"}]
            registro = data[0]
            df = pd.DataFrame([{
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'indicador': 'Selic',
                'valor': float(registro['valor']),
                'fonte': 'BCB'
            }])
            
            print(f"✅ Selic extraída: {df['valor'].iloc[0]:.2f}%")
            return df
        else:
            print("⚠️ Nenhum dado da Selic retornado")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Erro ao extrair Selic: {e}")
        return pd.DataFrame()

def extract_ipca():
    """
    Busca o IPCA acumulado dos últimos 12 meses (BCB)
    Série 433 = IPCA - Variação mensal
    """
    try:
        # API do BCB - série 433 (IPCA mensal)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/12"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data:
            # Calcular acumulado dos últimos 12 meses
            valores = [float(item['valor']) for item in data if item['valor']]
            acumulado = (sum(valores) / len(valores)) if valores else 0
            
            df = pd.DataFrame([{
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'indicador': 'IPCA_12m',
                'valor': round(acumulado, 2),
                'fonte': 'BCB',
                'detalhes': f"Base em {len(valores)} meses"
            }])
            
            print(f"✅ IPCA acumulado extraído: {df['valor'].iloc[0]:.2f}%")
            return df
        else:
            print("⚠️ Nenhum dado do IPCA retornado")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Erro ao extrair IPCA: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Teste rápido
    print("=== Testando extração ===\n")
    
    df_dolar = extract_dolar()
    df_selic = extract_selic()
    df_ipca = extract_ipca()
    
    print("\n=== Resultados ===")
    if not df_dolar.empty:
        print(f"Dólar: R$ {df_dolar['compra'].iloc[0]:.2f}")
    if not df_selic.empty:
        print(f"Selic: {df_selic['valor'].iloc[0]:.2f}%")
    if not df_ipca.empty:
        print(f"IPCA: {df_ipca['valor'].iloc[0]:.2f}%")