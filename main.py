import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import logging

TOKEN = "ВАШ_ТОКЕН_БОТА"
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_names = {}

@dp.message(commands=["setname"])
async def set_name(message: types.Message):
    user_id = message.from_user.id
    new_name = message.text[len("setname "):].strip()
    
    if new_name:
        user_names[user_id] = new_name
        await message.answer(f"Ваше имя изменено на: {new_name}")
    else:
        await message.answer("Пожалуйста, укажите новое имя после команды setname.")

@dp.message()
async def repeater(message: types.Message):
    user_id = message.from_user.id
    user_name = user_names.get(user_id, "Без имени")
    
    if message.reply_to_message:
        original_message = message.reply_to_message
        if original_message.text:
            original_text = original_message.text
        else:
            original_text = "Это не текстовое сообщение"
        
        text = f"{user_name} (ответ на сообщение):\n{original_text}\n{message.text}"
        
        await original_message.delete()

    else:
        text = f"{user_name}:\n{message.text}"

    await message.delete()

    if message.text:
        await message.answer(text)

    if message.photo:
        await message.answer_photo(message.photo[-1].file_id, caption=f"{user_name}: {message.caption}")
    elif message.video:
        await message.answer_video(message.video.file_id, caption=f"{user_name}: {message.caption}")
    elif message.document:
        await message.answer_document(message.document.file_id, caption=f"{user_name}: {message.caption}")
    elif message.sticker:
        await message.answer_sticker(message.sticker.file_id, caption=f"{user_name} отправил стикер.")
    elif message.animation:
        await message.answer_animation(message.animation.file_id, caption=f"{user_name} отправил GIF.")
    elif message.location:
        await message.answer_location(message.location.latitude, message.location.longitude, caption=f"{user_name}: Геолокация.")
    elif message.voice:
        await message.answer_voice(message.voice.file_id, caption=f"{user_name}: Голосовое сообщение.")

if __name__ == "__main__":
    from aiogram import executor
    asyncio.run(dp.start_polling())
