class CustomException(Exception):
    def __init__(self, status: int, payload: dict = None):
        payload = payload or {}

        self.status = int(status)
        self.payload = payload



    def status(self):
        return self.status


    
    def __str__(self):
        return str(self.status)+", "+str(self.payload)
