import sqlite3

class Settings:
	def __init__(self):
		self.database = "settings.db"
		self.copy_radio_path = "radio/"
	
	def bot_auth(self):
		db_conn = sqlite3.connect(self.database)
		db_cur = db_conn.cursor()
		login  = db_cur.execute("SELECT value FROM settings WHERE setting='bot_login'").fetchone()[0]
		passwd = db_cur.execute("SELECT value FROM settings WHERE setting='bot_passwd'").fetchone()[0]
		db_conn.close()
		return {'login': login, 'passwd': passwd}
		
	def copy_auth(self):
		db_conn = sqlite3.connect(self.database)
		db_cur = db_conn.cursor()
		login  = db_cur.execute("SELECT value FROM settings WHERE setting='copy_login'").fetchone()[0]
		passwd = db_cur.execute("SELECT value FROM settings WHERE setting='copy_passwd'").fetchone()[0]
		db_conn.close()
		return {'login': login, 'passwd': passwd}
		
settings = Settings()
		