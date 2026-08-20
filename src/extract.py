# src/extract.py
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def extract_dolar():
    """
    Busca a cotação do Dólar (USD/BRL) da API AwesomeAPI
    Retorna: DataFrame com data e cotação
    """
    try:
        # API pública (não precisa de chave para uso básico)
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extrair dados
        dolar = data['USDBRL']
        df = pd.DataFrame([{
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'moeda': 'USD',
            'compra': float(dolar['bid']),
            'venda': float(dolar['ask']),
            'maximo': float(dolar['high']),
            'minimo': float(dolar['low']),
            'fonte': 'AwesomeAPI'
        }])
        
        print(f"✅ Dólar extraído: R$ {df['compra'].iloc[0]:.2f}")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao extrair Dólar: {e}")
        return pd.DataFrame()

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