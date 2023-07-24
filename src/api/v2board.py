import json

from .ApiContract import ApiContract
import requests

from .objects.user import User


class V2board(ApiContract):
    def get_users(self):
        url = self.get_url("user")

        req = requests.post(url)

        data = []

        if 'data' not in req.json():
            return data

        for user in req.json()['data']:
            try:
                data.append(User(user['id'], user['v2ray_user']['email'], user['v2ray_user']['uuid']))
            except:
                continue

        return data

    def get_url(self, node_type="submit"):
        protocol = self.config.get("protocol")
        host = self.config.get("server.host")
        token = self.config.get("server.token")
        node_id = self.config.get("server.id")

        path = "/api/v1/server/Deepbwork/"

        if protocol == "trojan":
            path = "/api/v1/server/TrojanTidalab/"
        if protocol == "shadowsocks":
            path = "/api/v1/server/ShadowsocksTidalab/"

        url = f"https://{host}{path}{node_type}?token={token}&node_id={node_id}"
        return url

    def report_usage(self, usages: list[User]) -> bool:
        data = []
        for usage in usages:
            data.append({"u": usage.upload, "d": usage.download, "user_id": usage.id})

        url = self.get_url("submit")

        req = requests.post(url, data=json.dumps(data), allow_redirects=True,
                            headers={"content-type": "application/json"})

        return req.status_code == 200
