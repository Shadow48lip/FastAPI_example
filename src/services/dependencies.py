from typing import Annotated
import secrets
from fastapi import Header, HTTPException


# Авторизация по хидеру
async def verify_token(auth_token: Annotated[str, Header()]):
    allow_token = "fake-super-secret-token"
    # Это просто вариант сравнения допускает атаку "по времени", когда можно по длительности ответа подобрать токен.
    # if auth_token != allow_token:
    #     raise HTTPException(status_code=401, detail="Auth-Token header invalid")

    # В этом варианте время сравнения будет всегда одинаковым
    token_client_bytes = auth_token.encode("utf-8")
    token_allow_bytes = allow_token.encode("utf-8")
    if not secrets.compare_digest(token_allow_bytes, token_client_bytes):
        raise HTTPException(status_code=401, detail="Auth-Token header invalid")