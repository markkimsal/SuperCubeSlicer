import wx
CS_PROJ_CREATE          = wx.NewEventType()
CS_PROJ_CREATE_EVT      = wx.PyEventBinder(CS_PROJ_CREATE, 1)

CS_PROJ_CHANGED         = wx.NewEventType()
CS_PROJ_CHANGED_EVT     = wx.PyEventBinder(CS_PROJ_CHANGED, 1)

CS_PROJ_SELECT          = wx.NewEventType()
CS_PROJ_SELECT_EVT      = wx.PyEventBinder(CS_PROJ_SELECT, 1)
