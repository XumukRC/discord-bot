import discord

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = 'Hello {0.attachments }'.format(message)
    await client.send_message(message.channel, msg)