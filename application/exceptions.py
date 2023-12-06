class SshConnectionException(Exception):
    def __init__(self, error):
        self.error = error


class TransportCreateException(Exception):
    def __init__(self, status, warns):
        self.status = status
        self.warns = warns
