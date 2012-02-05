import wx
evtHandler = None

def get_evt_handler():
	global evtHandler
	return evtHandler

def set_evt_handler(eh):
	global evtHandler
	evtHandler = eh

CS_PROJ_CREATE          = wx.NewEventType()
CS_PROJ_CREATE_EVT      = wx.PyEventBinder(CS_PROJ_CREATE, 1)

CS_PROJ_CHANGED         = wx.NewEventType()
CS_PROJ_CHANGED_EVT     = wx.PyEventBinder(CS_PROJ_CHANGED, 1)

CS_PROJ_SELECT          = wx.NewEventType()
CS_PROJ_SELECT_EVT      = wx.PyEventBinder(CS_PROJ_SELECT, 1)

CS_FILE_IMPORT          = wx.NewEventType()
CS_FILE_IMPORT_EVT      = wx.PyEventBinder(CS_FILE_IMPORT, 1)
