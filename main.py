from coletor_de_links import crawler
from coletor_de_links import scraper

def main():
    links = crawler()
    scraper(links)
    print("Coleta de links concluída.")

if __name__ == "__main__":
    main()