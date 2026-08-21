# dashboard/app.py - DASHBOARD COMPLETO COM ANÁLISES
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════
# 🎨 CONFIGURAÇÃO
# ═══════════════════════════════════════════════════

st.set_page_config(
    page_title="Indicadores Econômicos",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'Get Help': None, 'Report a bug': None, 'About': None}
)

# CSS - Tema Escuro Neon
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    :root {
        --neon-blue: #00D4FF;
        --neon-purple: #7C3AED;
        --neon-green: #00FF88;
        --neon-pink: #FF2D95;
        --neon-yellow: #FFE600;
        --dark-bg: #0A0A1A;
        --card-bg: #141430;
        --card-border: rgba(0, 212, 255, 0.15);
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --glow-blue: rgba(0, 212, 255, 0.3);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none !important;}
    button[kind="header"] {display: none !important;}
    
    .stApp, .stApp > div, .stApp > div > div {
        background-color: #0A0A1A !important;
    }
    
    * {font-family: 'Inter', sans-serif !important;}
    
    h1 {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-shadow: 0 0 40px var(--glow-blue);
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, var(--card-bg), rgba(20, 20, 48, 0.8));
        border-radius: 16px;
        padding: 20px 18px;
        border: 1px solid var(--card-border);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.05);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: var(--neon-blue);
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.1);
        transform: translateY(-4px);
    }
    
    div[data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--neon-blue) !important;
        font-weight: 800 !important;
        font-size: 26px !important;
        text-shadow: 0 0 20px var(--glow-blue);
    }
    
    .stLineChart, .stPlotlyChart {
        background: linear-gradient(145deg, var(--card-bg), rgba(20, 20, 48, 0.8));
        border-radius: 16px;
        padding: 20px;
        border: 1px solid var(--card-border);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.03);
    }
    
    .stDataFrame {
        background: linear-gradient(145deg, var(--card-bg), rgba(20, 20, 48, 0.8));
        border-radius: 16px;
        padding: 10px;
        border: 1px solid var(--card-border);
    }
    
    .stDataFrame thead tr th {
        background-color: rgba(0, 212, 255, 0.05) !important;
        color: var(--neon-blue) !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(20, 20, 48, 0.5) !important;
        padding: 6px !important;
        border-radius: 12px !important;
        border: 1px solid var(--card-border) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--neon-blue) !important;
        background-color: rgba(0, 212, 255, 0.05) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple)) !important;
        color: white !important;
        box-shadow: 0 0 30px var(--glow-blue) !important;
    }
    
    .subtitle {color: var(--text-secondary); font-size: 16px; font-weight: 400; margin-bottom: 24px;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 📊 TÍTULO
# ═══════════════════════════════════════════════════

st.title("⚡ Dashboard Indicadores Econômicos")
st.markdown('<p class="subtitle">Dólar · Selic · IPCA — Análise completa em tempo real</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 🔑 CONEXÃO COM SUPABASE
# ═══════════════════════════════════════════════════

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    load_dotenv()
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Credenciais do Supabase não encontradas!")
    st.stop()

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

# ═══════════════════════════════════════════════════
# 📥 CARREGAR DADOS
# ═══════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def load_data():
    try:
        cambio = supabase.table('cambio').select('*').order('timestamp', desc=True).limit(30).execute()
        indicadores = supabase.table('indicadores').select('*').order('timestamp', desc=True).limit(30).execute()
        return pd.DataFrame(cambio.data), pd.DataFrame(indicadores.data)
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_cambio, df_indicadores = load_data()

# ═══════════════════════════════════════════════════
# 📊 FUNÇÕES DE ANÁLISE
# ═══════════════════════════════════════════════════

def calcular_medias_moveis(df, coluna, periodo=7):
    if len(df) >= periodo:
        return df[coluna].tail(periodo).mean()
    return None

def calcular_volatilidade(df, coluna):
    if len(df) >= 2:
        return df[coluna].std()
    return None

def analisar_tendencia(df, coluna):
    if len(df) >= 7:
        ultimos = df[coluna].tail(7)
        if ultimos.iloc[-1] > ultimos.iloc[0]:
            return "ALTA", "bull"
        elif ultimos.iloc[-1] < ultimos.iloc[0]:
            return "BAIXA", "bear"
    return "NEUTRA", "neutral"

def calcular_variacao_periodo(df, coluna, dias=7):
    if len(df) >= dias:
        inicio = df[coluna].iloc[-dias]
        fim = df[coluna].iloc[-1]
        return ((fim - inicio) / inicio) * 100
    return None

# ═══════════════════════════════════════════════════
# 📈 MÉTRICAS PRINCIPAIS (LINHA 1)
# ═══════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

if not df_cambio.empty:
    ultimo = df_cambio.iloc[0]
    
    media_7d = calcular_medias_moveis(df_cambio, 'dolar_compra', 7)
    volatilidade = calcular_volatilidade(df_cambio, 'dolar_compra')
    tendencia, tendencia_class = analisar_tendencia(df_cambio, 'dolar_compra')
    variacao_7d = calcular_variacao_periodo(df_cambio, 'dolar_compra', 7)
    
    variacao_diaria = float(ultimo.get('variacao_percentual', 0))
    
    with col1:
        st.metric(
            label="💵 Dólar (Compra)",
            value=f"R$ {float(ultimo['dolar_compra']):.2f}",
            delta=f"{variacao_diaria:.2f}%",
            delta_color="inverse" if variacao_diaria < 0 else "normal"
        )
    
    with col2:
        if media_7d:
            st.metric(
                label="📊 Média 7 dias",
                value=f"R$ {media_7d:.2f}",
                delta=f"{((float(ultimo['dolar_compra']) - media_7d) / media_7d * 100):.2f}% vs média"
            )
        else:
            st.metric("📊 Média 7 dias", "Dados insuficientes")
    
    with col3:
        if variacao_7d is not None:
            st.metric(
                label="📈 Variação 7 dias",
                value=f"{variacao_7d:.2f}%",
                delta="Acumulado"
            )
        else:
            st.metric("📈 Variação 7 dias", "Dados insuficientes")
    
    with col4:
        badge_class = f"badge-{tendencia_class}"

# ═══════════════════════════════════════════════════
# 📊 INDICADORES ECONÔMICOS (LINHA 2)
# ═══════════════════════════════════════════════════

col5, col6, col7 = st.columns(3)

if not df_indicadores.empty:
    df_selic = df_indicadores[df_indicadores['indicador'] == 'Selic']
    df_ipca = df_indicadores[df_indicadores['indicador'] == 'IPCA_12m']
    
    with col5:
        if not df_selic.empty:
            selic_atual = float(df_selic.iloc[0]['valor'])
            if len(df_selic) > 1:
                selic_anterior = float(df_selic.iloc[1]['valor'])
                delta_selic = selic_atual - selic_anterior
                st.metric(
                    label="🏦 Taxa Selic",
                    value=f"{selic_atual:.2f}%",
                    delta=f"{delta_selic:+.2f}%",
                    delta_color="inverse" if delta_selic < 0 else "normal"
                )
            else:
                st.metric("🏦 Taxa Selic", f"{selic_atual:.2f}%")
        else:
            st.metric("🏦 Taxa Selic", "N/A")
    
    with col6:
        if not df_ipca.empty:
            ipca_atual = float(df_ipca.iloc[0]['valor'])
            if len(df_ipca) > 1:
                ipca_anterior = float(df_ipca.iloc[1]['valor'])
                delta_ipca = ipca_atual - ipca_anterior
                st.metric(
                    label="📈 IPCA (12 meses)",
                    value=f"{ipca_atual:.2f}%",
                    delta=f"{delta_ipca:+.2f}%",
                    delta_color="inverse" if delta_ipca < 0 else "normal"
                )
            else:
                st.metric("📈 IPCA (12 meses)", f"{ipca_atual:.2f}%")
        else:
            st.metric("📈 IPCA (12 meses)", "N/A")
    
    with col7:
        if not df_selic.empty and not df_ipca.empty:
            selic_val = float(df_selic.iloc[0]['valor'])
            ipca_val = float(df_ipca.iloc[0]['valor'])
            juro_real = selic_val - ipca_val
            
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, var(--card-bg), rgba(20,20,48,0.8)); 
                        border-radius: 16px; padding: 20px 18px; 
                        border: 1px solid var(--card-border); height: 100%;">
                <div style="color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600;">
                    📊 Análise Econômica
                </div>
                <div style="margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; padding: 4px 0;">
                        <span style="color: var(--text-secondary);">Juro Real</span>
                        <span style="color: {'var(--neon-green)' if juro_real > 0 else 'var(--neon-pink)'}; font-weight: 700;">
                            {juro_real:.2f}%
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 4px 0; border-top: 1px solid var(--card-border);">
                        <span style="color: var(--text-secondary);">Spread Selic/IPCA</span>
                        <span style="color: var(--neon-blue); font-weight: 700;">
                            {(selic_val - ipca_val):.2f} p.p.
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 📈 GRÁFICOS E ANÁLISES
# ═══════════════════════════════════════════════════

st.subheader("📊 Análises Avançadas")

tab1, tab2, tab3 = st.tabs(["📈 Evolução do Dólar", "📊 Estatísticas", "📋 Dados Históricos"])

# ─── TAB 1: GRÁFICO ───
# ─── TAB 1: GRÁFICO ───
with tab1:
    if not df_cambio.empty:
        df_ordenado = df_cambio.sort_values('timestamp')
        
        if len(df_ordenado) > 1:
            import plotly.graph_objects as go
            
            # Criar figura
            fig = go.Figure()
            
            # Adicionar linha de Compra (mais grossa e com marcadores)
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df_ordenado['timestamp']),
                y=df_ordenado['dolar_compra'].astype(float),
                mode='lines+markers',
                name='Compra',
                line=dict(color='#00D4FF', width=4),
                marker=dict(size=10, color='#00D4FF', symbol='circle', line=dict(color='#FFFFFF', width=2))
            ))
            
            # Adicionar linha de Venda (com estilo diferente)
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df_ordenado['timestamp']),
                y=df_ordenado['dolar_venda'].astype(float),
                mode='lines+markers',
                name='Venda',
                line=dict(color='#FF2D95', width=4, dash='dash'),  # Linha tracejada
                marker=dict(size=10, color='#FF2D95', symbol='diamond', line=dict(color='#FFFFFF', width=2))
            ))
            
            # 🔥 ADICIONAR ÁREA ENTRE AS LINHAS (SPREAD)
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df_ordenado['timestamp']),
                y=df_ordenado['dolar_compra'].astype(float),
                mode='lines',
                name='Spread',
                fill='tonexty',
                fillcolor='rgba(0, 212, 255, 0.05)',
                line=dict(color='rgba(0,0,0,0)'),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df_ordenado['timestamp']),
                y=df_ordenado['dolar_venda'].astype(float),
                mode='lines',
                name='Spread',
                fill='tonexty',
                fillcolor='rgba(255, 45, 149, 0.05)',
                line=dict(color='rgba(0,0,0,0)'),
                showlegend=False
            ))
            
            # Configurar layout
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(20, 20, 48, 0.8)',
                plot_bgcolor='rgba(20, 20, 48, 0.8)',
                font=dict(color='#94A3B8'),
                title=dict(
                    text='Evolução do Dólar (USD/BRL)',
                    font=dict(color='#FFFFFF', size=16)
                ),
                xaxis=dict(
                    title='Data',
                    gridcolor='rgba(0, 212, 255, 0.1)',
                    showgrid=True,
                    tickformat='%d/%m'
                ),
                yaxis=dict(
                    title='Valor (R$)',
                    gridcolor='rgba(0, 212, 255, 0.1)',
                    showgrid=True,
                    tickformat='.2f'
                ),
                legend=dict(
                    x=0.02,
                    y=0.98,
                    bgcolor='rgba(20, 20, 48, 0.8)',
                    bordercolor='rgba(0, 212, 255, 0.2)',
                    borderwidth=1
                ),
                hovermode='x unified'
            )
            
            # Mostrar gráfico
            st.plotly_chart(fig, use_container_width=True)
            
            # Informação sobre o spread
            spread_medio = (df_ordenado['dolar_venda'].astype(float) - df_ordenado['dolar_compra'].astype(float)).mean()
            st.caption(f"📊 Spread médio: R$ {spread_medio:.4f} (diferença entre compra e venda)")
            
            # Resumo
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("📈 Máxima Compra", f"R$ {df_ordenado['dolar_compra'].max():.2f}")
            with col_b:
                st.metric("📉 Mínima Compra", f"R$ {df_ordenado['dolar_compra'].min():.2f}")
            with col_c:
                st.metric("📊 Amplitude", f"R$ {(df_ordenado['dolar_compra'].max() - df_ordenado['dolar_compra'].min()):.2f}")
        else:
            st.warning("⚠️ Dados insuficientes. São necessários pelo menos 2 pontos para exibir o gráfico.")
    else:
        st.warning("⚠️ Nenhum dado de câmbio encontrado.")
