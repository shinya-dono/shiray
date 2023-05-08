import json

from .ApiContract import ApiContract
import requests

from .objects.user import User


class NewV2board(ApiContract):
    def get_users(self):
        url = self.config.get(f"xray.inbounds.{self.inbound}.urls.fetch")
        req = requests.post(url)

        data = []

        if 'users' not in req.json():
            return data

        for user in req.json()['users']:
            data.append(User(user['id'], f"{user['uuid']}@mail.com", user['uuid']))

        return data

    def report_usage(self, usages: list[User]) -> bool:
        data = {}
        for usage in usages:
            data[f"{usage.id}"] = [usage.upload, usage.download]

        url = self.config.get(f"xray.inbounds.{self.inbound}.urls.push")

        req = requests.post(url, data=json.dumps(data), allow_redirects=True,
                            headers={"content-type": "application/json"})

        return req.status_code == 200
