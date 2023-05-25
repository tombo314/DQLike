class Window:
    """
    UIを表示する
    """
    def __init__(self) -> None:
        """
        画面にUIを表示する
        """
        self.message_box = None
        self.message_text = None
        self.button = [None]*3
        self.enemy = [None]*3
        self.log_text = [None]*15
    
    def make_message_box(self) -> None:
        """
        メッセージボックスを生成する
        """
        start_x, start_y = 90, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_box = canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#eee",
            outline = "#777"
        )
        canvas.update()
    
    def show_message(self, message: str, is_fast: bool, log_list: list[str]) -> None:
        """
        メッセージを表示（変更）する
        message: 表示するメッセージ
        is_fast: 表示間隔を短くするかどうか
        log_list: 表示するログのリスト
        """
        # メッセージを表示する
        # すでにメッセージが書いてある場合は消去する
        if self.message_text is not None:
            canvas.delete(self.message_text)
        # メッセージを表示する
        start_x, start_y = 70, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_text = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            font = ("helvetica", 18),
            text = message
        )
        # ログを表示する
        LOG_NUM = 15
        # すでにログが書いてある場合は削除する
        for i in range(LOG_NUM):
            canvas.delete(self.log_text[i])
        # ログを出力する
        if log_list is not None:
            log_list.append(message)
            if len(log_list)>LOG_NUM:
                log_list.pop(0)
            for i,content in enumerate(log_list):
                start_x, start_y = 950, 27*(i+1)
                width, height = 100, 30
                end_x, end_y = start_x+width, start_y+height
                self.log_text[i] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    font = ("helvetica", 12),
                    text = content
                )
        canvas.update()
        if is_fast==True:
            sleep(SHOW_DURATION*0.3)
        elif is_fast==False:
            sleep(SHOW_DURATION)
