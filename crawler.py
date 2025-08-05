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
driver.get("https://www.google.com")

def crawler():
    search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
    search_box.send_keys("ppc ciência da computação pdf")
    search_box.send_keys(Keys.ENTER)
    
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "zReHs"))
        )
    resultados = driver.find_elements(By.CLASS_NAME, "zReHs")
    links = [link.get_attribute("href") for link in resultados if link.get_attribute("href")]
    print(f"Total de links encontrados: {len(links)}")

    return links

def crawler_lattes():
    aba_original = driver.current_window_handle
    print("🚀 Iniciando a coleta de Lattes...")
    texto = ""
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
                resultado = driver.find_element(By.CLASS_NAME, "resultado")
                try:
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
                                
                                time.sleep(2)
                                abas = driver.window_handles
                                driver.switch_to.window(abas[-1])
                                time.sleep(2)
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "resumo"))
                                )
                                texto = driver.find_element(By.TAG_NAME, "body").text
                                scraper_lattes(texto, nome)
                                driver.close()
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
        