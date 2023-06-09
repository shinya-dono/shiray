from time import sleep

import requests
import xtlsapi

from api.new_v2board import NewV2board
from config import Config

from service.xray import Xray


def main() -> None:
    config = Config()
    print("starting")

    connection = Xray("inbound")

    print("started")

    while True:
        api = NewV2board(connection.inbound)
        try:
            api.report_usage(connection.get_stats())

            users = api.get_users()
            connection.apply_update(users)
        except requests.exceptions.ConnectTimeout:
            pass
        except xtlsapi.exceptions.email_already_exists.EmailAlreadyExists:
            pass

        sleep(config.get('usages.interval'))


if __name__ == '__main__':
    main()
