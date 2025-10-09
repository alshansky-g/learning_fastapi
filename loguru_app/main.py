import random
import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

app = FastAPI()
fmt = ""
logger.remove()
logger.add("log_file.log", serialize=True, backtrace=False)
logger.add(sys.stdout, serialize=True, backtrace=False)


class CustomAppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    status_code = getattr(exc, "code", None) or 500
    message = getattr(exc, "message", "no message")
    logger.error("method={}, path={}, status={}",
                 request.method, request.url.path, status_code)
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code, "message": message})


@app.get("/ok")
async def ok(request: Request):
    print(request.method, request.url.path)
    return {"status": "ok"}


@app.get("/error")
async def error():
    raise CustomAppError("Возникло недоразумение", code=418)


# Маршрут для проверки случайного необработанного исключения (ожидается 500)
@app.get("/boom")
async def boom():
    def div_by_zero():
        return 1 / 0

    def key_err():
        return {}["missing"]

    def value_err():
        return int("not-an-int")

    def runtime_err():
        raise RuntimeError("Случайная ошибка")

    random.choice([div_by_zero, key_err, value_err, runtime_err])()
    return {"status": "unreachable"}
