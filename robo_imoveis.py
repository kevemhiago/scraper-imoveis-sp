from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
from time import sleep

# --- CONFIGURAÇÃO ---
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")

print("🤖 Iniciando Robô V5.2 (Paginação Automática)...")
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.vivareal.com.br/aluguel/sp/sao-paulo/apartamento_residencial/"
navegador.get(url)

todos_imoveis = []
quantidade_paginas = 5 

for pagina in range(quantidade_paginas):
    print(f"\n📄 Lendo Página {pagina + 1} de {quantidade_paginas}...")
    
    # 1. Espera e Scroll
    sleep(3)
    navegador.execute_script("window.scrollTo(0, 1000);")
    sleep(2)
    
    # 2. Coleta
    elementos = navegador.find_elements(By.XPATH, "//a[contains(@href, '/imovel/')]")
    elementos = list(set(elementos)) 
    
    print(f"   🏠 Encontrei {len(elementos)} anúncios nesta página.")

    for imovel in elementos:
        try:
            link = imovel.get_attribute("href")
            texto = imovel.text
            if not texto: continue

            linhas = texto.split("\n")
            endereco = linhas[0]
            preco_real = "Preço não achado" 

            for linha in linhas:
                if "R$" in linha:
                    preco_real = linha
                    break 

            todos_imoveis.append({
                "Endereço": endereco,
                "Preço": preco_real,
                "Link": link
            })
        except:
            continue

    # 3. MUDANÇA DE PÁGINA (CORRIGIDO)
    try:
        print("   ➡️ Tentando ir para a próxima página...")
        
        # Rola até o fundo absoluto
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        # Tenta achar o botão de várias formas
        botao_proxima = None
        try:
            # Tenta pelo texto "Próxima" (mais comum)
            botao_proxima = navegador.find_element(By.XPATH, "//a[contains(text(), 'Próxima')]")
        except:
            try:
                # Tenta pelo título
                botao_proxima = navegador.find_element(By.XPATH, "//*[@title='Próxima página']")
            except:
                # Tenta pelo número da próxima página
                prox_num = str(pagina + 2)
                botao_proxima = navegador.find_element(By.XPATH, f"//button[contains(text(), '{prox_num}')]")

        if botao_proxima:
            navegador.execute_script("arguments[0].click();", botao_proxima)
            sleep(5) # Dá tempo para a nova página carregar
        else:
            print("   ❌ Botão não encontrado. Parando.")
            break

    except Exception as e:
        print(f"   ⚠️ Erro ao mudar de página: {e}")
        break

# --- FINALIZAR ---
print(f"\n💾 Salvando {len(todos_imoveis)} imóveis no Excel...")
df = pd.DataFrame(todos_imoveis)
df.to_csv("resultado_imoveis_completo.csv", index=False, sep=";", encoding="utf-8-sig")

print("✅ SUCESSO! Pode abrir o arquivo.")
navegador.quit()