import time
import aiohttp
import discord
from discord.ext import commands

class TypeRacerSolver(commands.Cog):
    def __init__(self, bot: commands.Bot, api_token: str):
        self.bot = bot
        self.api_token = api_token
        self.typeracer_bot_id = 825617171589759006
        self.solver_api_url = 'https://Ocr-api.phantomxnovaxd.repl.co/api/v1/solver'

    async def solve_image(self, image_url: str):
        payload = {
            'image_url': image_url,
            'Authorization': self.api_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.solver_api_url, data=payload, headers=headers) as response:
                res = await response.json()
                return res['text'], res['time']

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.typeracer_bot_id:
            return
        if not message.embeds or not message.embeds[0].image or not message.embeds[0].image.url:
            return

        start_clock = time.time()
        image_target_url = message.embeds[0].image.url
        solved_text, api_time = await self.solve_image(image_target_url)
        total_duration = time.time() - start_clock

        await message.reply(solved_text)
        await message.reply(f'TypeRacer Solved! Time taken: {total_duration:.4f} seconds | API time: {api_time} seconds')

async def setup(bot: commands.Bot):
    await bot.add_cog(TypeRacerSolver(bot, api_token="YOUR_TOKEN_HERE"))
