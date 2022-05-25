from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from config_reader import ConfigReader
from webdriver_manager.chrome import ChromeDriverManager
 


# クロームドライバークラス
class ChromeDriver():
    # コンストラクタ
    def __init__(self,target_url : str=None) -> None:
        # 対象のURL
        self.target_url : str = target_url
        
        
    # ページ読み込み関数
    def load_web_page(self, element_load_time:int=8) -> webdriver:
        
        # ドライバー生成
        # Webドライバーが正しいバージョンでない場合、「C:\Users\USERNAME\.wdm ~」配下に自動でインストール
        driver : webdriver.Chrome = webdriver.Chrome(ChromeDriverManager(log_level=0).install())
        
        # config.iniで設定されたロード時間取得
        cr = ConfigReader()
        page_load_time : int = cr.get_int_value("WaitTime")
        retry_count : int = cr.get_int_value("RetryCount")
        
        # リトライ回数が0より少ないか判別
        if retry_count <= 0:
            # 0より少ない場合
            retry_count = 1
        
        # ページ読み込み時間指定
        driver.set_page_load_timeout(page_load_time)
        
        # 指定回数ページ読み込み
        for _ in range(retry_count):
            
            try:
                driver.get(self.target_url)
                # 読み込み完了した場合
                break
            except TimeoutException as ex:
                # 指定時間内に読み込めない場合
                print("タイムアウト")
                pass
        else:
            # 指定回数内に呼び込みができなかった場合
            print("ページを取得できませんでした")
            # 終了処理
            return None
            
    
        # 要素読み込み時間設定
        driver.implicitly_wait(element_load_time)
        
        return driver