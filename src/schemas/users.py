from pydantic import BaseModel


class UsersSchema(BaseModel):
    id: int
    name: str
    age: int
