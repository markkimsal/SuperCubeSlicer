import pygame
from pygame.locals import *
import vlicer.model
import vlicer.geom
import wx

class PygameDisplay(wx.Panel):
    """wx Window subclass that draws a pygame surface onto a wx Device Context"""

    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        #pygame.display.init()
       
        self.SetClientRect( wx.Rect(20, 100, 20, 20) )
        print self.GetClientRect()
        print self.GetClientRect().GetTop()
        self.size = self.GetSizeTuple()
        self.size_dirty = True
       
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
       
        self.fps = 18.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.world = Viz_World(6)


    def UpdateLayer(self, idx):
        self.world.layer_set(idx);
        self.Redraw()
        pass


    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        #self.Redraw()
        #self.SetClientRect( wx.Rect(20, 100, 596, 179) )
        #print self.GetClientRect()
        #print self.GetClientRect().GetTop()
        pass

    def Redraw(self):
#        if self.size_dirty == False:
#            return
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        self.screen.fill((0,0,0))
        self.screen.blit( self.world.platform.image , (0, 0))
 
        cur = 0
 
        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        #dc = wx.PaintDC(self)
        dc = wx.BufferedPaintDC(self)
        #dc.SetBackground(wx.Brush('white'))
        #dc.Clear()
        #dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        #dc = wx.PaintDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc
 
    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        self.size_dirty = True

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)



class VZ_sprite:
	image =''
	x_pos =0
	y_pos =0
	rect  =0
	h_velocity = 0
	v_velocity = 0

	def __init__(this,i):
		this.x_pos = 20
		this.y_pos = 20
		this.image = i

	
	def paint(this,g):
		g.blit( this.image, (this.x_pos,this.y_pos))

	def update(this):
		if (this.h_velocity > 0 ):
			this.x_pos += 24;
			this.h_velocity = 0
		if (this.h_velocity < 0 ):
			this.x_pos -= 24;
			this.h_velocity = 0
		if (this.v_velocity > 0 ):
			this.y_pos -= 24;
			this.v_velocity = 0
		if (this.v_velocity < 0 ):
			this.y_pos += 24;
			this.v_velocity = 0


class VZ_sprite_platform(VZ_sprite):
	image =''
	color = ''
	x_pos =0
	y_pos =0
	rect  =0
	h_velocity = 0
	v_velocity = 0

	def __init__(this, size, color, zoom=2):
		this.x_pos = 0
		this.y_pos = 0
		this.size_x = size[0]
		this.size_y = size[1]
		this.color = color
		this.set_zoom(zoom)

	def set_zoom(this, zoom):
		this.zoom = zoom
		this.create_surf()

	def create_surf(this):
		this.image = pygame.Surface( (this.size_x*this.zoom, this.size_y*this.zoom) )
		this.erase()

	def erase(this):
		this.image.fill( this.color )

	def paint(this,g):
		g.blit( this.image, (this.x_pos,this.y_pos))

	def update(this):
		if (this.h_velocity > 0 ):
			this.x_pos += 2;
		if (this.h_velocity < 0 ):
			this.x_pos -= 2;
		if (this.v_velocity > 0 ):
			this.y_pos -= 2;
		if (this.v_velocity < 0 ):
			this.y_pos += 2;


