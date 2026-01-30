# 🏘️ Scraper de Imóveis (SP) - Data Engineering Project

## 📋 Sobre o Projeto
Este projeto é um pipeline de dados completo (ETL) desenvolvido para monitorar preços de aluguel em São Paulo. Ele automatiza a coleta de dados, armazena em banco de dados SQL e gera insights visuais.

**Objetivo:** Identificar oportunidades de aluguel abaixo da média de mercado de forma automatizada.

## 🛠️ Tecnologias Utilizadas
* **Python 3.12**
* **Selenium:** Automação Web e Scraping (Web Crawler).
* **Pandas:** Limpeza e tratamento de dados (Data Cleaning).
* **SQLite:** Armazenamento persistente (Banco de Dados SQL).
* **Matplotlib:** Visualização de dados e Analytics.
* **VS Code:** IDE de desenvolvimento.

## ⚙️ Funcionalidades
1.  **Robô Extrator (`robo_imoveis.py`):**
    * Acessa o site VivaReal.
    * Navega automaticamente por múltiplas páginas (Paginação).
    * Coleta Endereço, Preço e Link.
    * Exporta dados brutos para CSV.

2.  **Pipeline de Dados (`analise_dados.py`):**
    * Lê o CSV bruto.
    * Aplica limpeza de dados (remoção de caracteres, conversão de tipos).
    * **Salva em Banco de Dados SQL** (`imoveis_sp.db`).
    * Gera um Histograma de preços para análise de mercado.

## 📊 Resultados
O projeto identificou oportunidades de aluguel a partir de **R$ 1.600,00** em bairros valorizados, permitindo uma tomada de decisão baseada em dados reais e não em "achismo".

---
*Desenvolvido por Kevem como projeto prático de Engenharia de Dados.*