from beautifulsoup_scraping import BeautifulsoupScraper
from selenium_scraping import SeleniumScraper
from abc_scraping import AbcScraping


# メイン関数
def main():
    # 各インスタンスのscrapingを実行
    bs : BeautifulsoupScraper = BeautifulsoupScraper()
    ss : SeleniumScraper = SeleniumScraper()
    scraping_list : list[AbcScraping]= [bs,ss]
    
    for s in scraping_list:
        print(s.scraping())


if __name__ == "__main__":
    main()