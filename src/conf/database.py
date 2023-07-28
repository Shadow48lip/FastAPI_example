from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from src.conf.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, DB_ENGINE

# Разные движки баз данных
if DB_ENGINE == 'mysql':
    DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # инициализируем новый движок SQLAlchemy с помощью create_async_engine(
    # echo=True при инициализации движка позволит нам увидеть сгенерированные SQL-запросы в консоли
    engine = create_async_engine(DATABASE_URL, echo=False)
elif DB_ENGINE == 'postgresql':
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_async_engine(DATABASE_URL, echo=False)
else:
    engine = create_async_engine("sqlite+aiosqlite:///src/sqlite.db")


# Base = declarative_base()
class Base(DeclarativeBase):
    pass


try:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
except Exception as e:
    print(f"DB connection error!\n{e}")


# Наконец, мы создадим функцию FastAPI Dependency, которая будет формировать для нас будущие сессии по запросу:
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
    except OperationalError as e:
        print(f"OperationalError session error!\n{e}")
    except SQLAlchemyError as e:
        print(f"SQLAlchemyError session error!\n{e}")

