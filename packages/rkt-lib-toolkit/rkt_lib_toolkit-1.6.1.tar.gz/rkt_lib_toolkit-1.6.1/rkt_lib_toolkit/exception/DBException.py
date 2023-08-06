
class DBBaseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoSubKeyFoundError(DBBaseError):
    def __init__(self, msg: str = ''):
        self.msg = msg or "user isn't define in database yaml file"
        super().__init__(self.msg)


class NoDataError(DBBaseError):
    def __init__(self, msg: str = ''):
        self.msg = msg or "\nYour database yaml file does not contain the 'url' or 'connect_id' key.\n" \
                          "The 'connect_id' key must contain the following sub-keys 'dbms', 'user', 'password'" \
                            ", 'host', 'port'"
        super().__init__(self.msg)


