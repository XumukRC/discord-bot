#!/usr/bin/env python3.5

import discord
import random

from settings import settings
from connect import bot
import music
import search

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
	
@bot.command()
async def add(left : int, right : int):
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
async def choose(*choices : str):
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command()
async def haitaka():
    await bot.say('Yes, Haitaka is cool.')
	
@cool.command()
async def child():
    await bot.say('Yes, Child is cool.')
	

bot_auth = settings.bot_auth()
bot.run(bot_auth['login'], bot_auth['passwd'])