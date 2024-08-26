class KeyNotExistException(Exception):
    def __init__(self, key):
        self.key = key
        self.message = f"Invalid key: {key}"
        super().__init__(self.message)