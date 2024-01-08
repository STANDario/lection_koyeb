from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class OwnerModel(BaseModel):
    email: EmailStr


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DogModel(BaseModel):
    nickname: str = Field("Mur4ik", min_length=3, max_length=16)
    age: int = Field(1, ge=0, le=30)
    vaccinated: bool = False
    description: str
    owner_id: int = Field(1, gt=0)


class DogResponse(BaseModel):
    id: int = 1
    nickname: str
    age: int
    vaccinated: bool
    description: str
    owner: OwnerResponse

    class Config:
        orm_mode = True


class DogVaccinatedModel(BaseModel):
    vaccinated: bool = False


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserDb(BaseModel):
    id: int = 1
    username: str
    email: str
    avatar: str
    roles: Role

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
