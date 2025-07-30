from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from io import BytesIO
import pdfplumber
import fitz
import requests
import re
import csv

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

    driver.quit()

    return links
    
def scraper(links_filtrados):
    lista_docentes = []
    print("Iniciando a extração de nomes docentes...")

    for url in links_filtrados:
        try:
            texto = extrair_texto_pdf(url)
            if "compiladores" in texto.lower():
                linhas_texto = extrair_linhas_de_tabelas(url).split("\n")

                for linha in linhas_texto:
                    celulas = linha.split("\t")
                    if celulas and celulas[0].strip():
                        lista_docentes.append(celulas[0].strip())
                        print(f"\n👤 Docente encontrado: {celulas[0].strip()}")

        except Exception as e:
            print(f"\n⚠️ Erro ao processar {url}: {e}")
            continue

    with open("nomes_docentes.csv", mode="w", newline="", encoding="utf-8") as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Nome do Docente"])
        for nome in lista_docentes:
            writer.writerow([nome])

    print(f"\n📁 Total de nomes salvos: {len(lista_docentes)}")

def extrair_texto_pdf(url_pdf):
    try:
        resposta = requests.get(url_pdf, timeout=60)
        with fitz.open(stream=resposta.content, filetype="pdf") as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            return texto
    except requests.exceptions.Timeout:
        print(f"\n⏳ Tempo esgotado ao tentar acessar: {url_pdf}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão ou download: {e}")
    except Exception as e:
        print(f"\n❌ Erro ao processar o PDF: {e}")
    return ""

def extrair_linhas_de_tabelas(url):
    try:
        resposta = requests.get(url, timeout=60)
        linhas_extraidas = []

        with pdfplumber.open(BytesIO(resposta.content)) as pdf:
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()

                if not tabelas:
                    continue

                for tabela in tabelas:
                    if tabela:
                        for linha in tabela:
                            if linha:
                                if re.search(r"\b(Doutor|Mestre)\b", linha):
                                    primeira_celula = linha[0].lower() if linha[0] else ""
                                    if "bibliografia" in primeira_celula:
                                        continue  # ignora linhas de bibliografia

                                    linha_limpa = [celula if celula else "" for celula in linha]
                                    linhas_extraidas.append("\t".join(linha_limpa))
                                    print("📄 Linha válida:", linha_limpa)

        return "\n".join(linhas_extraidas)

    except requests.exceptions.Timeout:
        print(f"\n⏳ Tempo esgotado ao tentar acessar: {url}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão ou download: {e}")
    except Exception as e:
        print(f"\n❌ Erro ao processar o PDF: {e}")

    return ""
