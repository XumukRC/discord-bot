import discord
from discord.ext import commands
import random
import asyncio

bot = commands.Bot(command_prefix='?')

@bot.event
@asyncio.coroutine
 def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@asyncio.coroutine
 def add(left : int, right : int):
    await bot.say(left + right)
	
@bot.command()
@asyncio.coroutine
 def �����(left : int, right : int):
    await bot.say(left - right)

@bot.command()
@asyncio.coroutine
 def roll(dice : str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
@asyncio.coroutine
 def choose(*choices : str):
    await bot.say(random.choice(choices))

@bot.command()
@asyncio.coroutine
 def repeat(times : int, content='repeating...'):
    for i in range(times):
        await bot.say(content)

@bot.command()
@asyncio.coroutine
 def joined(member : discord.Member):
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
@asyncio.coroutine
 def cool(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command()
@asyncio.coroutine
 def bob():
    await bot.say('Yes, bob is cool.')

bot.run('haitaka@yandex.ru', '22:=Kp|/|cToF')