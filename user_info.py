# クラスのインポート
from json_import import *

class UserInfo:
    """
    プレイヤーの情報を管理する
    """
    def __init__(self) -> None:
        # 味方パーティー
        self.friend = [None]*3

    def set_friend(self, friend: list[str]) -> None:
        """
        自分のパーティーを設定する
        """
        self.friend = friend
        # パーティー内でモンスターの重複があったら終了
        if len(set(self.friend))<=2:
            print("味方パーティー内でモンスターが重複しています。")
            exit()

user_info = UserInfo()