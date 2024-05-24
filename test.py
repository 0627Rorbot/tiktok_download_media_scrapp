import requests
from SsstikScraper import scraper
result = scraper("https://vm.tiktok.com/ZMMT23rVY/")
images = result.get("images")
# you can add your own logic for handling request errors
for index, image_url in enumerate(images):
    image_request = requests.get(image_url)
    with open(f"{index}.png", "wb") as img:
        img.write(image_request.content)