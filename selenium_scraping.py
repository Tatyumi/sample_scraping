import re
import datetime
from abc_scraping import AbcScraping
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from chrome_driver import ChromeDriver
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement



# seleniumを利用したScrapingクラス
# ハードコーディングになって申し訳ないです
# ラ・ジェントステイ札幌大通りの宿泊料金を取得しています。
class SeleniumScraper(AbcScraping):
    # コンストラクタ
    def __init__(self) -> None:
        pass
        
    
    # スクレイピング処理   
    def scraping(self) -> str:
        # 対象のURL
        target_url : str = "https://asp.hotel-story.ne.jp/ver3d/ASPP0200.asp?hidSELECTCOD1=74910&hidSELECTCOD2=001&hidSELECTPLAN=A0FFI&pac=R/C&hidSELECTARRYMD=&hidSELECTHAKSU=1&rooms=1&selectptyp=00033&selectppsn=&hidk=&reffrom=&LB01=server11&DispUnit=room"
        
        # ページ読み込み
        cd : ChromeDriver  = ChromeDriver(target_url=target_url)
        driver : webdriver = cd.load_web_page()
        
        # ページ読み込みが成功したか判別
        if driver is None:
            # 失敗した場合
            return None
            
        # 今日の日にちを取得
        dt_now : datetime = datetime.datetime.now()
        today  : int      = dt_now.day
        
        # 対象の宿泊料金
        target_price : str = None
    
        try:
            # カレンダー要素を取得
            calender_element : webdriver = driver.find_element(by=By.ID,value="calendarleft")
            
            # カレンダー要素から宿泊料金を取得
            tds : list = calender_element.find_elements(by=By.CSS_SELECTOR,value="td")
            
            for td in tds:
                # カレンダーから日付の要素を取得
                day : WebElement = td.find_element(by=By.CSS_SELECTOR,value="strong")
                
                # 日付要素が本日の日にちを同一か判別
                if(day.text.isspace()==False and today == int(day.text)):
                    # 同一の場合
                    
                    # 文字列を精査して宿泊料金を取得
                    sub_re_text : str = re.sub(r"\\n","",repr(td.text))
                    # 抽出開始文字
                    char : str = "￥"
                    # char以降の文字列抽出
                    idx : int = sub_re_text.find(char)
                    target_price = sub_re_text[idx+1:]
                    break
                
        except NoSuchElementException as ex:
            # 要素が取得できなかった場合
            print("要素が取得できませんでした。")
            # プログラム終了
            return None
                   
        finally:
            # 開かれたウィンドウとドライバーの終了
            driver.quit()

        return re.sub(r"\D", "", target_price)