import requests
import magic
import sqlite3
import discord
from connect import bot

#CREATE TABLE songs (title text, artist text, uploader text, url text, date text)

@bot.event
async def on_message(message):
	await bot.process_commands(message)
	
	if message.channel.name == "uploads_test" and message.attachments:
		upload = requests.get(message.attachments[0]["url"])
		mime = magic.from_buffer(upload.content, mime=True)
		if mime.startswith(b"audio"):
			db_conn = sqlite3.connect('uploads.db')
			db_cur = db_conn.cursor()
			db_cur.execute("INSERT INTO songs (uploader, url) \
							VALUES ({0.author.name}, {1})".format(message, message.attachments[0]["url"]))
			db_conn.commit()
			db_conn.close()