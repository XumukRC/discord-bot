import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='%')
bot.run('haitaka@yandex.ru', '22:=Kp|/|cToF')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')