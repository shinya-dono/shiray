import json


class Config:

    def __init__(self):
        with open("config.json", "r") as file:
            self.data: dict = json.load(file)

    def get(self, config_key: str = "", default=None):

        keys = [x for x in config_key.split('.') if len(x) >= 1]

        data = self.data

        for key in keys:
            if key not in data:
                return default

            data = data.get(key)

            if not isinstance(data, dict):
                return data

        return data
