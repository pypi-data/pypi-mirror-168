import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    profile_id: int
    picture: str
    description: str
    private: bool
    email: str
    username: str
    password: str
    ime: str
    prezime: str
    telefon: str
    datumRodjenja: datetime.date
    pol: str
    role: str
