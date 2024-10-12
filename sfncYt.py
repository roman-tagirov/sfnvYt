import asyncio
from googleapiclient.discovery import build
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

API_KEY = 'AIzaSyD9zwIQ1ISmExvGKNNdX4kMuh8oGJSrt0M'
CHANNEL_ID = 'UCL04GObJoemmW4HUlgZ2llw'
TELEGRAM_TOKEN = "7927318859:AAHXlOhih-2jkn6djUhA10iJCXVCxL_HMHo"
TELEGRAM_CHAT_ID = "-1002436966994"

youtube = build('youtube', 'v3', developerKey=API_KEY)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

last_video_id = None

async def check_new_video():
    global last_video_id
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=CHANNEL_ID,
            maxResults=1,
            order='date',
            type='video'
        )
        response = request.execute()

        video = response['items'][0]
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        if video_id != last_video_id:
            last_video_id = video_id
            await bot.send_message(TELEGRAM_CHAT_ID, f"-Вышло новое видео:-\n{video_title}\n{video_url}", disable_web_page_preview=False)

        await asyncio.sleep(120)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Начало работы")


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(check_new_video())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())