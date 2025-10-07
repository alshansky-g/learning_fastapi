from fastapi import HTTPException


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str = 'ошибка а', status_code: int = 422,
                 message: str = 'Увы, произошла ошибка а'):
        super().__init__(detail=detail, status_code=status_code)
        self.message = message


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str = 'ошибка б', status_code: int = 418,
                 message: str = 'Увы, произошла ошибка б'):
        super().__init__(detail=detail, status_code=status_code)
        self.message = message
