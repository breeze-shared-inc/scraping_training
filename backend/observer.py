import json
from flask_sock import Sock
class Observer:
    """
    フロントエンド側にスクレイピングの進行状況を通知するクラス

    Attributes
    ----------
    ws : Sock
        WebSocket
    """
    def __init__(self,ws: Sock) -> None:
        """
        Parameters
        ----------
        ws : Sock
            WebSocket
        """
        self.ws: Sock = ws

    def send_finish(self):
        """
        1記事の取得が完了したら通知する
        """
        print('send_finish')
        data = {
            'type': 'current',
            'value': 1
        }
        self.ws.send(json.dumps(data))

    def send_max(self,max: int) -> None:
        """
        最大記事数が確定したら通知するメソッド

        Parameters
        ----------
        max : int
            取得する記事の最大数
        """
        print('send_max')
        data = {
            'type': 'max',
            'value': max
        }
        self.ws.send(json.dumps(data))

    def complete(self) -> None:
        """
        全ての記事の取得が完了したら通知する
        """

        print('send_complete')
        data = {
            'type': 'complete',
            'value': True
        }
        self.ws.send(json.dumps(data))