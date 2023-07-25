from traceback import print_exception
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from src.conf.database import get_async_session
from src.conf.routers import router_list
from src.models.users import User
from src.schemas.users import UsersSchema

app = FastAPI(title="Test API", version='0.0.1')

# Запереть ошибки и обработать самому
# async def catch_exceptions_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as e:
#         # you probably want some kind of logging here
#         # print_exception(e)
#         return Response("Internal server error!!", status_code=500)
#
# app.middleware('http')(catch_exceptions_middleware)

# В соответствии с паттерном по слоям
for router in router_list:
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
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


@app.get("/hello/{name}", response_model=UsersSchema)
async def say_hello(name: Annotated[str, Path(max_length=20, description="имя пользователя")], session: AsyncSession = Depends(get_async_session)):

    q = select(User).where(User.name == name)

    result = await session.scalar(q)
    if not result:
        raise HTTPException(status_code=404, detail='Name not found')

    return UsersSchema(id=result.id, name=result.name, age=result.age)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)