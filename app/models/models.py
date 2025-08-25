from pydantic import BaseModel, EmailStr, Field, field_validator

BAD_WORDS = ["редиск", "бяк", "козявк"]


class Contact(BaseModel):
    email: EmailStr
    phone: str | None = None

    @field_validator("phone")
    def check_phone(cls, phone: str):
        if phone is None:
            return phone
        if not phone.isdigit() or not 7 <= len(phone) <= 15:
            raise ValueError("Номер телефона должен состоять из 7-15 цифр")
        return phone


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    age: int | None = Field(None, ge=0, le=65)
    is_subscribed: bool | None = None


class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)
    contact: Contact

    @field_validator("message")
    def check_bad_words(cls, message: str):
        for word in BAD_WORDS:
            if word.lower() in message.lower():
                raise ValueError("Использование недопустимых слов")
        return message
