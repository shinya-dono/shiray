import json

import var_dump

from api.new_v2board import NewV2board
from config import Config
import subprocess

from service.xray import Xray


def main() -> None:
    config = Config()

    inbounds = config.get('xray.inbounds')

    connections: list[Xray] = []

    json_config = config.get('xray.default')

    for inbound_name in inbounds:
        json_config['inbounds'].append(inbounds[inbound_name]['config'])
        connections.append(Xray(inbound_name))

    with open('xray.json', 'w') as file:
        json.dump(json_config, file)

    subprocess.Popen(
        [
            './bin/xray',
            '-c',
            'xray.json'
        ]
    )

    for connection in connections:
        users = NewV2board(connection.inbound).get_users()

        var_dump.var_dump(NewV2board(connection.inbound).get_users())
        connection.apply_update(users)


if __name__ == '__main__':
    main()
