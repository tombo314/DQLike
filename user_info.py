class UserInfo:
    """
    プレイヤーの情報を管理する
    """
    def __init__(self) -> None:
        # 味方パーティー
        self.friend = []

    def set_friend(self, friend: list[dict]) -> None:
        """
        味方パーティーを設定する
        """
        # 味方パーティーを設定する
        self.friend = friend.copy()
        # パーティー内でモンスターの重複があったら終了
        a = []
        for mons in self.friend:
            a.append(mons["name"])
        if len(set(a))<=2:
            print("味方パーティー内でモンスターが重複しています。")
            exit()

user_info = UserInfo()