import json
from time import sleep

from api.new_v2board import NewV2board
from config import Config
import subprocess

from service.core import Core
from service.xray import Xray


def main() -> None:
    config = Config()
    print("starting")
    inbounds = config.get('xray.inbounds')

    connections: list[Xray] = []

    json_config = config.get('xray.default')

    for inbound_name in inbounds:
        json_config['inbounds'].append(inbounds[inbound_name]['config'])
        connections.append(Xray(inbound_name))

    with open('xray.json', 'w') as file:
        json.dump(json_config, file)

    # subprocess.Popen(["/code/bin/xray", "run", "-config", "/code/bin/xray.json"])

    Core().start()
    print("started")

    while True:

        for connection in connections:
            users = NewV2board(connection.inbound).get_users()

            connection.apply_update(users)

        sleep(60)


if __name__ == '__main__':
    main()
