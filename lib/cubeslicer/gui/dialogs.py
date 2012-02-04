import wx

class NewProjectDialog(wx.Dialog):
	def __init__(
			this, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
			style=wx.DEFAULT_DIALOG_STYLE,
			useMetal=False,
			):

		# Instead of calling wx.Dialog.__init__ we precreate the dialog
		# so we can set an extra style that must be set before
		# creation, and then we create the GUI object using the Create
		# method.
		pre = wx.PreDialog()
		pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
		pre.Create(parent, ID, title, pos, size, style)

		# This next step is the most important, it turns this Python
		# object into the real wrapper of the dialog (instead of pre)
		# as far as the wxPython extension is concerned.
		this.PostCreate(pre)

		# This extra style can be set after the UI object has been created.
		if 'wxMac' in wx.PlatformInfo and useMetal:
			this.SetExtraStyle(wx.DIALOG_EX_METAL)


		# Now continue with the normal construction of the dialog
		# contents
		sizer = wx.BoxSizer(wx.VERTICAL)

		box = wx.BoxSizer(wx.HORIZONTAL)

		label = wx.StaticText(this, -1, "New Project Name:")
		label.SetHelpText("Just a simple name to keep track of one or more files.")
		box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

		this.text = wx.TextCtrl(this, -1, "New Project", size=(200,-1))
		this.text.SetHelpText("New Project")
		box.Add(this.text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

		sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

		line = wx.StaticLine(this, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
		sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

		btnsizer = wx.StdDialogButtonSizer()

		#align buttons right
		btnsizer.Add((200, 60), 0, wx.EXPAND)

		if wx.Platform != "__WXMSW__":
			btn = wx.ContextHelpButton(this)
			btnsizer.AddButton(btn)


		btn = wx.Button(this, wx.ID_OK)
		btn.SetHelpText("The OK button completes the dialog")
		btn.SetDefault()
		btnsizer.AddButton(btn)

		btn = wx.Button(this, wx.ID_CANCEL)
		btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
		btnsizer.AddButton(btn)
		btnsizer.Realize()

		sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)

		this.SetSizer(sizer)
		sizer.Fit(this)

	def getName(this):
		return this.text.GetValue()
