import sqlite3

class Settings:
	def __init__(self):
		self.database = "settings.db"
		self.copy_radio_path = "radio/"
	
	def bot_auth(self):
		db_conn = sqlite3.connect(self.database)
		db_cur = db_conn.cursor()
		reqst = db_cur.execute("SELECT bot_login, bot_passwd FROM settings").fetchone()
		auth_data = {'login': reqst[0], 'passwd': reqst[1]}
		db_conn.close()
		return auth_data
		
	def copy_auth(self):
		db_conn = sqlite3.connect(self.database)
		db_cur = db_conn.cursor()
		reqst = db_cur.execute("SELECT copy_login, copy_passwd FROM settings").fetchone()
		auth_data = {'login': reqst[0], 'passwd': reqst[1]}
		db_conn.close()
		return auth_data
		
settings = Settings()
		