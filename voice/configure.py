import json
import os


class Configure:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_manual__()
        return cls._instance
    
    def auth_key(self):
        return self.secret['auth_key']
    
    def wsserver_url(self):
        return self.config['wsserver_url']
    
    def __init_manual__(self) -> None:
        current_directory = self._get_current_directory_of_file(__file__)
        secret_path = f"{current_directory}/secret.json"
        with open(secret_path, 'r') as json_file:
            self.secret = json.load(json_file)

        config_path = f"{current_directory}/config.json"
        with open(config_path, 'r') as json_file:
            self.config = json.load(json_file)

    def _get_current_directory_of_file(self, file: str) -> str:
        current_script_path = os.path.abspath(file)
        current_directory = os.path.dirname(current_script_path)
        return current_directory