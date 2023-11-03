import pyaudio
import websockets
import asyncio
import base64
import json
from configure import Configure
import pyttsx3
import threading

FRAMES_PER_BUFFER = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


class SpeechToText:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.stream = None
        self.URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self.auth_key = Configure.instance().auth_key()
        self.running = True
        self.callback = None
        self._ws = None

    def set_callback(self, callback):
        self.callback = callback
    
    def _start_recording(self):
        p = pyaudio.PyAudio()
        self.stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )

    def _stop_recording(self):
        self.stream.close()
        self.stream = None

    async def connect(self):
        self._ws = await websockets.connect(
            self.URL,
            extra_headers=(("Authorization", self.auth_key),),
            ping_interval=5,
            ping_timeout=20
        )
        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")
        session_begins = await self._ws.recv()
        print(session_begins)
        print("Sending messages ...")

    async def disconnect(self):
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def send(self):
        while self.running:
            try:
                data = self.stream.read(FRAMES_PER_BUFFER)
                data = base64.b64encode(data).decode("utf-8")
                json_data = json.dumps({"audio_data": str(data)})
                await self._ws.send(json_data)
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except Exception as e:
                assert False, f"Not a websocket 4008 error: {str(e)}"
            await asyncio.sleep(0.01)

        return True

    async def receive(self):
        while self.running:
            try:
                result_str = await self._ws.recv()
                json_result = json.loads(result_str)
                if json_result['message_type'] == 'FinalTranscript':
                    print(json_result['text'])
                    if self.callback:
                        await self.callback(json_result['text'])
            except websockets.exceptions.ConnectionClosedError as e:
                print(e)
                assert e.code == 4008
                break
            except Exception as e:
                assert False, f"Not a websocket 4008 error: {str(e)}"
    
    async def run(self):
        self.running = True
        await self.connect()
        self._start_recording()
        await asyncio.gather(self.send(), self.receive())

    async def stop(self):
        self.running = False
        await self.disconnect()
        self._stop_recording()

    def set_running(self, flag: bool):
        self.running = flag
        print(f"after set running: {self.running}")
        
def print_callback(text):
    print("Recognized Text:", text)

def run_speech_to_text(stt):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stt.run())

if __name__ == "__main__":
    stt = SpeechToText()
    stt.set_callback(print_callback)

    thread = threading.Thread(target=run_speech_to_text, args=(stt,))
    thread.start()
    thread.join()