class Viz_World:
	def __init__(this, zoom=1):
		this.zoom=zoom
		this.platform = VZ_sprite_platform( (210, 210) ,  pygame.Color( 250, 240, 200, 255 ))
		this.pen_color = pygame.Color( 50, 40, 10, 255 )
		this.grid_color = pygame.Color( 230, 220, 180, 255 )

		this.a_color = pygame.Color( 200, 100, 100 , 100)
		this.b_color = pygame.Color( 100, 100, 200 , 100)

		this.viz_layer = 1
		this.model = None
		this.erasePlatform()

	def erasePlatform(this):
		this.platform.erase()
		sx = this.platform.size_x * this.zoom
		sy = this.platform.size_y * this.zoom
		for h in range(10, sx, 10):
			h = h*this.zoom
			pygame.draw.line(this.platform.image, this.grid_color, (h, 0), (h, sy), 1)

		for w in range(10, sy, 10):
			w = w*this.zoom
			pygame.draw.line(this.platform.image, this.grid_color, (0, w), (sx, w), 1)


	def layer_up(this):
		this.viz_layer += 1
		if (len(this.model.layers) <= this.viz_layer):
			this.viz_layer -= 1
			#print "Layer is ", this.model.get_layer_z(this.viz_layer)
			return;
		#print "Layer is ", this.model.get_layer_z(this.viz_layer)
		this.erasePlatform()
		this.paint_model(this.platform.image, this.model)

	def layer_down(this):
		this.viz_layer -= 1
		if (0 > this.viz_layer):
			this.viz_layer += 1
			#print "Layer is ", this.model.get_layer_z(this.viz_layer)
			return;
		#print "Layer is ", this.model.get_layer_z(this.viz_layer)
		this.erasePlatform()
		this.paint_model(this.platform.image, this.model)

	def layer_set(this, idx):
		if (len(this.model.layers) <= idx and 0 > idx):
			print "Layer is ", this.model.get_layer_z(this.viz_layer)
			return;
		this.viz_layer = idx
		print "Layer is ", this.model.get_layer_z(this.viz_layer)
		this.erasePlatform()
		this.paint_model(this.platform.image, this.model)

	def paint_platform(this, g):
		g.blit( this.platform.image, (this.platform.x_pos, this.platform.y_pos))

	def set_model(this, model):
		this.model = model
		this.paint_model(this.platform.image, model)

	def paint_model(this, g, model):
		laykeys = model.layers.keys()
		laykeys.sort()
		try:
			layid = laykeys[this.viz_layer]
		except IndexError:
			return
		lay = model.layers[layid]
		for line in lay.lines:
			ax = int((line.a().X *this.zoom) + this.platform.size_x)
			bx = int((line.b().X *this.zoom)+ this.platform.size_x)
			ay = int((line.a().Y *this.zoom)+ this.platform.size_y)
			by = int((line.b().Y *this.zoom)+ this.platform.size_y)
			#print line.a().X, ax, line.b().X, bx
			pygame.draw.line(g, this.pen_color, (ax, ay), (bx, by), 1)
			pygame.draw.circle(g, this.a_color, (ax, ay), 4)
			pygame.draw.circle(g, this.b_color, (bx, by), 4)


	def get_updates(this):
		updates = pygame.Rect( (this.platform.x_pos, this.platform.y_pos, this.platform.size_x, this.platform.size_y) )

	def get_max_z(this):
		if this.model == None:
			return 0
		return this.model.get_max_z()


if __name__ == '__main__':
	pygame.display.init()
	window = pygame.display.set_mode( (512,448) )
	pygame.display.set_caption('Super Cube Slice (Alpha)')
	world = Viz_World(2)
	df = ('ut', 'data', 'cube.stl')
	model = vlicer.model.parse_stl('/'.join(df), 0.25)

	world.set_model(model)


	while ( 1 ):
		updates = world.get_updates()
		evt = pygame.event.poll()
		if evt.type != NOEVENT:
			#working over a network, mouse movements can really clog up the queue and
			# delay a close window or quit event
			pygame.event.clear(MOUSEMOTION)
		if (evt.type == QUIT or (evt.type == KEYDOWN and evt.key == K_ESCAPE) ):
			print 'got quit event'
			break

		if (evt.type == KEYDOWN and evt.key == K_UP):
			print "layer up"
			world.layer_up()
			print world.viz_layer
		if (evt.type == KEYDOWN and evt.key == K_DOWN):
			print "layer down"
			world.layer_down()
			print world.viz_layer

		window.fill( (0,0,0) )
		#sprite.update()
		world.paint_platform(window)
		#updates = updates.unionall( (updates,(sprite.x_pos,sprite.y_pos,244,244)) )
		pygame.display.update(updates)
		pygame.display.flip()
		pygame.time.wait(40)
