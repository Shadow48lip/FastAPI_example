from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/pd", tags=["Pydantic примеры"])


class ItemSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@router.post("/post/")
async def create_item(item: ItemSchema):
    return [item, item.name]