from io import BytesIO
import re
import fitz
import pdfplumber
import requests
import unicodedata


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
        docentes = []
        with pdfplumber.open(BytesIO(resposta.content)) as pdf:
            for pagina in pdf.pages:
                tabelas = pagina.extract_tables()

                if not tabelas:
                    continue

                for tabela in tabelas:
                    if tabela and len(tabela[0])>1:
                        for linha in tabela:
                            if not linha or not linha[0]:  # ignora linhas vazias
                                continue
                            
                            texto_linha = " ".join([str(item) for item in linha if item])

                            if re.search(r"\b(Doutor|Mestre)\b", texto_linha):
                                if "bibliografia" in texto_linha.lower():
                                    continue
                               
                                nome = str(linha[0]).strip()
                                if (
                                    re.search(r'\d', nome) or
                                    ":" in nome or
                                    "(" in nome or
                                    ")" in nome or
                                    "," in nome or
                                    "." in nome or
                                    ";" in nome or
                                    "&" in nome or
                                    "%" in nome or
                                    re.search(r'\bI{1,3}\b', nome)  # detecta "I" ou "II" como palavra isolada
                                ):
                                    continue

                                nome = nome.replace("-", "")

                                nome_formatado = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', nome)
                                nome_formatado = " ".join(nome_formatado.split())
                                nome_normalizado = normalizar(nome_formatado)
                                if nome_normalizado not in [normalizar(d) for d in docentes]:
                                    docentes.append(nome_formatado)

        return "\n".join(docentes)

    except requests.exceptions.Timeout:
        print(f"\n⏳ Extrair tabela: Tempo esgotado ao tentar acessar: {url}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Extrair tabela: Erro de conexão ou download: {e}")
    except Exception as e:
        print(f"\n❌ Extrair tabela: Erro ao processar o PDF: {e}")

    return ""

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

