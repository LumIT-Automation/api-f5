class CustomException(Exception):
    def __init__(self, status: int, payload: dict):
        self.status = int(status)
        self.payload = payload

    def status(self):
        return self.status

