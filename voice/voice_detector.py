
import pyaudio
import websockets
import asyncio
import base64
import json
from configure import auth_key
import pyttsx3
from websocket_client import WebSocketClient


FRAMES_PER_BUFFER = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

class VoiceDetector:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        p = pyaudio.PyAudio()

        # starts recording
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )

        # the AssemblyAI endpoint we're going to hit
        URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
        self.wsclient = WebSocketClient("ws://localhost:8765")

    async def send_receive():
        print(f'Connecting websocket to url ${URL}')
        async with websockets.connect(
                URL,
                extra_headers=(("Authorization", auth_key),),
                ping_interval=5,
                ping_timeout=20
        ) as _ws:
            await wsclient.connect()
            await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")

            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data": str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)

                return True

            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        json_result = json.loads(result_str)
                        if json_result['message_type'] == 'FinalTranscript':
                            print(json_result['text'])
                            await wsclient.send_message({
                                'name': 'Text',
                                'text': json_result['text']
                            })

                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"

            async def receive_message():
                await wsclient.receive_message()

            await asyncio.gather(send(), receive(), receive_message())