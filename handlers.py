import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from driver import subscribe

regexp = re.compile(r"https://www\.instagram\.com/(?P<name>[\w.]+)/?")
router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу подписаться на аккаунт, просто пришли ссылку на него")


@router.message()
async def message_handler(msg: Message):
    name = regexp.match(msg.html_text)
    if name:
        result = subscribe(name.group('name'))
        # result = True
        if result:
            await msg.answer(f"Подписка на пользователя {name.group('name')} прошла успешно")
        else:
            await msg.answer(f"Произошла ошибка, подписка на пользователя {name.group('name')} не прошла")
    else:
        await msg.answer("Неверная ссылка на профиль")


