import pygame
from pygame.locals import *
import vlicer.model
import vlicer.geom


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

	def __init__(this, size, zoom=2):
		this.x_pos = 0
		this.y_pos = 0
		this.size_x = size[0]
		this.size_y = size[1]
		this.color = pygame.Color( 250, 240, 200, 255 )
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
		this.platform = VZ_sprite_platform( (210, 210) )
		this.pen_color = pygame.Color( 50, 40, 10, 255 )
		this.viz_layer = 0
		this.model = None

	def layer_up(this):
		this.viz_layer += 1
		if (len(this.model.layers) <= this.viz_layer):
			this.viz_layer -= 1
			print "Layer is ", this.model.get_layer_z(this.viz_layer)
			return;
		print "Layer is ", this.model.get_layer_z(this.viz_layer)
		this.platform.erase()
		this.paint_model(this.platform.image, this.model)

	def layer_down(this):
		this.viz_layer -= 1
		if (0 > this.viz_layer):
			this.viz_layer += 1
			print "Layer is ", this.model.get_layer_z(this.viz_layer)
			return;
		print "Layer is ", this.model.get_layer_z(this.viz_layer)
		this.platform.erase()
		this.paint_model(this.platform.image, this.model)

	def paint_platform(this, g):
		g.blit( this.platform.image, (this.platform.x_pos, this.platform.y_pos))

	def set_model(this, model):
		this.model = model
		this.paint_model(this.platform.image, model)

	def paint_model(this, g, model):
		laykeys = model.layers.keys()
		laykeys.sort()
		layid = laykeys[this.viz_layer]
		lay = model.layers[layid]
		for line in lay.lines:
			ax = (line.a().X *this.zoom) + this.platform.size_x/2
			bx = (line.b().X *this.zoom)+ this.platform.size_x/2
			ay = (line.a().Y *this.zoom)+ this.platform.size_y/2
			by = (line.b().Y *this.zoom)+ this.platform.size_y/2
			print line.a().X, ax, line.b().X, bx
			pygame.draw.line(g, this.pen_color, (ax, ay), (bx, by), 1)

	def get_updates(this):
		updates = pygame.Rect( (this.platform.x_pos, this.platform.y_pos, this.platform.size_x, this.platform.size_y) )


if __name__ == '__main__':
	pygame.display.init()
	window = pygame.display.set_mode( (512,448) )
	pygame.display.set_caption('Fresh Cube Slice (Alpha)')
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

		"""
		if (evt.type == KEYDOWN and evt.key == K_RIGHT):
			sprite.h_velocity = 1
			sprite.is_accelerating = 1
		if (evt.type == KEYDOWN and evt.key == K_LEFT):
			sprite.h_velocity = -1
			sprite.is_accelerating = 1
		if (evt.type == KEYUP and (evt.key == K_RIGHT or evt.key == K_LEFT)):
			sprite.h_velocity = 0
			sprite.is_accelerating = 0
		if (evt.type == KEYDOWN and evt.key == K_UP):
			sprite.v_velocity = 1
			sprite.is_accelerating = 1
		if (evt.type == KEYDOWN and evt.key == K_DOWN):
			sprite.v_velocity = -1
			sprite.is_accelerating = 1
		if (evt.type == KEYUP and (evt.key == K_UP or evt.key == K_DOWN)):
			sprite.v_velocity = 0
			sprite.is_accelerating = 0
		"""

		window.fill( (0,0,0) )
		#sprite.update()
		world.paint_platform(window)
		#updates = updates.unionall( (updates,(sprite.x_pos,sprite.y_pos,244,244)) )
		pygame.display.update(updates)
		pygame.display.flip()
		pygame.time.wait(40)
