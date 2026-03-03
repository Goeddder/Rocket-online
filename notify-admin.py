import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery

# Твій актуальний токен
API_TOKEN = "8651326096:AAFBOQ-GPNJKON6KGic81DvxHjH-XDXwYFM"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обробка кнопки "Прийняти"
@dp.callback_query(F.data.startswith("confirm_"))
async def handle_confirm(callback: CallbackQuery):
    try:
        # Розбираємо дані: confirm_USERID_AMOUNT
        parts = callback.data.split("_")
        user_id = parts[1]
        amount = parts[2]

        # 1. Оновлюємо повідомлення в тебе (адміна)
        await callback.message.edit_text(
            f"{callback.message.text}\n\n✅ **СТАТУС: ОПЛАЧЕНО**",
            parse_mode="Markdown"
        )

        # 2. Надсилаємо повідомлення клієнту
        await bot.send_message(
            user_id, 
            f"✅ Ваша оплата ({amount} ₴) підтверджена!\nДякуємо за покупку, доступ активовано."
        )
        
        await callback.answer("Підтверджено успішно!")
    except Exception as e:
        logging.error(f"Помилка підтвердження: {e}")
        await callback.answer("Помилка: можливо, юзер не запустив бота", show_alert=True)

# Обробка кнопки "Відхилити"
@dp.callback_query(F.data.startswith("cancel_"))
async def handle_cancel(callback: CallbackQuery):
    try:
        user_id = callback.data.split("_")[1]

        # 1. Оновлюємо повідомлення в тебе
        await callback.message.edit_text(
            f"{callback.message.text}\n\n❌ **СТАТУС: ВІДХИЛЕНО**",
            parse_mode="Markdown"
        )

        # 2. Пишемо клієнту
        await bot.send_message(
            user_id, 
            "❌ Вашу оплату відхилено адміністратором.\nЯкщо ви впевнені, що оплатили — напишіть нам у підтримку."
        )
        
        await callback.answer("Відхилено")
    except Exception as e:
        logging.error(f"Помилка відхилення: {e}")
        await callback.answer("Помилка при відхиленні", show_alert=True)

async def main():
    print("🤖 Бот-адмін запущений і слухає кнопки...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
