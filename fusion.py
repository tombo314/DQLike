# クラスのインポート
from json_import import *

class Fusion:
    """
    モンスターを配合する
    """
    def __init__(self) -> None:
        """
        モンスターの配合に関する情報を持つ
        """
    
    def show_fusion_screen(self) -> None:
        """
        配合画面を表示する
        """
    
    def get_makeable_monster(self, monster: str) -> None:
        """
        モンスターの配合候補を返す
        monster: 親の片方となるモンスター
        """
        return fusion_tree[monster]

fusion = Fusion()