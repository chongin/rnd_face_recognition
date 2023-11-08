
from websocket_client import WebSocketClient
from speech_to_text import SpeechToText
import asyncio
import threading
from configure import Configure
import time
from ws_client import WSClient


class VoiceDetector:
    def __init__(self) -> None:
        self.speech_to_text = SpeechToText()
        self.speech_to_text.set_callback(self.handle_text_from_speech)

        self.callback = None
        self.text_to_speech_cli = WSClient(Configure.instance().wsserver_url())
        self.text_to_speech_cli.set_handle_message_cb(self.handle_message_from_server)

    def is_running(self):
        return self.speech_to_text.is_running()

    def set_callback(self, callback):
        self.callback = callback

    def run_loop(self):
        self.speech_to_text.run()

    def stop(self):
        self.speech_to_text.stop()

    def handle_text_from_speech(self, text: str) -> None:
        if self.callback:
            self.callback(text)
        else:
            print(f"Recognize: {text}")

        try:
            self.text_to_speech_cli.send_message(text)
        except Exception as e:
            print(f"Handle text from speech error: str{e}")

    def handle_message_from_server(self, text: str):
        if self.callback:
            self.callback(text)
        else:
            print(f"From server: {text}")


if __name__ == "__main__":
    voice_detector = VoiceDetector()
    speech_thread = threading.Thread(
        target=voice_detector.run_loop, args=()
    )

    speech_thread.start()
    t1 = threading.Thread(target=voice_detector.speech_to_text.stop)
    time.sleep(15)
    t1.start()

    speech_thread.join()
    print("End speech running thread......")
    t1.join()
    print("End stop speech thread......")