from aiogram import Bot, Dispatcher, executor, types
import os
from config import TOKEN, ADMIN_ID
from keyboards import video

bot=Bot(TOKEN)
dp = Dispatcher(bot)

if not os.path.exists('video'):
    os.makedirs('video')

@dp.message_handler(commands=['start'])
async def start_command(m: types.Message):
    await m.answer(f'''
    Привет, @{m.from_user.username}!
Ты можешь заработать до <b>5 000 рублей</b>, прорекламировав наш YouTube канал <a href="https://www.youtube.com/@MKM_Vsevolozhsk">MKM Всеволожск</a>.

<b>Для того чтобы отправить доказательства, нажми на кнопку</b>
    ''', reply_markup=video(), parse_mode='HTML')

@dp.message_handler(commands=['send'])
async def send_message(message: types.Message):
    # Проверяем, что отправитель является админом
    if str(message.from_user.id) != ADMIN_ID:
        pass
    
    # Получаем ID пользователя и сообщение
    try:
        user_id, text = message.text.split(' ', maxsplit=1)[1].split(' ', maxsplit=1)
    except (IndexError, ValueError):
        await message.answer('Некорректный формат команды. Используйте /send <user_id> <text>')
        return
    try:
        await bot.send_message(chat_id=user_id, text=f"*Сообщение от админа:*\n\n{text}", parse_mode='MarkDown')
        await message.answer(f'Сообщение успешно отправлено пользователю!')
    except Exception as e:
        await message.answer(f'Не удалось отправить сообщение: {e}')
@dp.message_handler(content_types=['text'])
async def send_to_admin(message: types.Message):
    if message.text == "Отправить видео":
        await message.answer(f'Отправь мне видео в котором есть реклама нашего канала <a href="https://www.youtube.com/@MKM_Vsevolozhsk">MKM Всеволожск</a>, или отправь мне ссылку на видео. Формат видео должен быть .mp4', parse_mode='HTML')
    else:
        await bot.send_message(chat_id=ADMIN_ID, text=f"Новое сообщение!\nИмя: @{message.from_user.username}\nID: `{message.from_user.id}`\n\n{message.text}", parse_mode='MarkDown')

@dp.message_handler(content_types=['video'])
async def photo(message: types.Message):
    video = message.video
    username = message.from_user.username 
    file_id = video.file_id
    file_path = f'video/{file_id}.mp4'
    await video.download(file_path) 
    with open(file_path, 'rb') as video_file:
        try: 
            await message.answer(f"Я отправил видео на проверку к админу, он сообщит тебе через меня о том, что видео подходит/не подходит.\nУдачи!")
            await bot.send_video(chat_id=ADMIN_ID, video=video_file, caption=f"Пользователь @{username} отправил вам видео.\n(ID: `{message.from_user.id}`)\n\n_Для ответа используйте команду /send <ID> <текст>_", parse_mode='MarkDown')
        except Exception:
            await message.answer(f"Похоже что-то пошло не так...")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)