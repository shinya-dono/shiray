import crypt
import os
import re
import subprocess

from api.objects.user import User
from config import Config


class SshController:

    def __init__(self):
        self.executor = os.system
        self.exec_and_read = subprocess.run

    def add_client(self, name, username, password):
        enc_pass = crypt.crypt(password, "22")
        return self.executor(
            f"useradd -p {enc_pass} -s /bin/true -d {username} -m -c \"{name}\" username"
        )

    def get_connections(self):
        return self.exec_and_read(["lsof", "-i", ":22", "-n"], capture_output=True, text=True).stdout.split("\n")

    def remove_client(self, username):
        return self.executor(f"killall -u {username} && userdel {username}")


class SSH:
    def __init__(self, inbound: str):
        self.inbound = inbound
        self.controller = SshController()
        self.config = Config()
        self.users: list[User] = []

    def apply_update(self, users: list[User]):

        users_to_be_added = [user for user in users if user.uuid not in [x.uuid for x in self.users]]
        users_to_be_removed = [user for user in self.users if user.uuid not in [x.uuid for x in users]]

        self.users = [user for user in self.users if
                      user not in [x.uuid for x in users_to_be_removed]] + users_to_be_added

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
        list_of_connections = self.controller.get_connections()

        ssh_users = [int(re.search("user(\d+)", x).group(1)) for x in list_of_connections if re.search("user(\d+)", x)]
        users = []

        for user in self.users:
            if user.id in ssh_users:
                user.set_usage(1, 1)
                users.append(user)

        return users
