import streamlit as st

st.title("🔑 Teste de Conexão com Supabase")

try:
    from supabase import create_client
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    
    st.write(f"✅ URL: {url}")
    st.write(f"✅ Key: {key[:20]}...")
    
    # Testar conexão
    supabase = create_client(url, key)
    response = supabase.table('cambio').select('*').limit(1).execute()
    st.success(f"✅ Conexão funcionou! {len(response.data)} registros encontrados.")
    
except Exception as e:
    st.error(f"❌ Erro: {e}")
