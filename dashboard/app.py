# dashboard/app.py
import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv

# Configuração da página
st.set_page_config(
    page_title="Indicadores Econômicos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Painel de Indicadores Econômicos")
st.markdown("**Dólar, Selic e IPCA** - Atualizado diariamente")

# Carregar variáveis de ambiente
supabase_url = None
supabase_key = None

# 1. Tenta carregar dos secrets do Streamlit Cloud
try:
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    st.caption("🔐 Usando secrets do Streamlit Cloud")
except:
    pass

# 2. Se não encontrou nos secrets, tenta do .env
if not supabase_url or not supabase_key:
    try:
        load_dotenv()
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        st.caption("🔐 Usando .env local")
    except:
        pass

# Verifica se encontrou as credenciais
if not supabase_url or not supabase_key:
    st.error("❌ Credenciais do Supabase não configuradas!")
    st.stop()

# Conectar ao Supabase
@st.cache_resource
def get_supabase():
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Supabase: {e}")
        st.stop()

supabase = get_supabase()

# Carregar dados do Supabase
@st.cache_data(ttl=3600)
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
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Carregar dados e mostrar
df_cambio, df_indicadores = load_data()

if df_cambio.empty:
    st.warning("⚠️ Nenhum dado encontrado no Supabase.")

# Layout do dashboard
col1, col2, col3 = st.columns(3)

if not df_cambio.empty:
    ultimo_dolar = df_cambio.iloc[0]
    with col1:
        st.metric(
            label="💵 Dólar (Compra)",
            value=f"R$ {float(ultimo_dolar['dolar_compra']):.2f}",
            delta=f"{float(ultimo_dolar.get('variacao_percentual', 0)):.2f}%"
        )

if not df_indicadores.empty:
    df_selic = df_indicadores[df_indicadores['indicador'] == 'Selic']
    df_ipca = df_indicadores[df_indicadores['indicador'] == 'IPCA_12m']
    
    if not df_selic.empty:
        with col2:
            st.metric(
                label="🏦 Taxa Selic",
                value=f"{float(df_selic.iloc[0]['valor']):.2f}%",
                delta="Meta atual"
            )
    
    if not df_ipca.empty:
        with col3:
            st.metric(
                label="📈 IPCA (12 meses)",
                value=f"{float(df_ipca.iloc[0]['valor']):.2f}%",
                delta="Acumulado"
            )

# Gráfico
st.subheader("📈 Evolução do Dólar")

if not df_cambio.empty:
    df_cambio_ordenado = df_cambio.sort_values('timestamp')
    chart_data = pd.DataFrame({
        'Data': pd.to_datetime(df_cambio_ordenado['timestamp']),
        'Compra': df_cambio_ordenado['dolar_compra'].astype(float),
        'Venda': df_cambio_ordenado['dolar_venda'].astype(float)
    })
    st.line_chart(chart_data.set_index('Data'))

# Tabela histórica
st.subheader("📋 Histórico Completo")
tab1, tab2 = st.tabs(["💵 Câmbio", "📊 Indicadores"])

with tab1:
    if not df_cambio.empty:
        st.dataframe(df_cambio[['timestamp', 'dolar_compra', 'dolar_venda']].head(10))
    else:
        st.info("Nenhum dado disponível na tabela 'cambio'.")

with tab2:
    if not df_indicadores.empty:
        st.dataframe(df_indicadores[['timestamp', 'indicador', 'valor', 'fonte']].head(10))
    else:
        st.info("Nenhum dado disponível na tabela 'indicadores'.")

# Rodapé
st.markdown("---")
st.caption(f"🔄 Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
st.caption("📡 Dados: AwesomeAPI (Dólar) e Banco Central (Selic/IPCA)")