import json

from .ApiContract import ApiContract
import requests

from .objects.user import User


class NewV2board(ApiContract):
    def get_users(self):
        url = self.get_url("user")
        req = requests.post(url)

        data = []

        if 'users' not in req.json():
            return data

        for user in req.json()['users']:
            try:
                data.append(User(user['id'], f"{user['uuid']}@mail.com", user['uuid']))
            except:
                continue

        return data

    def get_url(self, node_type="push"):
        protocol = self.config.get("protocol")
        host = self.config.get("server.host")
        token = self.config.get("server.token")
        node_id = self.config.get("server.id")

        path = "/api/v1/server/UniProxy/"

        if protocol == "vless" or protocol == "vmess":
            protocol = "v2ray"

        url = f"https://{host}{path}{node_type}?token={token}&node_id={node_id}&node_type={protocol}"
        return url

    def report_usage(self, usages: list[User]) -> bool:
        data = {}
        for usage in usages:
            data[f"{usage.id}"] = [usage.upload, usage.download]

        url = self.get_url("push")

        req = requests.post(url, data=json.dumps(data), allow_redirects=True,
                            headers={"content-type": "application/json"})

        return req.status_code == 200
