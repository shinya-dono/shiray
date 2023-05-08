class User:

    def __init__(self, site_id: int, email: str, uuid: str):
        self.id = site_id
        self.email = email
        self.uuid = uuid
        self.upload = 0
        self.download = 0

    def set_usage(self, download: int, upload: int):
        self.download = download
        self.upload = upload
        return self

    def __str__(self):
        return self.email
