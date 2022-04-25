import json

class Observer:
    def __init__(self,ws):
        self.ws = ws

    def send_finish(self):
        print('send_finish')
        data = {
            'type': 'current',
            'value': 1
        }
        self.ws.send(json.dumps(data))

    def send_max(self,max):
        print('send_max')
        data = {
            'type': 'max',
            'value': max
        }
        self.ws.send(json.dumps(data))

    def complete(self):
        print('send_complete')
        data = {
            'type': 'complete',
            'value': True
        }
        self.ws.send(json.dumps(data))