class DistinctBackendInformation:
    def __init__(self, host: str, username: str, password: str, uuid: str = None):
        self.host = host
        self.username = username
        self.password = password
        self.uuid = None
