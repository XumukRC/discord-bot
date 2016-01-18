import asyncio
import sqlite3
from os import listdir
from os.path import isfile, join
import random

import discord
from connect import bot
import uploads


if not discord.opus.is_loaded():
	discord.opus.load_opus('/usr/local/lib/libopus.so')

class Radio:
	def __init__(self):
		self.songs = asyncio.Queue()
		self.play_next_song = asyncio.Event()
		#self.starter = None
		self.player = None
		self.current = None
		self.files_dir = "copyfs/radio/"
		# list ONLY files
		self.files = [f for f in listdir(self.files_dir) if isfile(join(self.files_dir, f))]

	def toggle_next_song(self):
		bot.loop.call_soon_threadsafe(self.play_next_song.set)

	def can_control_song(self, author):
		return author == self.starter or (self.current is not None and author == self.current.requester)

	def is_playing(self):
		return self.player is not None and self.player.is_playing()
		
	async def random_q(self):
		q = random.sample(self.files, len(self.files))
		for song in q:
			await self.songs.put(self.files_dir + song)

radio = Radio()
		
@bot.command(pass_context=True)
async def join(context, channel_name : str):
	global radio
	if bot.is_voice_connected():
		await bot.say('Already connected to a voice channel')
		
	check = lambda c: c.name == channel_name and c.type == discord.ChannelType.voice

	channel = discord.utils.find(check, context.message.server.channels)
	if channel is None:
		await bot.say('Cannot find a voice channel by that name.')

	await bot.join_voice_channel(channel)
	#radio.starter = context.message.author
	
@bot.command()
async def leave():
	global radio
	#if not radio.can_control_song(message.author):
	#	return
	#self.starter = None
	await bot.voice.disconnect()

@bot.command()
async def pause():
	global radio
	#if not self.can_control_song(message.author):
	#	fmt = 'Only the requester ({0.current.requester}) can control this song'
	#	await self.send_message(message.channel, fmt.format(self))
	if radio.player.is_playing():
		radio.player.pause()

@bot.command()
async def resume():
	global radio
	#if not self.can_control_song(message.author):
	#	fmt = 'Only the requester ({0.current.requester}) can control this song'
	#	await self.send_message(message.channel, fmt.format(self))
	if radio.player is not None and not radio.is_playing():
		radio.player.resume()

@bot.command()
async def skip():
	if radio.player.is_playing():
		radio.player.stop()
		radio.toggle_next_song()

@bot.group(pass_context=True)
async def play(ctx):
	global radio
	if radio.player is not None and radio.player.is_playing():
		await bot.say('Already playing a song')
		return
	if radio.songs.empty() and ctx.invoked_subcommand is None:
		await radio.random_q()
	while True:
		if not bot.is_voice_connected():
			await bot.say('Not connected to a voice channel')
			return

		radio.play_next_song.clear()
		radio.current = await radio.songs.get()
		radio.player = bot.voice.create_ffmpeg_player(radio.current, after=radio.toggle_next_song)
		radio.player.start()
		fmt = 'Playing song "{0}"'
		await bot.say(fmt.format(radio.current))
		await radio.play_next_song.wait()
	