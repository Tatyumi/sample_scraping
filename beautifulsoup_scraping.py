import requests
import re
from abc_scraping import AbcScraping
from requests.exceptions import Timeout
from bs4 import BeautifulSoup, ResultSet
from config_reader import ConfigReader



# beautifulsoupを利用したスクレイピングクラス
# ハードコーディングになって申し訳ないです
# APAホテルのツインプランの宿泊料金を取得しています
class BeautifulsoupScraper(AbcScraping):
    # コンストラクタ
    def __init__(self) -> None:
        pass
        
        
    # スクレイピング処理
    def scraping(self)->str:
        # 対象のURL
        target_url : str = "https://www.apahotel.com/hotel/hokkaido-tohoku/hokkaido/sapporo/pricelist/"
        # ヘッダ情報
        header_dic : dict[str,str] = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        
        # config.iniで設定された待機時間、リトライ回数取得
        cr = ConfigReader()
        wait_time : int = cr.get_int_value("WaitTime")
        retry_count : int = cr.get_int_value("RetryCount")
        
        # サーバー接続までの待機時間
        connect_wait_time : int = wait_time
        # バイト送信してからの待機時間
        read_wait_time : int = wait_time
        
        # レスポンスデータ
        res : requests.Response = None
        
        # リトライ回数が0より少ないか判別
        if retry_count <= 0:
            # 0より少ない場合
            retry_count = 1
        
        # 指定回数ページ読み込み
        for _ in range(retry_count):
            try:
                # 対象URLのレスポンスを取得
                res = requests.get(target_url, headers=header_dic, timeout=(connect_wait_time, read_wait_time))
                break
                
            except Timeout as time_ex:
                # タイムアウトした場合
                print("タイムアウト")
        else:
            # 指定回数内に読み込めなかった場合
            print("ページを取得できませんでした")
            return None
        
        try:
            # レスポンスの状態チェック
            res.raise_for_status()
            
        except requests.exceptions.RequestException as req_ex:
            # レスポンス結果がエラーの場合
            print("リクエストエラー")
            return None

        # レスポンスデータから客室通常料金のテーブルを取得
        soup : BeautifulSoup = BeautifulSoup(res.text, "html.parser")
        soup.find("table").find_all("tr")
        plan_list : ResultSet      = soup.find_all("th")
        hotel_fee_list : ResultSet = soup.find_all("td")

        # 対象のプラン名
        target_plan_name : str = "ツイン"
        # ツインの宿泊価格を取得
        target_hotel_fee : str = None
        
        # 対象のプランを捜索
        for plan, price in zip(plan_list, hotel_fee_list):
            # プランの判別
            if plan.getText() == target_plan_name:
                #対象のプランの場合
                #宿泊料金を取得
                target_hotel_fee = price.getText()
                break

        # 宿泊料金を返す
        return  re.sub(r"\D","", target_hotel_fee)