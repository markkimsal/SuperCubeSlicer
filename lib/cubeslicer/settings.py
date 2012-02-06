import os
import sqlite3

smudge = 0.0004

def update_setting(skey, sval):

	import uuid, time

	insertSql = 'INSERT INTO app_setting (skey, sval, created_on, updated_on) \
			VALUES (?, ?, ?, ?)'

	updateSql = 'UPDATE app_setting set sval = ?, updated_on = ?  \
			WHERE skey = ?'
	try:
		db = cubeslicer.settings.DbDriver()
		db._query(updateSql, (sval, time.time(), skey))
		if (db._rowcount() == 0):
			db._query(insertSql, (skey, sval, time.time(), time.time()))
	except Exception:
		cubeslicer.settings._db_init()
		return this.fileList

	while db.next():
		this.fileList.append( FileModel.from_rec(db.rec) )



def get_settings_dir():
	home = os.getenv('USERPROFILE') or os.getenv('HOME')
	settings_dir = os.path.join(  home, ".supercubeslicer" )

	#print settings_dir
	if (not os.path.exists( settings_dir) ):
		os.mkdir( settings_dir )
	return settings_dir

def get_db_file():
	return os.path.join( get_settings_dir(), "scs.db" )


class DbDriver(object):

	def __init__(this):
		this.dbfile = get_db_file()
		this.rec  = ()
		this.cur  = None
		this.conn = None


	def _conn(this):
		this.conn = sqlite3.connect(this.dbfile)
		this.conn.row_factory = sqlite3.Row

	def _rowcount(this, SQL):
		if (not this.conn):
			return 0
		try:
			return this.conn.rowcount
		except sqlite3.Error, e:
			return 0


	def _query(this, SQL):
		if (not this.conn):
			this._conn()
		try:
			print SQL
			this.cur = this.conn.cursor()    
			x = this.cur.execute( SQL )
			this.conn.commit()
		except sqlite3.Error, e:
			print "Error: %s"%e.args[0]
			raise Exception(e.args[0])

	def next(this):
		this.rec = this.cur.fetchone()
		print this.rec
		return this.rec

	def _close(this):
		if this.conn:
			conn.close()

def _db_init():
	db = DbDriver()
	db._query('''CREATE TABLE IF NOT EXISTS project
			(project_id text, name text, created_on int)''')

	db._query('''CREATE TABLE IF NOT EXISTS file 
			(project_id text, file_name text, base_name text, created_on int)''')

	db._query('''CREATE TABLE IF NOT EXISTS app_setting
			(skey text, svalue text, created_on int, updated_on int)''')

