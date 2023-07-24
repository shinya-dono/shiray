from time import sleep

import requests

from api.new_v2board import NewV2board
from api.v2board import V2board
from config import Config
from service.ssh import SSH

from service.xray import Xray


def main() -> None:
    config = Config()
    print("starting")

    if config.get(f"protocol") == "ssh":
        connection = SSH("inbound")
    else:
        connection = Xray("inbound")

    print("started")

    while True:

        if config.get("server.type") == "v2board":
            api = V2board("inbound")
        else:
            api = NewV2board("inbound")

        try:
            api.report_usage(connection.get_stats())

            users = api.get_users()
            connection.apply_update(users)
        except requests.exceptions.ConnectTimeout:
            pass

        sleep(config.get('usages.interval'))


if __name__ == '__main__':
    main()
