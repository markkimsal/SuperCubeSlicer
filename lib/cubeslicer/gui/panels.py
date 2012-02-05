import wx
import cubeslicer.gui.viz
import cubeslicer.gui.events
import cubeslicer.gui.dialogs
import cubeslicer.workspace
import cubeslicer.model
import cubeslicer.slicer

class PageWithText(wx.Panel):
    def __init__(this, parent, title):
        wx.Panel.__init__(this, parent)
        t = wx.StaticText(this, -1, title, (60,60))

class WorkspacePanel(wx.Panel):
	def __init__(this, parent, id):
		wx.Panel.__init__(this, parent, id, style= wx.SIMPLE_BORDER)
		this.parent     = parent

		cubeslicer.gui.events.set_evt_handler(this.GetEventHandler())

		this.Bind(cubeslicer.gui.events.CS_PROJ_CREATE_EVT, cubeslicer.workspace.new_project_event, id=10)

		this.Bind(cubeslicer.gui.events.CS_PROJ_SELECT_EVT, this.OnProjectSelected, id=10)

		this.Bind(cubeslicer.gui.events.CS_FILE_IMPORT_EVT, cubeslicer.workspace.import_file, id=10)

		this.Bind(cubeslicer.gui.events.CS_PROJ_CHANGED_EVT, this._populateTree, id=10)

		tb = wx.ToolBar(this, style= (wx.TB_HORIZONTAL| wx.TB_TEXT | wx.TB_NOICONS))
		#bmp = wx.Bitmap("media/icons/tango/Folder.png", wx.BITMAP_TYPE_PNG)
		bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
		tb.AddLabelTool(10, "New Project", bmp)
		tb.AddLabelTool(20, "Import STL", bmp)
		tb.EnableTool(20, False)
		#tb.AddLabelTool(30, "Import STL as new Project", bmp)

		#tb.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
		this.Bind(wx.EVT_TOOL, this.OnToolClick, id=10)
		this.Bind(wx.EVT_TOOL, this.OnToolClick, id=20)
		this.tb = tb

		this.tree       = this._makeTree()

		this._populateTree()

		this.Bind(wx.EVT_TREE_SEL_CHANGED, this.OnSelect, this.tree)

		this.viz         = None
		#this.viz        = this.makeVisualizer(parent, id)
		#this.viz        = VizPanel(this, id)

		this.settingsPage = PageWithText (this, "Placeholder")

		this.upsizer    = wx.BoxSizer(wx.VERTICAL)
		this.sizer      = wx.BoxSizer(wx.HORIZONTAL)
		this.sizer.Add(this.tree, 0,  wx.EXPAND)
		#this.sizer.Add(this.viz,      1,  wx.EXPAND)
		#this.sizer.Detach(this.viz)
		this.sizer.Add(this.settingsPage,      1,  wx.EXPAND)

		this.upsizer.Add(tb, 0, wx.EXPAND)
		this.upsizer.Add(this.sizer, 1, wx.EXPAND)

		this.SetSizer(this.upsizer)
		this.Layout()

	def makeVisualizer(this, parent, id):
		return VizPanel(parent, id)

	def makeListbook(this):
		lb = wx.Listbook(this, -1, style= \
			wx.BK_DEFAULT \
		)
		il = wx.ImageList(32, 32)
		bmp = wx.Bitmap("media/icons/tango/Folder.png", wx.BITMAP_TYPE_PNG)
		#bmp.LoadFile( )
		il.Add(bmp)
		lb.AssignImageList(il)

		win = wx.Panel(lb, -1)
		lb.AddPage(win, "Project", imageId=0)
		return lb


	def _makeTree(this):
		tID             = wx.NewId()
		tree = wx.TreeCtrl(this, tID, wx.DefaultPosition, wx.DefaultSize, \
				(wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS) )

		this.Bind(wx.EVT_TREE_ITEM_ACTIVATED, this.OnActivate, tree)

		return tree

	def _populateTree(this, evt=None):
		this.tree.DeleteAllItems()
		isz = (36,36)
		il = wx.ImageList(isz[0], isz[1])
		fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
		fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
		fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))

		this.root = this.tree.AddRoot("Workspace")
		this.tree.SetPyData(this.root, None)
		this.tree.SetItemImage(this.root, fldridx, wx.TreeItemIcon_Normal)
		this.tree.SetItemImage(this.root, fldropenidx, wx.TreeItemIcon_Expanded)
		this.tree.SetImageList(il)
		this.il = il


		model = cubeslicer.workspace.WorkspaceModel()
		proj  = model.projects()
		for _proj in proj:
			itm = this.tree.AppendItem(this.root, _proj.name, image=-1, selectedImage=-1, data=wx.TreeItemData(_proj))
			this.tree.SetItemImage(itm, fldridx, wx.TreeItemIcon_Normal)
			this.tree.SetItemImage(itm, fldropenidx, wx.TreeItemIcon_Expanded)

			itm2 = this.tree.AppendItem(itm, 'Hollow Pyramid', image=-1, selectedImage=-1, data=wx.TreeItemData( ('ut', 'data', 'hollow_pyramid.stl') ))
			this.tree.SetItemImage(itm2, fileidx, wx.TreeItemIcon_Normal)

		this.tree.Expand(this.root)

	def OnActivate(this, event):
		itm = event.GetItem()

		data = this.tree.GetItemData(itm)

		if not data:
			return

		if isinstance(data.GetData(), cubeslicer.workspace.ProjectModel):
			return

		# assume we activated an stl file
		df = data.GetData()

		this.runViz(df)

	def runViz(this, df):
		import os
		pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25, 'filename': os.sep.join(df)})
		model = pipe.newModel()
		pipe.appendPlugin('cubeslicer.plugins.parse_stl')
		pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
		pipe.appendPlugin('cubeslicer.plugins.find_polylines')
		pipe.runPipeline()

		this.viz.display.world.set_model(model)
		this.viz.slider.SetMax( this.viz.display.world.get_max_z() )
		this.viz.slider.SetMin( 1 )
		this.viz.display.UpdateLayer( 1 );


	def OnSelect(this, event):
		itm = event.GetItem()
		if itm == this.root:
			this.tb.EnableTool(20, False)
			return

		if itm:
			data = this.tree.GetItemData(itm)
			if (not data):
				this.tb.EnableTool(20, False)
				print "not proj"
				return

			if isinstance(data.GetData(), cubeslicer.workspace.ProjectModel):
				evt = wx.PyCommandEvent( cubeslicer.gui.events.CS_PROJ_SELECT, 10)
				evt.SetString( data.GetData().project_id )
				this.GetEventHandler().ProcessEvent(evt)
				evt.Skip()

			else:
				#assume STL click
				this.showViz()
				this.runViz(data.GetData())

		event.Skip()

	def showViz(this):
		this.sizer.Remove(1)
		if this.viz is None:
			this.viz        = VizPanel(this, -1)
		this.sizer.Add(this.viz,      1,  wx.EXPAND)
		this.sizer.Layout()

	def OnProjectSelected(this, event):
		proj_id = event.GetString()

		this.tb.EnableTool(20, True)
		this.selectedProject = cubeslicer.workspace.WorkspaceModel.get_project(proj_id);
		print this.selectedProject
		print "Selected project: %s"%this.selectedProject.project_id
		event.Skip()


	def OnToolClick(this, event):
		tb = event.GetEventObject()
		toolid = event.GetId()
		if (toolid == 10):
			dlg = cubeslicer.gui.dialogs.NewProjectDialog(this, -1,  "New Project")
			dlg.CenterOnScreen()
			val = dlg.ShowModal()
			if val == wx.ID_OK:
				dlg.getName()
				evt = wx.PyCommandEvent( cubeslicer.gui.events.CS_PROJ_CREATE, 10)
				evt.SetString( dlg.getName() )
				this.GetEventHandler().ProcessEvent(evt)
				evt.Skip()
				#cubeslicer.gui.events.ProjectNewEvent(dlg.getName())

		if (toolid == 20):
			import os
			dlg = wx.FileDialog(
				this, message="Choose a file",
				defaultDir=os.getcwd(), 
				defaultFile="",
				style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
				)
			dlg.CenterOnScreen()
			val = dlg.ShowModal()
			if val == wx.ID_OK:
				paths = dlg.GetPaths()
				evt = wx.PyCommandEvent( cubeslicer.gui.events.CS_FILE_IMPORT, 10)
				evt.SetClientData( paths )
				evt.SetString( this.selectedProject.project_id )
				this.GetEventHandler().ProcessEvent(evt)
				evt.Skip()
				#cubeslicer.gui.events.ProjectNewEvent(dlg.getName())


class VizPanel(wx.Panel):
	def __init__(this, parent, id):
		wx.Panel.__init__(this, parent, id,  style= wx.SIMPLE_BORDER)

		this.display = cubeslicer.gui.viz.PygameDisplay(this, -1)

		max_z = this.display.world.get_max_z()
		this.slider = wx.Slider(this, wx.ID_ANY, 5, 1, max_z, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
		this.slider.SetTickFreq(0.1, 1)

		this.Bind(wx.EVT_SCROLL, this.OnScroll)

		this.sizer      = wx.BoxSizer(wx.VERTICAL)
		this.sizer.Add(this.display, 1, wx.EXPAND)
		this.sizer.Add(this.slider, 0,  wx.EXPAND)
		this.SetSizer(this.sizer)
		this.Layout()

 
	def OnScroll(this, event):
		#this.display.linespacing = this.slider.GetValue()
		this.display.size_dirty = False
		this.display.UpdateLayer(this.slider.GetValue())

 
