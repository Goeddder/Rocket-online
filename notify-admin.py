import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery

API_TOKEN = "8651326096:AAFBOQ-GPNJKON6KGic81DvxHjH-XDXwYFM"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обробка кнопки ПРИЙНЯТИ
@dp.callback_query(F.data.startswith("ok_"))
async def handle_ok(callback: CallbackQuery):
    try:
        # Дані: ok_USERID_ORDERID
        parts = callback.data.split("_")
        user_id = int(parts[1])
        order_id = parts[2]

        # Оновлюємо чат адміна
        await callback.message.edit_text(f"{callback.message.text}\n\n✅ **ПІДТВЕРДЖЕНО АДМІНІСТРАТОРОМ**")
        
        # Шлемо юзеру повідомлення
        await bot.send_message(user_id, f"✅ Ваша оплата замовлення #{order_id} підтверджена! Дякуємо за покупку.")
        await callback.answer("Успішно підтверджено!")
        
    except Exception as e:
        await callback.answer(f"Помилка: Користувач не запустив бота!", show_alert=True)

# Обробка кнопки ВІДХИЛИТИ
@dp.callback_query(F.data.startswith("no_"))
async def handle_no(callback: CallbackQuery):
    try:
        parts = callback.data.split("_")
        user_id = int(parts[1])
        
        await callback.message.edit_text(f"{callback.message.text}\n\n❌ **ВІДХИЛЕНО**")
        await bot.send_message(user_id, "❌ Ваша оплата була відхилена адміністратором. Зв'яжіться з підтримкою.")
        await callback.answer("Відхилено")
    except Exception as e:
        await callback.answer("Помилка при відхиленні", show_alert=True)

async def main():
    print("💎 Адмін-бот IllyaGarant запущений!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
        
