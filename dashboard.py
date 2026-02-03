import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard Imóveis SP", layout="wide")

st.title("🏙️ Dashboard de Inteligência Imobiliária")
st.write("Monitoramento de preços de aluguel em São Paulo/SP (Fonte: VivaReal)")

# --- 1. CARREGAR DADOS ---
@st.cache_data
def carregar_dados():
    conexao = sqlite3.connect("imoveis_sp.db")
    df = pd.read_sql("SELECT * FROM tb_anuncios", conexao)
    conexao.close()
    return df

try:
    df = carregar_dados()
except:
    st.error("Erro: Banco de dados não encontrado.")
    st.stop()

# --- 2. SIDEBAR (FILTROS) ---
st.sidebar.header("🔍 Filtros Avançados")

# Filtro 1: Preço Máximo
max_preco = st.sidebar.slider("💰 Preço Máximo (R$)", 
                              min_value=float(df['Valor_Real'].min()), 
                              max_value=float(df['Valor_Real'].max()), 
                              value=5000.0)

# Filtro 2: Bairro (NOVIDADE!)
bairro = st.sidebar.text_input("📍 Filtrar por Bairro (Ex: Perdizes)", "")

# --- APLICAÇÃO DOS FILTROS ---
# Primeiro filtra pelo preço
df_filtrado = df[df['Valor_Real'] <= max_preco]

# Se tiver algo escrito no bairro, filtra também
if bairro:
    # O 'case=False' faz funcionar tanto 'Perdizes' quanto 'perdizes'
    df_filtrado = df_filtrado[df_filtrado['Endereço'].str.contains(bairro, case=False, na=False)]

# --- 3. MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("Imóveis Encontrados", len(df_filtrado))

if len(df_filtrado) > 0:
    col2.metric("Média de Preço", f"R$ {df_filtrado['Valor_Real'].mean():.2f}")
    col3.metric("Mais Barato", f"R$ {df_filtrado['Valor_Real'].min():.2f}")
else:
    col2.metric("Média", "R$ 0,00")
    col3.metric("Mais Barato", "R$ 0,00")
    st.warning("⚠️ Nenhum imóvel encontrado com esses filtros.")

# --- 4. GRÁFICOS E TABELA ---
col_grafico, col_tabela = st.columns([2, 1])

with col_grafico:
    st.subheader("📊 Distribuição de Preços")
    if len(df_filtrado) > 0:
        st.bar_chart(df_filtrado['Valor_Real'])

with col_tabela:
    st.subheader("📋 Lista de Imóveis")
    if len(df_filtrado) > 0:
        st.dataframe(
            df_filtrado[['Endereço', 'Valor_Real', 'Link']],
            column_config={
                "Link": st.column_config.LinkColumn("Link do Anúncio")
            },
            hide_index=True
        )