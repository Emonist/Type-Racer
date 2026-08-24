import time
import aiohttp
import discord
from discord.ext import commands

class OcrSolver(commands.Cog):
    def __init__(self, bot: commands.Bot, api_token: str):
        self.bot = bot
        self.api_token = api_token
        self.target_author_id = 825617171589759006
        self.api_url = 'https://Ocr-api.phantomxnovaxd.repl.co/api/v1/solver'

    async def solver(self, solution_img_url: str):
        data = {
            'image_url': solution_img_url,
            'Authorization': self.api_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, data=data, headers=headers) as response:
                result = await response.json()
                return result['text'], result['time']

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id != self.target_author_id:
            return
        if not message.embeds or not message.embeds[0].image or not message.embeds[0].image.url:
            return

        time_start = time.time()
        url = message.embeds[0].image.url
        solution_text, solving_time = await self.solver(url)
        time_taken = time.time() - time_start

        await message.reply(solution_text)
        await message.reply(f'Solved! Time taken: {time_taken:.4f} seconds | Solving time: {solving_time} seconds')

async def setup(bot: commands.Bot):
    await bot.add_cog(OcrSolver(bot, api_token="YOUR_TOKEN_HERE"))
