import asyncio
import sqlite3

import discord
from connect import bot
import uploads

if not discord.opus.is_loaded():
	discord.opus.load_opus('/usr/local/lib/libopus.so')

@bot.command()
async def join(channel_name : str):
	check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice
	channel = discord.utils.find(check, message.server.channels)
	if channel is None:
		await bot.say('Cannot find a voice channel by that name.')
	await bot.join_voice_channel(channel)
	
@bot.command()
async def leave():
	await self.voice.disconnect()
	
@bot.command()
async def play():
	#SELECT * FROM table ORDER BY RANDOM() LIMIT 1;
	player = bot.voice.create_ffmpeg_player('https://cdn.discordapp.com/attachments/137278249502769152/137640630137389056/Bad_Religion_-_Dearly_Beloved_Acoustic.mp3')
	player.start()
