import os
import cubeslicer.settings

class ProjectModel(object):

	def __init__(this, name, proj_id):
		this.name = name
		this.project_id = proj_id
		this.fileList = []

	@classmethod
	def from_rec(this, rec):
		return ProjectModel( rec['name'], rec['project_id'] )

	def get_files(this):
		try:
			db = cubeslicer.settings.DbDriver()
			db._query("SELECT * FROM file where project_id='%s'"%this.project_id)
		except Exception:
			cubeslicer.settings._db_init()
			return this.fileList

		while db.next():
			this.fileList.append( FileModel.from_rec(db.rec) )

		#this.dbfile = cubeslicer.settings.get_db_file()
		return this.fileList


class FileModel(object):
	def __init__(this, file_name, base_name, proj_id):
		this.file_name = file_name
		this.base_name = base_name
		this.project_id = proj_id
		this.fileList = []

	@classmethod
	def from_rec(this, rec):
		return FileModel( rec['file_name'], rec['base_name'], rec['project_id'] )


class WorkspaceModel(object):

	def __init__(this):
		this.projList = []

	def projects(this):
		try:
			db = cubeslicer.settings.DbDriver()
			db._query("SELECT * FROM project")
		except Exception:
			cubeslicer.settings._db_init()
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

	"""
	def new_project(this, name):
		import uuid, 
		proj_id = uuid.uuid1()
		db = cubeslicer.settings.DbDriver()
		db._query("insert into project (project_id, name) VALUES ('%s', '%s')"%(proj_id, name))

	"""

def new_project_event(event):
	import uuid, time
	proj_id = uuid.uuid1()
	name = event.GetString()
	db = cubeslicer.settings.DbDriver()
	db._query("insert into project (project_id, name, created_on) VALUES ('%s', '%s', %d)"%(proj_id, name, time.time()))
	fire_project_changed()

def fire_project_changed():
	import wx, cubeslicer.gui.events
	evt = wx.PyCommandEvent( cubeslicer.gui.events.CS_PROJ_CHANGED, 10)
	#this.GetEventHandler().ProcessEvent(evt)
	#print dir(wx.PostEvent)
	#wx.EvtHandler.GetNextHandler().ProcessEvent(evt)
	cubeslicer.gui.events.get_evt_handler().ProcessEvent(evt)
	evt.Skip()

def import_file(event):
	import time, os
	proj_id   = event.GetString();
	paths     = event.GetClientData()
	name = paths[0]
	base_name = os.path.basename(name)

	db = cubeslicer.settings.DbDriver()
	#print "insert into file (project_id, file_name, created_on) VALUES ('%s', '%s', %d)"%(proj_id, name, time.time())
	db._query("insert into file (project_id, file_name, base_name, created_on) VALUES ('%s', '%s', '%s', %d)"%(proj_id, name, base_name, time.time()))
	fire_project_changed()
