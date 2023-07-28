from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.conf.database import get_async_session
from src.models.users import User
from src.schemas.users import UsersSchema
from src.services.dependencies import verify_token

router = APIRouter(prefix="/users", tags=["Требуется авторизация"], dependencies=[Depends(verify_token)])


@router.get("/auth_req/")
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


@router.get("/get_all/")
async def all_users(session: AsyncSession = Depends(get_async_session)) -> list[UsersSchema]:
    q = select(User)

    # не ясно как проверить есть требуемая колонка в базе, ну только через try...
    results = await session.execute(q)
    row = results.first()[0]
    print(type(results), type(row))
    print(row.name)

    results = await session.execute(q)
    rows = results.all()
    print(type(results), type(rows))
    # row_list = [{line.id: line.name} for line in rows]
    row_list = [line[0].name for line in rows]
    print(row_list)

    result = await session.scalar(q)
    print(type(result))
    if hasattr(result, 'name'):
        print(result.name)

    results = await session.scalars(q)
    print(type(results))
    result = [UsersSchema(id=row.id, name=row.name, age=row.age) for row in results]
    # если имена колонок совпадают, то можно использовать и более простой механизм
    # result = [row for row in results]

    return result


@router.get("/get_detail/{name}", response_model=UsersSchema)
async def say_hello(
            name: Annotated[str, Path(max_length=20, description="имя пользователя")],
            session: AsyncSession = Depends(get_async_session)
        ):

    q = select(User).where(User.name == name)

    result = await session.scalar(q)
    if not result:
        raise HTTPException(status_code=404, detail='Name not found')

    return UsersSchema(id=result.id, name=result.name, age=result.age)