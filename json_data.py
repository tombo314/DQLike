from json_import import import_json

class JsonData:
    """
    JSONファイルを読み込む
    """
    def __init__(self) -> None:
        self.save_data = None
        self.monster = None
        self.skill = None
        self.fusion_tree = None
    
    def load_json(self, save_data_id: int) -> None:
        """
        JSONファイルを読み込む
        save_data_id: セーブデータの番号
        """
        data = import_json(save_data_id)
        self.save_data = data["save_data"]
        self.monster = data["monster"]
        self.skill = data["skill"]
        self.fusion_tree = data["fusion_tree"]
    
    def select_save_data(self) -> None:
        """
        セーブデータ画面を表示する
        セーブデータをロードする
        """
        # debug
        print("セーブデータの番号を入力してください...")
        tmp = int(input())
        self.load_json(tmp)

json_data = JsonData()