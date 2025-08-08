import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from scraper import scraper_lattes

options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service, options=options)

def crawler():
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
    search_box.send_keys("ppc ciência da computação pdf")
    search_box.send_keys(Keys.ENTER)
    
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    
    links = []

    for pagina in range(1, 17):  # Vai da página 1 até 16
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "zReHs"))
        )

        resultados = driver.find_elements(By.CLASS_NAME, "zReHs")
        novos_links = [link.get_attribute("href") for link in resultados if link.get_attribute("href")]
        links.extend(novos_links)
        print(f"🔎 Página {pagina} 🔗 Links encontrados na página: {len(novos_links)}")
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "NKTSme"))
            )
            botoes_paginas = driver.find_elements(By.XPATH, "//*[@class='NKTSme']")
            proxima_pagina = f"Page {pagina+1}"
            botao_correto = None
            for botao in botoes_paginas:
                link_tag = botao.find_element(By.TAG_NAME, "a")
                if link_tag.get_attribute("aria-label") == proxima_pagina:
                    botao_correto = link_tag
                    break

            if botao_correto:
                botao_correto.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "zReHs"))
                )
                time.sleep(2)  # Pequena pausa para garantir carregamento
            else:
                print(f"🚫 Botão para página {pagina+1} não encontrado.")
                break

                
        except:
            print("🚫 Não foi possível avançar para a próxima página.")
            break

    print(f"🔗 Total de links encontrados: {len(links)}")
    return links

def crawler_lattes():
    aba_original = driver.current_window_handle
    print("🚀 Iniciando a coleta de Lattes...")
    texto_completo = ""
    try:    
        with open("docentes.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()

            for nome in linhas:
                driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar")
                
                WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.ID, "buscarDemais"))
                )

                checkbox = driver.find_element(By.ID, "buscarDemais")
                if checkbox.get_attribute("value") == "true":
                    checkbox.click()
                    
                WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.ID, "textoBusca"))
                )
                search_box = driver.find_element(By.CLASS_NAME, "input-text")
                search_box.clear()
                search_box.send_keys(nome)
                search_box.send_keys(Keys.ENTER)
                WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "resultado"))
                )
                div_resultado = driver.find_element(By.CLASS_NAME, "resultado")
                resultados_lista = div_resultado.find_element(By.TAG_NAME, "ol")
                resultados = resultados_lista.find_elements(By.TAG_NAME, "li")
                try:
                    aba_resultado = driver.current_window_handle
                    for resultado in resultados:
                        link_resultado = resultado.find_element(By.TAG_NAME, "a")
                        href_resultado = link_resultado.get_attribute("href")
                    
                        if href_resultado is not None:
                            link_resultado.click()
                            WebDriverWait(driver, 30).until(
                                        EC.presence_of_element_located((By.NAME, "frameModalPreview"))
                                    )
                            WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "control-bar-wrapper")
                            ))
                            
                            resumo = driver.find_element(By.CLASS_NAME, "control-bar-wrapper")
                            
                            WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.TAG_NAME, "a")
                            ))
                            
                            link_resumo = resumo.find_element(By.TAG_NAME, "a")
                            id_resumo = link_resumo.get_attribute("id")
                            
                            if "idbtnabrircurriculo" in id_resumo:
                                href_resumo = link_resumo.get_attribute("href")
                                if href_resumo is not None:
                                    time.sleep(2)
                                    link_resumo.click()
                                    
                                    time.sleep(5)
                                    abas = driver.window_handles
                                    driver.switch_to.window(abas[-1])
                                    time.sleep(3)
                                    WebDriverWait(driver, 30).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "resumo"))
                                    )
                                    
                                    div_principal = driver.find_elements(By.CLASS_NAME, "title-wrapper")

                                    for elemento in div_principal:
                                        try:
                                            titulo = elemento.find_element(By.TAG_NAME, "a")
                                            nome_titulo = titulo.get_attribute("name")

                                            if "AtuacaoProfissional" in nome_titulo:
                                                
                                                divs_internas = elemento.find_elements(By.TAG_NAME, "div")

                                                textos = []
                                                for div_interna in divs_internas:
                                                    try:
                                                        div_texto = div_interna.find_element(By.TAG_NAME, "div")
                                                        texto = div_texto.text.strip()
                                                        if texto:
                                                            textos.append(texto)
                                                    except:
                                                        continue
                                                texto_completo = " ".join(textos)
                                        except:
                                            continue

                                    scraper_lattes(texto_completo, nome)
                                    driver.close()
                                    driver.switch_to.window(aba_resultado)
                                    div_botao = driver.find_element(By.CLASS_NAME, "bt-moldal")
                                    botao = div_botao.find_element(By.TAG_NAME, "a")
                                    if not botao:
                                        continue
                                    botao.click()
                  
                    driver.switch_to.window(aba_original)                  
                except NoSuchElementException:
                    print(f"\n❌ Nenhum resultado encontrado para: {nome}")
                    continue
                    
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")    
    except Exception as e:
        print(f"❌ Erro ao acessar Lattes: {e}")
    finally:
        driver.quit()
        