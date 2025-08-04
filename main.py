from crawler import crawler, crawler_lattes
from scraper import scraper, scraper_lattes

def main():
    links = crawler()
    scraper(links)
    crawler_lattes()
    
if __name__ == "__main__":
    main()