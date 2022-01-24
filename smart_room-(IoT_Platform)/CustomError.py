import string


class CustomError(Exception):
    def __init__(self, message: string):
        self.message = message
