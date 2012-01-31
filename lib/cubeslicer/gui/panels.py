import wx
import cubeslicer.gui.viz
import cubeslicer.workspace
import cubeslicer.model
import cubeslicer.slicer

class WorkspacePanel(wx.Panel):
	def __init__(this, parent, id):
		wx.Panel.__init__(this, parent, id, style= wx.SIMPLE_BORDER)
		this.parent     = parent

		tb = wx.ToolBar(this, style= (wx.TB_HORIZONTAL| wx.TB_TEXT | wx.TB_NOICONS))
		#bmp = wx.Bitmap("media/icons/tango/Folder.png", wx.BITMAP_TYPE_PNG)
		bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN)
		tb.AddLabelTool(10, "New Project", bmp)
		tb.AddLabelTool(20, "Import STL", bmp)
		tb.AddLabelTool(30, "Import STL as new Project", bmp)

		this.tree       = this._makeTree()
		this._populateTree()

		#this.viz        = this.makeVisualizer(parent, id)
		this.viz        = VizPanel(this, id)

		this.upsizer    = wx.BoxSizer(wx.VERTICAL)
		this.sizer      = wx.BoxSizer(wx.HORIZONTAL)
		this.sizer.Add(this.tree, 0,  wx.EXPAND)
		this.sizer.Add(this.viz,      1,  wx.EXPAND)

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
		isz = (36,36)
		il = wx.ImageList(isz[0], isz[1])
		fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
		fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
		fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))

		tree.SetImageList(il)
		this.il = il

		this.Bind(wx.EVT_TREE_ITEM_ACTIVATED, this.OnActivate, tree)

		this.root = tree.AddRoot("Workspace")
		tree.SetPyData(this.root, None)
		tree.SetItemImage(this.root, fldridx, wx.TreeItemIcon_Normal)
		tree.SetItemImage(this.root, fldropenidx, wx.TreeItemIcon_Expanded)
		return tree

	def _populateTree(this):
		model = cubeslicer.workspace.WorkspaceModel()
		proj  = model.projects()
		itm = this.tree.AppendItem(this.root, "Hollow Pyramid")

		isz = (36,36)
		il = wx.ImageList(isz[0], isz[1])
		fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
		fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
		fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))

		this.tree.SetItemImage(itm, fldridx, wx.TreeItemIcon_Normal)
		this.tree.SetItemImage(itm, fldropenidx, wx.TreeItemIcon_Expanded)

	def OnActivate(this, event):
		itm = event.GetItem()
		df = ('ut', 'data', 'hollow_pyramid.stl')
		#df = ('ut', 'data', 'cube.stl')
		#model = cubeslicer.model.parse_stl('/'.join(df), 0.10)

		#df = ('ut', 'data', 'cube.stl')
		import os
		pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25, 'filename': os.sep.join(df)})
		model = pipe.newModel()
		pipe.appendPlugin('cubeslicer.plugins.parse_stl')
		pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
		pipe.runPipeline()

		this.viz.display.world.set_model(model)
		this.viz.slider.SetMax( this.viz.display.world.get_max_z() )
		this.viz.slider.SetMin( 1 )
		this.viz.display.UpdateLayer(1);



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

 
	def OnScroll(self, event):
		#self.display.linespacing = self.slider.GetValue()
		self.display.size_dirty = False
		self.display.UpdateLayer(self.slider.GetValue())

 