# ─── TAB 2: ESTATÍSTICAS ───
with tab2:
    if not df_cambio.empty:
        # Criar 2 colunas para Estatísticas e Tendência
        col_est1, col_est2 = st.columns(2)
        
        with col_est1:
            st.markdown("#### 📊 Estatísticas do Dólar")
            stats_df = pd.DataFrame({
                'Métrica': ['Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo'],
                'Valor': [
                    f"R$ {df_cambio['dolar_compra'].mean():.2f}",
                    f"R$ {df_cambio['dolar_compra'].median():.2f}",
                    f"R$ {df_cambio['dolar_compra'].std():.3f}",
                    f"R$ {df_cambio['dolar_compra'].min():.2f}",
                    f"R$ {df_cambio['dolar_compra'].max():.2f}"
                ]
            })
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
        
        with col_est2:
            st.markdown("#### 📈 Análise de Tendência")
            
            if len(df_cambio) >= 7:
                ultimos_7 = df_cambio['dolar_compra'].tail(7)
                tendencia_dias = []
                
                for i in range(1, len(ultimos_7)):
                    if ultimos_7.iloc[i] > ultimos_7.iloc[i-1]:
                        tendencia_dias.append("📈")
                    elif ultimos_7.iloc[i] < ultimos_7.iloc[i-1]:
                        tendencia_dias.append("📉")
                    else:
                        tendencia_dias.append("➡️")
                
                # Criar uma string com os emojis
                tendencia_str = " ".join(tendencia_dias)
                
                # Calcular dias em alta
                dias_alta = tendencia_dias.count("📈")
                perc_alta = (dias_alta / len(tendencia_dias)) * 100
                
                # 🔥 FORMATAR MELHOR A TENDÊNCIA
                st.markdown(f"""
                <div style="background: linear-gradient(145deg, var(--card-bg), rgba(20,20,48,0.8)); 
                            border-radius: 16px; padding: 20px; 
                            border: 1px solid var(--card-border);">
                    <div style="color: var(--text-secondary); font-size: 14px; margin-bottom: 12px;">
                        📊 Últimos 7 dias:
                    </div>
                    <div style="font-size: 28px; letter-spacing: 8px; text-align: center; padding: 10px 0;">
                        {tendencia_str}
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--card-border);">
                        <div>
                            <span style="color: var(--text-secondary);">📈 Dias em Alta</span>
                            <span style="color: var(--neon-green); font-weight: 700; font-size: 18px; margin-left: 8px;">
                                {dias_alta}/{len(tendencia_dias)}
                            </span>
                        </div>
                        <div>
                            <span style="color: var(--text-secondary);">🎯 Percentual</span>
                            <span style="color: var(--neon-blue); font-weight: 700; font-size: 18px; margin-left: 8px;">
                                {perc_alta:.0f}%
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Dados insuficientes para análise de tendência (mínimo 7 dias)")
    else:
        st.warning("⚠️ Nenhum dado disponível para estatísticas")

# ─── TAB 3: DADOS HISTÓRICOS ───
with tab3:
    if not df_cambio.empty:
        st.dataframe(
            df_cambio[['timestamp', 'dolar_compra', 'dolar_venda', 'maximo', 'minimo', 'variacao_percentual']].head(20),
            use_container_width=True,
            hide_index=True
        )
        
        st.caption(f"📊 Total de {len(df_cambio)} registros carregados")

# ═══════════════════════════════════════════════════
# 📌 RODAPÉ
# ═══════════════════════════════════════════════════

st.markdown("---")

data_atual = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')

st.write(f"🔄 **Última atualização:** {data_atual}")
st.write("📡 **Dados:** AwesomeAPI (Dólar) e Banco Central (Selic/IPCA)")
st.write("🚀 **Desenvolvido por:** Angelica Aquiarati")