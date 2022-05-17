from abc import ABCMeta, abstractmethod


# スクレイピング抽象クラス
# インターフェイスの役割で利用している
class AbcScraping(metaclass=ABCMeta):
    # コンストラクタ
    @abstractmethod
    def __init__(self) -> None:
        pass


    # スクレイピング処理
    @abstractmethod
    def scraping(self) -> str:
        pass
        
        