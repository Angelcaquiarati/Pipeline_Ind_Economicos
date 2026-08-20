# 📊 Pipeline de Indicadores Econômicos

Pipeline automatizado de engenharia de dados para coleta, transformação e visualização de indicadores econômicos (Dólar, Selic e IPCA).

## 🏗️ Arquitetura
[API AwesomeAPI] → [GitHub Actions] → [Python ETL] → [Supabase] → [Streamlit Dashboard]
[API BCB] → ↘

## 🛠️ Tecnologias

- **Orquestração**: GitHub Actions
- **ETL**: Python (Pandas, Requests)
- **Banco de Dados**: Supabase (PostgreSQL)
- **Dashboard**: Streamlit
- **Versionamento**: Git/GitHub

## 📊 Dashboards

Link público: [https://seu-app.streamlit.app](https://seu-app.streamlit.app)

## 📈 Dados Coletados

- **Dólar (USD/BRL)**: Cotação de compra e venda
- **Selic**: Taxa básica de juros
- **IPCA**: Inflação acumulada (12 meses)

## 🚀 Como Executar

### Localmente

```bash
conda activate pipeline-indicadores
python src/main.py
streamlit run dashboard/app.py

Automatizado

O pipeline roda automaticamente todos os dias via GitHub Actions.

pipeline_indicadores/
├── src/
│   ├── extract.py      # Coleta de dados
│   ├── transform.py    # Transformação
│   ├── load.py         # Carga no banco
│   └── main.py         # Pipeline principal
├── dashboard/
│   └── app.py          # Dashboard Streamlit
├── data/               # Backups locais
├── .github/workflows/  # GitHub Actions
└── README.md

📸 Screenshots

https://screenshot.png
🔑 Credenciais

As credenciais são gerenciadas via variáveis de ambiente (.env).
👩‍💻 Autora

[Seu Nome] - Cientista de Dados


### 2. Adicionar screenshot

```bash
# Tirar screenshot do dashboard
# No navegador, pressione F12, depois Ctrl+Shift+P (ou use a ferramenta de captura do sistema)

# Salvar como screenshot.png na raiz do projeto