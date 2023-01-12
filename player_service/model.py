from pydantic import BaseModel, EmailStr, Field

class Player(BaseModel):
    team_id: str
    first_name: str = Field(min_length=1, max_length=32)
    last_name: str = Field(min_length=1, max_length=32)
    email: EmailStr
    phone: str = Field(
        strip_whitespace=True,
        regex=r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$",
    )
    position: str = Field(
        strip_whitespace=True,
        regex=r"^[DELANTERO|MEDIO|DEFENSA|PORTERO]$",
    )

    def to_json(self):
        return {
            "team_id": self.team_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position
        }
