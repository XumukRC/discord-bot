import asyncio
import sqlite3

import discord
from connect import bot
import uploads


if not discord.opus.is_loaded():
	discord.opus.load_opus('/usr/local/lib/libopus.so')

class DJ:
	def __init__(self):
		self.songs = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		#self.starter = None
		self.player = None
		self.current = None

	def toggle_next_song(self):
		bot.loop.call_soon_threadsafe(self.play_next_song.set)

	def can_control_song(self, author):
		return author == self.starter or (self.current is not None and author == self.current.requester)

	def is_playing(self):
		return self.player is not None and self.player.is_playing()

bot_dj = DJ()
		
@bot.command(pass_context=True)
async def join(context, channel_name : str):
	global bot_dj
	if bot.is_voice_connected():
		await bot.say('Already connected to a voice channel')
		
	check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice

	channel = discord.utils.find(check, context.message.server.channels)
	if channel is None:
		await bot.say('Cannot find a voice channel by that name.')

	await bot.join_voice_channel(channel)
	#bot_dj.starter = context.message.author
	
@bot.command()
async def leave():
	global bot_dj
	#if not bot_dj.can_control_song(message.author):
	#	return
	#self.starter = None
	await bot.voice.disconnect()

@bot.command()
async def pause():
	global bot_dj
	#if not self.can_control_song(message.author):
	#	fmt = 'Only the requester ({0.current.requester}) can control this song'
	#	await self.send_message(message.channel, fmt.format(self))
	if bot_dj.player.is_playing():
		bot_dj.player.pause()

@bot.command()
async def resume():
	global bot_dj
	#if not self.can_control_song(message.author):
	#	fmt = 'Only the requester ({0.current.requester}) can control this song'
	#	await self.send_message(message.channel, fmt.format(self))
	if bot_dj.player is not None and not bot_dj.is_playing():
		bot_dj.player.resume()

@bot.command()
async def skip():
	if bot_dj.player.is_playing():
		bot_dj.player.stop()
		bot_dj.toggle_next_song()

@bot.command()
async def play():
	global bot_dj
	if bot_dj.player is not None and bot_dj.player.is_playing():
		await bot.say('Already playing a song')
		return
	if bot_dj.songs.empty():
		db_conn = sqlite3.connect('uploads.db')
		db_cur = db_conn.cursor()
		for song in db_cur.execute("""SELECT id, url FROM songs ORDER BY RANDOM()"""):
			await bot_dj.songs.put(song[1])
		db_conn.close()
	while True:
		if not bot.is_voice_connected():
			await bot.say('Not connected to a voice channel')
			return

		bot_dj.play_next_song.clear()
		bot_dj.current = await bot_dj.songs.get()
		bot_dj.player = bot.voice.create_ffmpeg_player(bot_dj.current, after=bot_dj.toggle_next_song)
		bot_dj.player.start()
		fmt = 'Playing song "{0}"'
		await bot.say(fmt.format(bot_dj.current))
		await bot_dj.play_next_song.wait()
	