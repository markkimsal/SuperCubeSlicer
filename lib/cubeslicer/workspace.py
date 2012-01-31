import os
import cubeslicer.settings

class WorkspaceModel(object):

	def __init__(this):
		this.projList = []

	def projects(this):
		db = cubeslicer.settings.DbDriver()
		db._query("SELECT * FROM projects")
		while db.next():
			this.projList.append(db.rec)
			print db.rec

		#this.dbfile = cubeslicer.settings.get_db_file()
		return this.projList

