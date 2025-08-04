from crawler import crawler, crawler_lattes
from scraper import scraper, scraper_lattes

def main():
    links = crawler()
    scraper(links)
    texto, docentes = crawler_lattes()
    scraper_lattes(texto, docentes)
    
if __name__ == "__main__":
    main()