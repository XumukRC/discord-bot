import discord
from connect import bot

print("test3")

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    msg = 'Hello {0.attachments }'.format(message)
    await client.send_message(message.channel, msg)