from extrair_PDF import extrair_texto_pdf, extrair_linhas_de_tabelas

def scraper(links_filtrados):
    docentes_lista = []

    print("🚀 Iniciando a extração de nomes docentes...")

    for url in links_filtrados:
        try:
            texto = extrair_texto_pdf(url)
            if "compiladores" not in texto.lower():
                continue
            try:
                with open("docentes.txt", "r", encoding="utf-8") as f:
                    nomes_arquivo = set(nome.strip() for nome in f if nome.strip())
            except FileNotFoundError:
                nomes_arquivo = set()

            docentes = extrair_linhas_de_tabelas(url)

            for nome in docentes.split("\n"):
                nome_limpo = nome.strip()
                if nome_limpo and nome_limpo not in docentes_lista and nome_limpo not in nomes_arquivo:
                    docentes_lista.append(nome_limpo)
            
            # Salva arquivos
            with open("docentes.txt", "w", encoding="utf-8") as arq1:
                arq1.write("\n".join(docentes_lista))
                
            print(f"\n✅ Registrado {len(docentes_lista)} novos docentes.")
            
        except Exception as e:
            print(f"\n⚠️ Erro ao processar {url}: {e}")
            continue
            
    

    print(f"\n📁 Total de docentes identificados: {len(docentes_lista)}")


def scraper_lattes(texto_pagina, docente):
    texto_pagina = texto_pagina.lower()  # padroniza para evitar variações
    nome = ""
    contato = ""
    if "compiladores" in texto_pagina:
        linhas = docente.split("\n")
        for linha in linhas:
                if linha:
                    nome = linha.strip()
                    contato = buscar_contato(texto_pagina)
            
        with open("docentes_compiladores.txt", "a", encoding="utf-8") as f:
            f.write(f"Nome: {nome}\nContato: {contato}\n\n")

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