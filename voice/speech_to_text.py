import pyaudio
import base64
import json
from configure import Configure
import pyttsx3
import threading


from ws_client import WSClient

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
        self._ws_cli = WSClient(self.URL, header={"Authorization": self.auth_key})
        self._ws_cli.set_handle_message_cb(self.handle_message)

    def handle_message(self, message):
        json_result = json.loads(message)
        if json_result['message_type'] != 'FinalTranscript':
            return
        
        final_script = json_result['text']
        if self.callback:
            self.callback(final_script)
        else:
            print(f"speech to text recieved: {final_script}")

    def set_callback(self, callback):
        self.callback = callback
    
    def _open_audio(self):
        self.p_audio = pyaudio.PyAudio()
        self.stream = self.p_audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )

    def _close_audio(self):
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.p_audio.terminate()

    def read_data_from_audio(self):
        data = self.stream.read(FRAMES_PER_BUFFER)
        data = base64.b64encode(data).decode("utf-8")
        json_data = json.dumps({"audio_data": str(data)})
        return json_data
    
    def run(self):
        self.running = True
        self._open_audio()
        self.text_thread = threading.Thread(target=self._ws_cli.run)
        self.text_thread.start()
        print("Start Listening.......")
        while self.running:
            try:
                json_data = self.read_data_from_audio()
                self._ws_cli.send_message(json_data)
            except Exception as e:
                print(f"while running speech to text, got a exception: {str(e)}")
                break
        print("End speech to text loop...")
    
    def stop(self):
        try:
            self.running = False
            # self._close_audio()
            self._ws_cli.manual_close()
            self.text_thread.join()
            print("Stop success.")

        except Exception as e:
            print(f"Stop speech to text got a exception: {str(e)}")
