
class CDB:

    def __init__(self):
        self.value = None

    def __str__(self):
        return str(self.value)

    def put(self, value):
        self.value = value

    def get(self):
        return self.value