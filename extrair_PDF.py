from io import BytesIO
import re
import fitz
import pdfplumber
import requests

def extrair_texto_pdf(url_pdf):
    try:
        resposta = requests.get(url_pdf, timeout=60)
        with fitz.open(stream=resposta.content, filetype="pdf") as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            return texto
    except requests.exceptions.Timeout:
        print(f"\n⏳ Extrair texto: Tempo esgotado ao tentar acessar: {url_pdf}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Extrair texto: Erro de conexão ou download: {e}")
    except Exception as e:
        print(f"\n❌ Extrair texto: Erro ao abrir ou extrair texto do PDF de {url_pdf}: {e}")
    return ""

def extrair_linhas_de_tabelas(url):
    try:
        resposta = requests.get(url, timeout=60)
        docentes_com_lattes = []
        docentes_sem_lattes = []

        with pdfplumber.open(BytesIO(resposta.content)) as pdf:
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()

                if not tabelas:
                    continue

                for tabela in tabelas:
                    if tabela:
                        for linha in tabela:
                            if linha and len(linha) >= 6:
                                # Trata a primeira célula separadamente
                                linha_tratada = []
                                for i, celula in enumerate(linha):
                                    if i == 0:  # nome
                                        valor = celula.replace("\n", " ") if celula else ""
                                    else:       # outras células
                                        valor = celula.replace("\n", "") if celula else ""
                                    linha_tratada.append(valor)

                                linha_texto = " ".join(linha_tratada)

                                if re.search(r"\b(Doutor|Mestre)\b", linha_texto):
                                    if "bibliografia" in linha_tratada[0].lower():
                                        continue

                                    nome = linha_tratada[0]
                                    contato = linha_tratada[4]
                                    link_lattes = linha_tratada[5]

                                    if "lattes.cnpq.br" in link_lattes.lower():
                                        registro = f"Nome: {nome}\nContato: {contato}\nLattes: {link_lattes}\n\n"
                                        docentes_com_lattes.append(registro)
                                        print(f"\n✅ Registrado docente com lattes: {nome} - {contato} - {link_lattes}")
                                    else:
                                        docentes_sem_lattes.append(nome)
                                        print(f"\n✅ Registrado docente sem lattes: {nome}")
        return "\n".join(docentes_com_lattes), "\n".join(docentes_sem_lattes)

    except requests.exceptions.Timeout:
        print(f"\n⏳ Extrair tabela: Tempo esgotado ao tentar acessar: {url}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Extrair tabela: Erro de conexão ou download: {e}")
    except Exception as e:
        print(f"\n❌ Extrair tabela: Erro ao processar o PDF: {e}")

    return ""