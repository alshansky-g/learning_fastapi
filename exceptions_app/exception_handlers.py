import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions_app.exceptions import CustomExceptionA, CustomExceptionB

logging.basicConfig(level=logging.INFO)


async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    logging.error('Ошибка: %s', exc.message)
    return JSONResponse(status_code=exc.status_code, content={'error': exc.message})


async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    logging.error('Ошибка: %s', exc.message)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})
