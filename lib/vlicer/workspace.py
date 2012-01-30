import os
import vlicer.settings

class WorkspaceModel(object):

	def __init__(this):
		this.projList = []

	def projects(this):
		db = vlicer.settings.DbDriver()
		db._query("SELECT * FROM projects")
		while db.next():
			this.projList.append(db.rec)
			print db.rec

		#this.dbfile = vlicer.settings.get_db_file()
		return this.projList

