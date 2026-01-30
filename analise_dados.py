import pandas as pd
import sqlite3
import matplotlib.pyplot as plt # A biblioteca que você acabou de instalar

# --- 1. PEGAR DADOS DO BANCO SQL ---
print("🔄 Conectando ao Banco de Dados...")
conexao = sqlite3.connect("imoveis_sp.db")
df = pd.read_sql("SELECT * FROM tb_anuncios", conexao)
conexao.close()

# --- 2. DESENHAR O GRÁFICO ---
print("🎨 Gerando gráfico de preços...")

# Cria a moldura do gráfico
plt.figure(figsize=(10, 6))

# Desenha o Histograma (Barras azuis)
plt.hist(df['Valor_Real'], bins=20, color='#007acc', edgecolor='black')

# Títulos e Etiquetas
plt.title('Distribuição dos Preços de Aluguel (SP)', fontsize=16)
plt.xlabel('Preço (R$)', fontsize=12)
plt.ylabel('Quantidade de Imóveis', fontsize=12)
plt.grid(axis='y', alpha=0.5) # Linhas de grade fraquinhas

# Mostra o gráfico na tela
print("✅ Gráfico pronto! Olhe a janela nova.")
plt.show()