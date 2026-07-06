import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

# Включаем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# ⚠️ ЗАМЕНИ ЭТОТ ТОКЕН НА СВОЙ ИЗ @BotFather
BOT_TOKEN = "8795840281:AAG5fhG8AZgssDN92kpdTMGDnhPq9yiYhWE"
WEB_APP_URL = "https://rocket-online.vercel.app/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создаем инлайн-кнопку для запуска Web App
    kb = InlineKeyboardBuilder()
    kb.button(
        text="🛒 Открыть магазин",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    
    # Текст приветствия
    welcome_text = (
        "👋 **Приветствуем в Oxide: Survival Island Shop!**\n\n"
        "🔥 Мы рады приветствовать тебя в нашем **официальном магазине игрового доната**!\n\n"
        "Здесь ты можешь быстро, безопасно и без лишних переплат приобрести:\n"
        "• Наборы монет (Coin Packs)\n"
        "• Наборы билетов\n"
        "• Монеты Боевого Пропуска\n"
        "• Premium статус и VIP привилегии\n\n"
        "⚡️ Весь донат начисляется автоматически по твоему Player ID.\n\n"
        "Жми кнопку ниже, чтобы перейти к ассортименту! 👇"
    )
    
    # Отправляем сообщение с поддержкой Markdown разметки
    await message.answer(welcome_text, reply_markup=kb.as_markup(), parse_mode="Markdown")

async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
