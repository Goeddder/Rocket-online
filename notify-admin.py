import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramForbiddenError

# --- НАЛАШТУВАННЯ ---
API_TOKEN = "8651326096:AAFBOQ-GPNJKON6KGic81DvxHjH-XDXwYFM"

# Налаштування логування для відстеження натискань
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 1. ОБРОБКА КНОПКИ "ПРИЙНЯТИ" (ok_USERID_ORDERID)
@dp.callback_query(F.data.startswith("ok_"))
async def handle_approve(callback: CallbackQuery):
    try:
        # Розбираємо дані з кнопки
        _, user_id, order_id = callback.data.split("_")
        
        # Отримуємо поточний текст повідомлення
        current_text = callback.message.text
        
        # Оновлюємо повідомлення в адміна (прибираємо кнопки, додаємо статус)
        await callback.message.edit_text(
            f"{current_text}\n\n✅ **СТАТУС: ПІДТВЕРДЖЕНО**\n(Доступ надано замовленню #{order_id})",
            parse_mode="Markdown"
        )

        # Надсилаємо радісну новину клієнту
        await bot.send_message(
            chat_id=int(user_id),
            text=f"✅ **Вашу оплату замовлення #{order_id} прийнято!**\n\nТепер ви маєте повний доступ до софту. Дякуємо, що обрали нас! Якщо є питання — звертайтесь."
        )
        
        # Маленьке сповіщення зверху в Телеграм адміна
        await callback.answer("Оплату успішно прийнято!")

    except TelegramForbiddenError:
        await callback.answer("Помилка: Користувач заблокував бота", show_alert=True)
    except Exception as e:
        logging.error(f"Error in approve: {e}")
        await callback.answer(f"Помилка: {e}", show_alert=True)

# 2. ОБРОБКА КНОПКИ "ВІДХИЛИТИ" (no_USERID_ORDERID)
@dp.callback_query(F.data.startswith("no_"))
async def handle_reject(callback: CallbackQuery):
    try:
        _, user_id, order_id = callback.data.split("_")
        
        current_text = callback.message.text

        # Оновлюємо повідомлення в адміна
        await callback.message.edit_text(
            f"{current_text}\n\n❌ **СТАТУС: ВІДХИЛЕНО**",
            parse_mode="Markdown"
        )

        # Сповіщаємо клієнта про відмову
        await bot.send_message(
            chat_id=int(user_id),
            text=f"❌ **Вашу оплату замовлення #{order_id} відхилено.**\n\nМожливо, переказ не було знайдено або сума невірна. Будь ласка, напишіть адміністратору для уточнення."
        )
        
        await callback.answer("Оплату відхилено")

    except TelegramForbiddenError:
        await callback.answer("Клієнт заблокував бота", show_alert=True)
    except Exception as e:
        logging.error(f"Error in reject: {e}")
        await callback.answer("Сталася помилка при відхиленні")

# 3. ЗАПУСК БОТА
async def main():
    print("---")
    print("💎 Адмін-панель IllyaGarant ПРАЦЮЄ")
    print("📡 Очікую на замовлення з Mini App...")
    print("---")
    
    # Видаляємо старі повідомлення, щоб бот не відповідав на них при старті
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nБот зупинений.")
        
