from pydantic import BaseModel


class Platform(BaseModel):
    id: int
    title: str
    id_name: str
