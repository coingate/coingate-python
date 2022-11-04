from pydantic import BaseModel


class Currency(BaseModel):
    id: int
    title: str
    symbol: str
