from configparser import ConfigParser
import os
import sys
from pathlib import Path
from logging import getLogger



#configファイル読み取りクラス
class ConfigReader():
    # デフォルトセクション
    DEFAULT_SECTION : str ="DEFAULT"
    # エンコード
    ENCODING : str = "utf-8"
    
    # コンストラクタ
    def __init__(self) -> None:
        # コンフィグファイル
        CONFIG_INI : str = r"config.ini"
        # ディレクトリーパス
        dir_path : str = os.path.dirname(sys.argv[0])
        
        # コンフィグファイルパス生成
        self._config_path: str = Path(dir_path,CONFIG_INI)
        # 子インスタンス生成
        self._logger = getLogger("__main__").getChild(__name__)        
        
    
    # ゲッター
    @property
    def config_path(self) -> str:
        return self._config_path
    
    
    # int値の取得
    def get_int_value(self,key,section="USERSETTINGS") -> int:
        
        # コンフィグファイル読み取り
        config : ConfigParser = ConfigParser()
        config.read(Path(self._config_path),encoding=self.ENCODING)
        
        # 読み込めたかNoneチェックが必要
        if config == None:
            # 読み込めなかった場合
            # 強制終了
            self._logger.critical("config.iniが読み込めませんでした")
            exit()
        
        # 指定のセクションを取得
        target_config : str = config[section]
        
        target_value : int = 0
        # 数値であるか判別する必要あり
        try :
            # 指定のキーが持つ値を取得
            target_value = target_config.getint(key)
        except ValueError as ex:
            # 型違いによるエラーが起きた場合
            self._logger.error(section+":"+key +"の値が正しくありません。")
            
            # DEFAULTセクションで設定されている値を取得
            target_config = config[self.DEFAULT_SECTION]
            target_value  = target_config.getint(key)
        finally:
            return target_value