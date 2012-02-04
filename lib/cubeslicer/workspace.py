import os
import cubeslicer.settings

class ProjectModel(object):

	def __init__(this, name, proj_id):
		this.name = name
		this.project_id = proj_id

	@classmethod
	def from_rec(this, rec):
		return ProjectModel( rec['name'], rec['project_id'] )


class WorkspaceModel(object):

	def __init__(this):
		this.projList = []

	def projects(this):
		try:
			db = cubeslicer.settings.DbDriver()
			db._query("SELECT * FROM project")
		except Exception:
			this.create_table()
			return this.projList

		while db.next():
			this.projList.append( ProjectModel.from_rec(db.rec) )

		#this.dbfile = cubeslicer.settings.get_db_file()
		return this.projList

	@classmethod
	def get_project(this, proj_id):
		db = cubeslicer.settings.DbDriver()
		db._query("SELECT * FROM project WHERE project_id='%s'"%(proj_id))
		db.next()
		return ProjectModel.from_rec(db.rec)

	def new_project(this, name):
		import uuid
		proj_id = uuid.uuid1()
		db = cubeslicer.settings.DbDriver()
		db._query("insert into project (project_id, name) VALUES ('%s', '%s')"%(proj_id, name))

	def create_table(this):
		db = cubeslicer.settings.DbDriver()
		db._query('''create table project
				(project_id text, name text)''')

def new_project_event(event):
	import uuid
	proj_id = uuid.uuid1()
	name = event.GetString()
	db = cubeslicer.settings.DbDriver()
	print "insert into project (project_id, name) VALUES ('%s', '%s')"%(proj_id, name)
	db._query("insert into project (project_id, name) VALUES ('%s', '%s')"%(proj_id, name))

def fire_project_changed():
	evt = wx.PyCommandEvent( cubeslicer.gui.events.CS_PROJ_CREATE, 10)
	evt.SetString( dlg.getName() )
	this.GetEventHandler().ProcessEvent(evt)
	evt.Skip()
