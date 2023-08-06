class FileLoadException(Exception):
    def __init__(self, message: str):
        self.message = message


class InvalidConfigurationException(Exception):
    def __init__(self, message: str):
        self.message = message


class BrowserAuthException(Exception):
    def __init__(self, message: str):
        self.message = message


class BigConfigValidationException(Exception):
    def __init__(self, message: str):
        self.message = message


class NoSourcesFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
