from pydantic import BaseModel, EmailStr, Field

class Player(BaseModel):
    team_id: int
    first_name: str = Field(min_length=0, max_length=32)
    last_name: str = Field(min_length=0, max_length=32)
    email: EmailStr
    position: str = Field(
        strip_whitespace=True,
        regex=r"DELANTERO|MEDIO|DEFENSA|PORTERO",
    )

    def to_json(self):
        return {
            "team_id": self.team_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "position": self.position
        }

class Match(BaseModel):
    id: str
    user_id: int
    opponent: str
    is_local: bool
    alignment: str
    url: str
    city: str
    weather: str
    start_date: str
    sent_email: str 