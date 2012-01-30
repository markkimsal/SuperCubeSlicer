import os
import sqlite3

def get_settings_dir():
	home = os.getenv('USERPROFILE') or os.getenv('HOME')
	settings_dir = os.path.join(  home, ".supercubeslicer" )

	print settings_dir
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

	def _query(this, SQL):
		if (not this.conn):
			this._conn()
		try:
			this.cur = this.conn.cursor()    
			this.cur.execute('SELECT SQLITE_VERSION()')


		except sqlite3.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)

	def next(this):
		this.rec = this.cur.fetchone()
		return this.rec

	def _close(this):
		if this.conn:
			conn.close()
