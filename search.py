import discord
from connect import bot
from settings import settings

import api.duckduckgo as ddg

@bot.command()
async def whatis(subj : str):
    await bot.say(ddg.get_zci(subj))
