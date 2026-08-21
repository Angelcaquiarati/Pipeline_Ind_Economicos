# 📊 Pipeline de Indicadores Econômicos

[![Pipeline Status](https://github.com/Angelcaquiarati/Pipeline_Ind_Economicos/actions/workflows/etl_pipeline.yml/badge.svg)](https://github.com/Angelcaquiarati/Pipeline_Ind_Economicos/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pipelineindeconomicos-nwzppy4nswwzcyglm657oo.streamlit.app/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipeline automatizado de engenharia de dados para coleta, transformação e visualização de indicadores econômicos brasileiros (Dólar, Selic e IPCA). O projeto foi desenvolvido para demonstrar habilidades em **Engenharia de Dados**, **ETL**, **Automação** e **Visualização de Dados**, servindo como um case técnico para portfólio.

## 🔗 Links Rápidos

- **📊 Dashboard Online**: [pipeline-ind-economicos.streamlit.app](https://pipeline-ind-economicos.streamlit.app)
- **🐙 Repositório**: [github.com/Angelcaquiarati/Pipeline_Ind_Economicos](https://github.com/Angelcaquiarati/Pipeline_Ind_Economicos)
- **🗄️ Banco de Dados**: Supabase PostgreSQL

---

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura moderna de **ELT (Extract, Load, Transform)** com as seguintes etapas:


**Fluxo de Dados:**
1. **Extração**: Coleta automatizada de dados das APIs da AwesomeAPI (Dólar) e Banco Central (Selic/IPCA)
2. **Transformação**: Limpeza, padronização e enriquecimento dos dados com Pandas
3. **Carga**: Armazenamento no Supabase PostgreSQL
4. **Visualização**: Dashboard interativo no Streamlit com atualização diária

---

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Descrição |
|-----------|------------|-----------|
| **Orquestração** | GitHub Actions | Agendador CI/CD para execução diária do pipeline |
| **ETL** | Python 3.10+ | Linguagem principal |
| | Pandas | Manipulação e transformação de dados |
| | Requests | Consumo de APIs REST |
| **Banco de Dados** | Supabase (PostgreSQL) | Armazenamento na nuvem com planos gratuitos |
| **Visualização** | Streamlit | Dashboard interativo com deploy automático |
| **Versionamento** | Git/GitHub | Controle de versão e hospedagem do código |
| **Gerenciamento** | Conda | Gerenciamento de ambiente e dependências |

---

## 📈 Dados Coletados

### Moedas
- **Dólar (USD/BRL)**: Cotação de compra e venda, máximo e mínimo diário
- **Spread**: Diferença entre venda e compra
- **Variação Percentual**: Oscilação diária

### Indicadores Econômicos
- **Selic**: Taxa básica de juros (série 11 do BCB)
- **IPCA**: Índice de inflação acumulado (últimos 12 meses, série 433 do BCB)

---

## 🚀 Como Executar o Projeto

### 🔧 Pré-requisitos

- Python 3.10+
- Conda (recomendado)
- Conta gratuita no [Supabase](https://supabase.com)
- Chave de API da AwesomeAPI (opcional)

### 📦 Configuração do Ambiente

```bash
# Clonar o repositório
git clone https://github.com/Angelcaquiarati/Pipeline_Ind_Economicos.git
cd Pipeline_Ind_Economicos

# Criar e ativar o ambiente Conda
conda create -n pipeline-indicadores python=3.10 -y
conda activate pipeline-indicadores

# Instalar dependências
conda install pandas requests python-dotenv -c conda-forge -y
pip install supabase streamlit
