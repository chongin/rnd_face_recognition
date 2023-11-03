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
        return self.config['auth_key']

    def __init_manual__(self) -> None:
        config_path = f"{self._get_current_directory_of_file(__file__)}/secret.json"
        with open(config_path, 'r') as json_file:
            self.config = json.load(json_file)

    def _get_current_directory_of_file(self, file: str) -> str:
        current_script_path = os.path.abspath(file)
        current_directory = os.path.dirname(current_script_path)
        return current_directory