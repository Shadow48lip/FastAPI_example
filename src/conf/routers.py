""" Склеиваем все роутеры """

from src.api.examples import router as router_1
from src.api.users import router as router_2


router_list = [
    router_1,
    router_2,
]
