from time import sleep

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

        api.report_usage(connection.get_stats())

        users = api.get_users()
        connection.apply_update(users)

        sleep(config.get('usages.interval'))


if __name__ == '__main__':
    main()
