
from websocket_client import WebSocketClient
from speech_to_text import SpeechToText
import asyncio
import threading
from configure import Configure


class VoiceDetector:
    def __init__(self) -> None:
        self.ws_cli = WebSocketClient(Configure.instance().wsserver_url())
        self.speech_to_text = SpeechToText()
        self.speech_to_text.set_callback(self.handle_callback)
        self.speech_thread = None
        self.running = False
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def _run_in_event_loop(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.speech_to_text.run())
        print("exit event loop................")

    def run(self):
        self.speech_thread = threading.Thread(
            target=self._run_in_event_loop, args=()
        )
        self.speech_thread.start()
        self.running = True
        self.speech_thread.join()

    async def handle_callback(self, text: str) -> None:
        print(f"{text}")
        if self.callback:
            self.callback(text)

    def stop(self) -> None:
        self.speech_to_text.stop()
        print("Thread has111111111 stopped")


if __name__ == "__main__":
    voice_detector = VoiceDetector()
    voice_detector.run()