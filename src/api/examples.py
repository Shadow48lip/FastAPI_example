from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from src.schemas.items import ItemSchema

router = APIRouter(prefix="/pages", tags=["Example router"])


# http://127.0.0.1:8000/www/pages/p1?name=Vasya
@router.get("/p1")
async def page_1(name: str):
    return {"name": name}


# http://127.0.0.1:8000/www/pages/p2/554
@router.get("/p2/{number}")
async def page_2(number: int):
    return {"integer": number}


# http://127.0.0.1:8000/www/pages/p3/Antenna?name=123
class TypeName(str, Enum):
    antenna = "Antenna"
    cabel = "Cabel"


@router.get("/p3/{type_name}", description="Enum пример")
async def page_3(type_name: TypeName, name: str | None = None):
    return [type_name.value, name]


# Более строгая фильтрация разрешенных значений
# https://fastapi.tiangolo.com/ru/tutorial/query-params-str-validations/#__tabbed_1_1
@router.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Возврат text/plain вместо json.
# В декораторе объявлен класс для документации. В функции для валидации ответа.
@router.get("/string", response_class=PlainTextResponse)
async def return_to_string() -> PlainTextResponse:
    return PlainTextResponse("Hello World")


@router.post("/post/", description="Pydantic пример")
async def create_item(item: ItemSchema):
    return [item, item.name]