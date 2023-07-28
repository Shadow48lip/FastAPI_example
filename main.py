import uvicorn
from fastapi import FastAPI

from src.conf.routers import router_list

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





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)