from extrair_PDF import extrair_texto_pdf, extrair_linhas_de_tabelas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def scraper(links_filtrados):
    docentes_com_lattes = []
    docentes_sem_lattes = []

    print("🚀 Iniciando a extração de nomes docentes...")

    for url in links_filtrados:
        try:
            texto = extrair_texto_pdf(url)
            if "compiladores" not in texto.lower():
                continue
            
            com_lattes, sem_lattes = extrair_linhas_de_tabelas(url)

            # Adiciona nomes à lista principal
            for linha in com_lattes.split("\n"):
                if linha:
                    celulas = linha.split("\t")
                    if celulas:
                        docentes_com_lattes.append(linha)

            for nome in sem_lattes.split("\n"):
                if nome.strip():
                    docentes_sem_lattes.append(nome.strip())
                    
        except Exception as e:
            print(f"\n⚠️ Erro ao processar {url}: {e}")
            continue
            
    # Salva arquivos
    with open("docentes_com_lattes.txt", "w", encoding="utf-8") as arq1:
        arq1.write("\n".join(docentes_com_lattes))

    with open("docentes_sem_lattes.txt", "w", encoding="utf-8") as arq2:
        arq2.write("\n".join(docentes_sem_lattes))

    print(f"\n📁 Total de docentes identificados: {len(docentes_com_lattes) + len(docentes_sem_lattes)}")


def scraper_lattes(texto_pagina, docente):
    texto_pagina = texto_pagina.lower()  # padroniza para evitar variações
    nome = ""
    contato = ""
    if "compiladores" in texto_pagina:
        linhas = docente.split("\n")
        # if len(linhas) > 1:
        #     for linha in linhas:
        #             if linha.lower().startswith("nome:"):
        #                 nome = linha.strip()
        #             elif linha.lower().startswith("contato:"):
        #                 contato = linha.strip()
        # else:
        nome = docente.strip()
        contato = buscar_contato(texto_pagina)
        with open("docentes_compiladores.txt", "a", encoding="utf-8") as f:
            f.write(f"{nome}\nContato: {contato}\n\n")

        print(f"✅ Registrado: {nome}\n{contato}")
    else:
        print("🔍 Nenhuma menção a 'compiladores' no texto da página.")

    
def buscar_contato(texto):
    contato = ""
    if "Telefone:" or "Email: " in texto:
        linhas = texto.split("\n")
        for linha in linhas:
            if "telefone:" in linha:
                contato = linha.replace("telefone:", "").strip()
            elif "email:" in linha:
                contato = linha.replace("email:", "").strip()
                
    return contato