
class LoggerBaseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidLogLevelError(LoggerBaseError):
    def __init__(self, msg: str = ''):
        super().__init__(msg)


class LogIsNotDirError(LoggerBaseError):
    def __init__(self, msg: str = ''):
        super().__init__(msg)
