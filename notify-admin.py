import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery

API_TOKEN = "8651326096:AAFBOQ-GPNJKON6KGic81DvxHjH-XDXwYFM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обробка кнопки "Прийняти"
@dp.callback_query(F.data.startswith("confirm_"))
async def handle_confirm(callback: CallbackQuery):
    try:
        data = callback.data.split("_")
        user_id = int(data[1])
        amount = data[2]

        # Оновлюємо ваше повідомлення
        await callback.message.edit_text(
            f"{callback.message.text}\n\n✅ **СТАТУС: ПІДТВЕРДЖЕНО**",
            parse_mode="Markdown"
        )

        # Пишемо клієнту
        await bot.send_message(user_id, f"✅ Вашу оплату ({amount} ₴) підтверджено! Доступ активовано.")
        await callback.answer("Виконано!")
    except Exception as e:
        await callback.answer("Помилка: користувач не написав боту /start", show_alert=True)

# Обробка кнопки "Відхилити"
@dp.callback_query(F.data.startswith("cancel_"))
async def handle_cancel(callback: CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])

        await callback.message.edit_text(
            f"{callback.message.text}\n\n❌ **СТАТУС: ВІДХИЛЕНО**",
            parse_mode="Markdown"
        )

        await bot.send_message(user_id, "❌ Вашу оплату відхилено адміністратором.")
        await callback.answer("Відхилено")
    except Exception as e:
        await callback.answer("Помилка при відхиленні", show_alert=True)

async def main():
    print("🚀 Адмін-бот запущений і чекає на кнопки...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
