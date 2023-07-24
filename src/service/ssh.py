import crypt
import os

from api.objects.user import User
from config import Config


class SshController:

    def __init__(self):
        self.executor = os.system

    def add_client(self, name, username, password):
        encPass = crypt.crypt(password, "22")
        return self.executor(
            "useradd -p " + encPass + " -s " + "/bin/true " + "-d " + "/home/" + username + " -m " + " -c \"" + name + "\" " + username)

    def remove_client(self, username):
        return self.executor("userdel " + username)


class SSH:
    def __init__(self, inbound: str):
        self.inbound = inbound
        self.controller = SshController()
        self.config = Config()
        self.users: list[User] = []

    def apply_update(self, users: list[User]):

        users_to_be_added = [user for user in users if user.uuid not in [x.uuid for x in self.users]]
        users_to_be_removed = [user for user in self.users if user.uuid not in [x.uuid for x in users]]

        self.users = [user for user in self.users if user not in [x.uuid for x in users_to_be_removed]] + users_to_be_added

        try:
            for user in users_to_be_added:
                self.controller.add_client(self.inbound, f"user{user.id}", user.uuid.replace("-", ""))

            for user in users_to_be_removed:
                self.controller.remove_client(f"user{user.id}")
        finally:
            pass

        print(f"added {len(users_to_be_added)} users")
        print(f"removed {len(users_to_be_removed)} users")

    def get_stats(self):
        users = []
        return users
