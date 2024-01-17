from scr.core.errors import ValidationException

PWD_REQ_MSG = '''Двухфакторная авторизация не поддерживается, мы над этим работаем'''
ALREADY_LOGINED = '''Пользователь уже авторизован'''
SESSION_NO_FOUND = '''Сессия не найдена'''
NOT_AUTHORIZED = '''Клиент не авторизован'''
PHONE_INV_FORMAT = '''Номер телефона должен состоять из чисел'''


class PasswordRequired(ValidationException):
    def __init__(
        self, details: str = PWD_REQ_MSG,
        http_status_code: int = 400, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class AlreadyLogined(ValidationException):
    def __init__(
        self, details: str = ALREADY_LOGINED,
        http_status_code: int = 400, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class SessionNotFound(ValidationException):
    def __init__(
        self, details: str = SESSION_NO_FOUND,
        http_status_code: int = 404, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class NotAuthorized(ValidationException):
    def __init__(
        self, details: str = NOT_AUTHORIZED,
        http_status_code: int = 404, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)


class PhoneInvalidFormat(ValidationException):
    def __init__(
        self, details: str = PHONE_INV_FORMAT,
        http_status_code: int = 400, *args: object
    ) -> None:
        super().__init__(details, http_status_code, *args)
