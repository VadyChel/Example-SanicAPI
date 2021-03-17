class ExampleSanicAPIException(BaseException):
    pass


class UserAlreadyExists(ExampleSanicAPIException):
    pass


class UserNotFound(ExampleSanicAPIException):
    pass


class InvalidPassword(ExampleSanicAPIException):
    pass