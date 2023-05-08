from config import Config
from .objects.user import User


class ApiContract:
    """
    api contract for api interfaces
    """

    def __init__(self, inbound: str):
        self.config = Config()
        self.inbound = inbound

    def get_users(self) -> list[User]:
        """
        fetch data from api server
        initiating fetch process
        """

        pass

    def report_config(self) -> str:
        """
        report current node to the server for distribution between clients
        """

        pass

    def report_usage(self, usages: list[User]) -> None:
        """
        report users usage
        """
        pass
