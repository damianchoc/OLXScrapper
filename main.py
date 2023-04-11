import json
import requests
from bs4 import BeautifulSoup
import discord
import asyncio

TOKEN = 'TOKEN' # Your discord bod token
url = 'https://www.olx.pl/elektronika/fotografia/?search%5Bphotos%5D=1&search%5Border%5D=created_at:desc' # olx.pl page to scrap on
CHANNEL_ID = 0 # Your discord channel id
offers_from_file = []


def get_newest_offers():
    print("Scrapping for offers...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('div', {'class': 'css-1sw7q4x', 'data-cy': 'l-card'})
    new_offers = []
    for listing in listings:
        offer_url = "https://olx.pl" + "" + listing.find('a', {'class': 'css-rc5s2u'}).get('href')
        offer = {'url': offer_url}
        new_offers.append(offer)

    print(new_offers)
    print("Done")
    return process_new_offers(new_offers)


def settle_offers_from_file():
    with open('offers.json', 'r') as f:
        global offers_from_file
        offers_from_file = json.load(f)


def process_new_offers(new_offers):
    global offers_from_file
    # Remove any existing offers with matching URLs
    urls = [offer['url'] for offer in offers_from_file]
    new_offers = [offer for offer in new_offers if offer['url'] not in urls]

    offers_from_file = offers_from_file + new_offers
    with open('offers.json', 'w') as f:
        json.dump(offers_from_file, f)

    return new_offers


class MyClient(discord.Client):
    def __init__(selfself, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        settle_offers_from_file()
        print("I'm online! Hello World!")

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.background_task())

    async def background_task(self):
        await self.wait_until_ready()
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("I'm online! Hello world!")
        while not self.is_closed():
            offers = get_newest_offers()
            for offer in offers:
                await channel.send("New offer:\nURL: " + "" + offer['url'])
            await asyncio.sleep(900)


bot = MyClient(intents=discord.Intents().all())
bot.run(TOKEN)

import asyncio

TOKEN = 'TOKEN' # Discord bot token
url = 'https://www.olx.pl/elektronika/fotografia/?search%5Bphotos%5D=1&search%5Border%5D=created_at:desc' # OLX URL to scrap
CHANNEL_ID = 0 # Dscord channel id
offers_from_file = []


def get_newest_offers():
    print("Scrapping for offers...")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('div', {'class': 'css-1sw7q4x', 'data-cy': 'l-card'})
    new_offers = []
    for listing in listings:
        offer_url = "https://olx.pl" + "" + listing.find('a', {'class': 'css-rc5s2u'}).get('href')
        offer = {'url': offer_url}
        new_offers.append(offer)

    print(new_offers)
    print("Done")
    return process_new_offers(new_offers)


def settle_offers_from_file():
    with open('offers.json', 'r') as f:
        global offers_from_file
        offers_from_file = json.load(f)


def process_new_offers(new_offers):
    global offers_from_file
    # Remove any existing offers with matching URLs
    urls = [offer['url'] for offer in offers_from_file]
    new_offers = [offer for offer in new_offers if offer['url'] not in urls]

    offers_from_file = offers_from_file + new_offers
    with open('offers.json', 'w') as f:
        json.dump(offers_from_file, f)

    return new_offers


class MyClient(discord.Client):
    def __init__(selfself, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        settle_offers_from_file()
        print("I'm online! Hello World!")

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.background_task())

    async def background_task(self):
        await self.wait_until_ready()
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("I'm online! Hello world!")
        while not self.is_closed():
            offers = get_newest_offers()
            for offer in offers:
                await channel.send("New offer:\nURL: " + "" + offer['url'])
            await asyncio.sleep(900)


bot = MyClient(intents=discord.Intents().all())
bot.run(TOKEN)
