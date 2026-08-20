#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:21:32 2026

@author: data-science
"""

# dashboard/app.py
import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Indicadores Econômicos",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Painel de Indicadores Econômicos")
st.markdown("Dólar, Selic e IPCA - Atualizado diariamente")

# Conectar ao Supabase
@st.cache_resource
def get_supabase():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    return create_client(url, key)

supabase = get_supabase()

# Função para carregar dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    try:
        # Buscar câmbio
        cambio = supabase.table('cambio').select('*').order('timestamp', desc=True).limit(30).execute()
        df_cambio = pd.DataFrame(cambio.data)
        
        # Buscar indicadores
        indicadores = supabase.table('indicadores').select('*').order('timestamp', desc=True).limit(30).execute()
        df_indicadores = pd.DataFrame(indicadores.data)
        
        return df_cambio, df_indicadores
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Carregar dados
df_cambio, df_indicadores = load_data()

# Layout em colunas
col1, col2, col3 = st.columns(3)

# Cards com indicadores atuais
if not df_cambio.empty:
    ultimo_dolar = df_cambio.iloc[0]
    with col1:
        st.metric(
            label="💵 Dólar (Compra)",
            value=f"R$ {ultimo_dolar['dolar_compra']:.2f}",
            delta=f"{ultimo_dolar['variacao_percentual']:.2f}%"
        )

if not df_indicadores.empty:
    df_selic = df_indicadores[df_indicadores['indicador'] == 'Selic']
    df_ipca = df_indicadores[df_indicadores['indicador'] == 'IPCA_12m']
    
    if not df_selic.empty:
        with col2:
            st.metric(
                label="🏦 Taxa Selic",
                value=f"{df_selic.iloc[0]['valor']:.2f}%",
                delta="Meta atual"
            )
    
    if not df_ipca.empty:
        with col3:
            st.metric(
                label="📈 IPCA (12 meses)",
                value=f"{df_ipca.iloc[0]['valor']:.2f}%",
                delta="Acumulado"
            )

# Gráficos
st.subheader("📈 Evolução do Dólar")
if not df_cambio.empty:
    df_cambio_ordenado = df_cambio.sort_values('timestamp')
    
    chart_data = pd.DataFrame({
        'Data': pd.to_datetime(df_cambio_ordenado['timestamp']),
        'Compra': df_cambio_ordenado['dolar_compra'],
        'Venda': df_cambio_ordenado['dolar_venda']
    })
    
    st.line_chart(chart_data.set_index('Data'))

# Tabela histórica
st.subheader("📋 Histórico Completo")
if not df_cambio.empty:
    st.dataframe(
        df_cambio[['timestamp', 'dolar_compra', 'dolar_venda', 'maximo', 'minimo']].head(10),
        use_container_width=True
    )

# Rodapé
st.markdown("---")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("Dados: AwesomeAPI (Dólar) e Banco Central (Selic/IPCA)")