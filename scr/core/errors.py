class ValidationException(Exception):
    def __init__(
        self,
        details: str,
        http_status_code: int = 400,
        *args: object
    ) -> None:
        self.details = details
        self.http_status_code = http_status_code
        super().__init__(details, http_status_code, *args)
