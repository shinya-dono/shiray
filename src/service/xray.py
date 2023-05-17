from xtlsapi import XrayClient, utils, exceptions

from api.objects.user import User
from config import Config


class Xray:

    def __init__(self, inbound: str):
        self.inbound = inbound
        self.config = Config()
        self.controller = XrayClient(self.config.get("xray.api.address"), self.config.get("xray.api.port"))
        self.users: list[User] = []

    def apply_update(self, users: list[User]):

        users_to_be_added = [user for user in users if user.uuid not in [x.uuid for x in self.users]]
        users_to_be_removed = [user for user in self.users if user.uuid not in [x.uuid for x in users]]

        self.users = [user for user in self.users if user not in [x.uuid for x in users_to_be_removed]] + users_to_be_added

        for user in users_to_be_added:
            self.controller.add_client(self.inbound, user.uuid, user.email, self.config.get(f"xray.inbound.protocol"))

        for user in users_to_be_removed:
            self.controller.remove_client(self.inbound, user.email)

        print(f"added {len(users_to_be_added)} users")
        print(f"removed {len(users_to_be_removed)} users")

    def get_stats(self):
        users = []
        for user in self.users:

            download = (1 - self.config.get('usages.disable_download')) * self.controller.get_client_download_traffic(user.email, True)
            upload = (1 - self.config.get('usages.disable_upload')) * self.controller.get_client_upload_traffic(user.email, True)

            if (upload + download) > self.config.get("usages.min"):
                user.set_usage(download, upload)
                users.append(user)

        return users
