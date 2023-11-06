import websocket
import threading
import rel


class WSClient:
    def __init__(self, url: str, header: dict={}) -> None:
        self.url = url
        self.WS = websocket.WebSocketApp(
            url,
            header=header,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        self.callback = None

    def set_handle_message_cb(self, callback):
        self.callback = callback
    
    def send_message(self, message):
        self.WS.send(message)

    def manual_close(self):
        self.WS.close()
        print("manually close")

    def on_message(self, ws, message):
        if self.callback:
            self.callback(message)
        else:
            print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"close status code: {close_status_code}")

    def run(self):
        websocket.enableTrace(False)
        self.WS.run_forever()
        # self.WS.run_forever(dispatcher=rel, reconnect=5)
        # rel.signal(2, rel.abort)  # Keyboard Interrupt
        # rel.dispatch()