import asyncio
import concurrent.futures
from SsstikScraper import scraper
import telebot
import requests
import io

bot = telebot.TeleBot('6998713632:AAE5oKB5UD737bnRZGbzJcQl1gp8bKZhhgw')

executor = concurrent.futures.ThreadPoolExecutor()

async def async_downloader(url):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, scraper, url)
    return result

def handle_message(message):
    asyncio.run(process_message(message))

async def process_message(message):
    if "https://vm.tiktok.com" in message.text or "https://www.tiktok.com/@" in message.text:
        url = message.text
        result = await async_downloader(url)
        
        if isinstance(result, dict):
            if "images" in result:
                images = result.get("images")
                # music = str(result.get("music"))
          
                for i in range(0, len(images), 10):
                    media_group = []
                    for image_url in images[i:i + 10]:
                        image_request = requests.get(image_url)
                        if image_request.status_code in [200, 206]:
                            image_bytes = io.BytesIO(image_request.content)
                            image_bytes.seek(0)
                            media_group.append(telebot.types.InputMediaPhoto(image_bytes))
                        else:
                            bot.send_message(message.chat.id, f"Error loading images: {image_request.status_code}")
                    
                    if media_group:
                        bot.send_media_group(message.chat.id, media_group)
        else:
            bot.send_message(message.chat.id, str(result))         

bot.message_handler(content_types=["text"])(handle_message)

bot.infinity_polling()
