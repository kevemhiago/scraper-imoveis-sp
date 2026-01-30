import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Dashboard Imóveis SP", layout="wide")

# Título e Subtítulo
st.title("🏙️ Dashboard de Inteligência Imobiliária")
st.write("Monitoramento de preços de aluguel em São Paulo/SP (Fonte: VivaReal)")

# --- 1. CARREGAR DADOS DO BANCO SQL ---
# Função com cache para não ficar lendo o banco toda hora
@st.cache_data
def carregar_dados():
    conexao = sqlite3.connect("imoveis_sp.db")
    df = pd.read_sql("SELECT * FROM tb_anuncios", conexao)
    conexao.close()
    return df

# Tenta carregar
try:
    df = carregar_dados()
except:
    st.error("Erro: Banco de dados não encontrado. Rode o robô primeiro!")
    st.stop()

# --- 2. SIDEBAR (FILTROS LATERAIS) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Preço Máximo
max_preco = st.sidebar.slider("Preço Máximo (R$)", 
                              min_value=float(df['Valor_Real'].min()), 
                              max_value=float(df['Valor_Real'].max()), 
                              value=3000.0) # Valor inicial

# Aplica o filtro na tabela
df_filtrado = df[df['Valor_Real'] <= max_preco]

# --- 3. MÉTRICAS (KPIs) ---
col1, col2, col3 = st.columns(3)
col1.metric("Imóveis Encontrados", len(df_filtrado))
col2.metric("Média de Preço", f"R$ {df_filtrado['Valor_Real'].mean():.2f}")
col3.metric("Mais Barato", f"R$ {df_filtrado['Valor_Real'].min():.2f}")

# --- 4. GRÁFICOS E TABELA ---
col_grafico, col_tabela = st.columns([2, 1]) # Coluna do gráfico é maior

with col_grafico:
    st.subheader("📊 Distribuição de Preços")
    # Gráfico simples nativo do Streamlit
    st.bar_chart(df_filtrado['Valor_Real'])

with col_tabela:
    st.subheader("📋 Lista de Imóveis")
    # Mostra apenas colunas importantes e links clicáveis
    st.dataframe(
        df_filtrado[['Endereço', 'Valor_Real', 'Link']],
        column_config={
            "Link": st.column_config.LinkColumn("Link do Anúncio")
        },
        hide_index=True
    )

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Kevem | Engenharia de Dados")