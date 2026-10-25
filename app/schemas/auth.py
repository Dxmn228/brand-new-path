import re
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

PHONE_PATTERN = re.compile(r"^\+7\d{10}$")

class _PasswordValidatorsMixin(BaseModel):


    @field_validator("password", check_fields=False)
    @classmethod
    def validate_password(cls, v: str) -> str:
        if ((len(v) < 8) or (not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v))):
            raise ValueError ("Пароль должен минимум содержать: 8 символов, одну букву и одну цифру.")
        return v
    
    @field_validator("phone", check_fields=False)
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not PHONE_PATTERN.match(v):
            raise ValueError("Укажите номер в формате +7ХХХХХХХХХХ")
        return v

class _PasswordsMatchMixin(BaseModel):
    @model_validator (mode = "after")
    def passwords_match(self):
        if hasattr(self, "password") and hasattr(self, "password_confirm"):
            if self.password is not None and self.password != self.password_confirm:
                raise ValueError("Пароли не совпадают")
            return self

class UserRegister(_PasswordValidatorsMixin):

    full_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str
    password: str
    password_confirm: str

class OrganizationRegister(_PasswordValidatorsMixin):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str
    description: str = Field(default="", max_length=2000)
    website: str | None = Field(default=None, max_length=500)
    password: str
    password_confirm: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str="bearer"

class RefreshRequest(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    id: int
    full_name: int
    email: EmailStr
    phone: str
    
    model_config = {"from_atributes": True}

class OrganizationRead (BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    description: str
    website: str | None = None

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    full_name: str | None = Field(default = None, min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = None
    password: str | None = None
    password_confirm: str | None = None
    current_password: str | None = None

class OrganizationUpdate(BaseModel):
    """Схема для изменения профиля организации."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = None
    description: str | None = Field(default=None, max_length=2000)
    website: str | None = Field(default=None, max_length=500)
    password: str | None = None
    password_confirm: str | None = None
    current_password: str | None = None

class AccountDeleteRequest(BaseModel):
    password: str