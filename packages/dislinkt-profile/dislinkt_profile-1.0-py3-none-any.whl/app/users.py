from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    ime: str
    prezime: str
    telefon: str
    datumRodjenja: str
    pol: str


class ProfileCreate(BaseModel):
    user_id: str
    private: bool


class ProfileEdit(BaseModel):
    user_id: str
    private: bool
    description: str


class EducationCreate(BaseModel):
    profile_id: str
    school: str
    degree: str
    start: str
    end: str
