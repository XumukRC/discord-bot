import asyncio
from os import listdir, system
from os.path import isfile, join
import random
from urllib.parse import unquote
from collections import deque

import discord
from connect import bot
import uploads
from settings import settings

import api.pycopy as pycopy


if not discord.opus.is_loaded():
	discord.opus.load_opus('/usr/local/lib/libopus.so') #FreeBSD path

class Radio:
	def __init__(self):
		#self.songs = asyncio.Queue()
		self.songs = deque()
		self.play_next_song = asyncio.Event()
		#self.starter = None
		self.player = None
		self.current = None
		self.copycom = pycopy.Copy(settings.copy_auth()['login'], settings.copy_auth()['passwd'])
		self.files = self.copycom.list_files(settings.copy_radio_path)

	def toggle_next_song(self):
		bot.loop.call_soon_threadsafe(self.play_next_song.set)

	def can_control_song(self, author):
		return author == self.starter or (self.current is not None and author == self.current.requester)

	def is_playing(self):
		return self.player is not None and self.player.is_playing()
	
	async def test_q(self):
		#await self.songs.put(self.copycom.direct_link("test.mp3"))
		self.songs.append(self.copycom.direct_link("test.mp3"))

	async def random_q(self):
		q = random.sample(self.files, len(self.files))
		for song in q:
			song_path = settings.copy_radio_path + song
			#print(song_path)
			#await self.songs.put(song_path)
			self.songs.append(song_path)

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
	if radio.player.is_playing():
		radio.player.stop()
	system("killall ffmpeg")
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
	if radio.player is not None and not radio.is_playing():
		radio.player.resume()

@bot.command()
async def skip():
	if radio.player.is_playing():
		radio.player.stop()
		radio.toggle_next_song()
		
@bot.command()
async def stop():
	global radio
	if radio.player.is_playing():
		radio.player.stop()

@bot.group(pass_context=True)
async def play(ctx):
	global radio
	if radio.player is not None and radio.player.is_playing():
		await bot.say('Already playing a song')
		return
	if len(radio.songs) == 0 and ctx.invoked_subcommand is None:
		await radio.random_q()
	while True:
		if not bot.is_voice_connected():
			await bot.say('Not connected to a voice channel')
			return

		radio.play_next_song.clear()
		#radio.current = await radio.songs.get()
		radio.current = radio.songs.popleft()
		#print(radio.current)
		radio.player = bot.voice.create_ffmpeg_player(radio.copycom.direct_link(radio.current), after=radio.toggle_next_song, options="-headers '{}' -loglevel debug -report".format(radio.copycom.get_headers_str()))
		radio.player.start()
		fmt = 'Playing song "{0}"'
		await bot.say(fmt.format(unquote(radio.current.split('/')[-1])))
		#await bot.say(fmt.format(unquote(radio.current)))
		await radio.play_next_song.wait()
		

@bot.command()
async def list():
	global radio
	song_list = ""
	id = 0
	for song in radio.files:
		song_list += "{}. {}\n".format(id, song)
		id += 1
	await bot.say(song_list)
	
@bot.group(pass_context=True)
async def q(ctx):
	global radio
	if ctx.invoked_subcommand is None:
		song_list = ""
		id = 0
		for song in radio.songs:
			song_list += "{}. {}\n".format(id, song)
			id += 1
		await bot.say(song_list)
		
@q.command()
async def random():
	global radio
	await radio.random_q()
	await bot.say("Random Queue generated.")

		

