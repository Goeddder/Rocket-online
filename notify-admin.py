import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery

# Твій API токен
API_TOKEN = "8651326096:AAFBOQ-GPNJKON6KGic81DvxHjH-XDXwYFM"

# Налаштування логів (будеш бачити помилки в консолі)
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 1. ОБРОБКА КНОПКИ "ПРИЙНЯТИ"
@dp.callback_query(F.data.startswith("confirm_"))
async def handle_confirm(callback: CallbackQuery):
    try:
        # Дані приходять у форматі: confirm_USERID_AMOUNT
        data = callback.data.split("_")
        user_id = data[1]
        amount = data[2]

        # Оновлюємо текст повідомлення у тебе (адміна)
        await callback.message.edit_text(
            f"{callback.message.text}\n\n✅ **СТАТУС: ПІДТВЕРДЖЕНО**\n(Клієнту надіслано сповіщення)",
            parse_mode="Markdown"
        )

        # Надсилаємо повідомлення клієнту в приват
        await bot.send_message(
            user_id, 
            f"✅ **Вашу оплату на суму {amount} ₴ підтверджено!**\n\nДякуємо за покупку. Тепер ви маєте повний доступ до софту. Якщо у вас виникли питання — пишіть у підтримку."
        )
        
        # Вібрація або маленьке сповіщення зверху в Telegram у тебе
        await callback.answer("Оплату прийнято!")
        
    except Exception as e:
        logging.error(f"Помилка: {e}")
        await callback.answer("Помилка: Юзер не запустив бота або заблокував його", show_alert=True)

# 2. ОБРОБКА КНОПКИ "ВІДХИЛИТИ"
@dp.callback_query(F.data.startswith("cancel_"))
async def handle_cancel(callback: CallbackQuery):
    try:
        user_id = callback.data.split("_")[1]

        # Оновлюємо текст у тебе
        await callback.message.edit_text(
            f"{callback.message.text}\n\n❌ **СТАТУС: ВІДХИЛЕНО**",
            parse_mode="Markdown"
        )

        # Пишемо клієнту
        await bot.send_message(
            user_id, 
            "❌ **Вашу оплату відхилено.**\n\nЯкщо ви справді здійснили переказ, будь ласка, надішліть скріншот чека адміністратору для перевірки вручну."
        )
        
        await callback.answer("Оплату відхилено")
        
    except Exception as e:
        logging.error(f"Помилка: {e}")
        await callback.answer("Не вдалося надіслати сповіщення юзеру", show_alert=True)

# ЗАПУСК БОТА
async def main():
    print("---")
    print("🚀 Адмін-бот Іллі запущений!")
    print("📡 Очікую на замовлення з Mini App...")
    print("---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинений")
        
