from extrair_PDF import extrair_texto_pdf, extrair_linhas_de_tabelas

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


def scraper_lattes(texto_pagina, lista_docentes):
    texto_pagina = texto_pagina.lower()  # padroniza para evitar variações

    if "compiladores" in texto_pagina:
        for docente in lista_docentes:
            dados = docente.split("\n")
            if "nome:" in dados[0].lower() and "email:" in dados[1].lower():
                nome = dados[0]
                email = dados[1]

            with open("docentes_compiladores.txt", "a", encoding="utf-8") as f:
                f.write(f"{nome} - {email}\n")

            print(f"✅ Registrado: {nome} - {email}")
    else:
        print("🔍 Nenhuma menção a 'compiladores' no texto da página.")



    
        