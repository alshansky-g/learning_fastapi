from fastapi import FastAPI, status

from exceptions_app.exception_handlers import custom_exception_a_handler, custom_exception_b_handler
from exceptions_app.exceptions import CustomExceptionA, CustomExceptionB
from exceptions_app.schemas import ResponseErrorA, ResponseErrorB

app = FastAPI()
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)  # type: ignore
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)  # type: ignore


@app.get("/{letter}",
         summary="Получить обратно букву",
         description="Возвращает ту же букву, что вы отправляете. Абсолютно бесполезно.",
         responses={
            status.HTTP_400_BAD_REQUEST: {"model": ResponseErrorA},
            status.HTTP_418_IM_A_TEAPOT: {"model": ResponseErrorB}
         })
async def endpoint_a(letter: str):
    if letter.lower() == 'a':
        raise CustomExceptionA
    elif letter.lower() == 'b':
        raise CustomExceptionB
    return {"letter": letter}
