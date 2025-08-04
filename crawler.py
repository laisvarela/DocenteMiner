from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
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
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    resultados = driver.find_elements(By.CLASS_NAME, "zReHs")
    links = [link.get_attribute("href") for link in resultados if link.get_attribute("href")]
    print(f"Total de links encontrados: {len(links)}")

    return links

def crawler_lattes():
    print("🚀 Iniciando a coleta de Lattes...")
    texto = driver.find_element(By.TAG_NAME, "body").text
    docente
    try:
        with open("docentes_com_lattes.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha in linhas:
                if "Nome:" in linha:
                    nome = linha
                if "Email:" in linha:
                    email = linha
                if "lattes:" in linha.lower():
                    lattes = linha.replace("Lattes:", "").strip()
                    print(f"Acessando Lattes: {lattes}")
                    docente = f"{nome}\n{email}\n"
                    driver.get(lattes)
                    WebDriverWait(driver, 30)
                scraper_lattes(texto, [docente])
            
        with open("docentes_sem_lattes.txt", "r", encoding="utf-8") as f:
            linhas2 = f.readlines()
            driver.get("https://buscatextual.cnpq.br/buscatextual/busca.do?metodo=apresentar")
            
            checkbox = driver.find_element(By.ID, "buscarDemais").get_attribute("value")
            WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.ID, "buscarDemais"))
            )
            if checkbox == "false":
                driver.find_element(By.ID, "buscarDemais").click()
                
            for nome in linhas2:
                WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.ID, "textoBusca"))
                )
                search_box = driver.find_element(By.CLASS_NAME, "input-text")
                search_box.clear()
                search_box.send_keys(nome)
                search_box.send_keys(Keys.ENTER)
                scraper_lattes(texto, [nome])
                
    except FileNotFoundError:
        print("❌ Arquivo não encontrado.")    
    except Exception as e:
        print(f"❌ Erro ao acessar Lattes: {e}")
    finally:
        driver.quit()