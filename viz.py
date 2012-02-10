import os, sys, math, logging
try :
	sys.path.append ( os.path.join( sys.path[0], 'lib')  )
except Exception as e:
	print "can't locate library path lib"

import pygame
from pygame.locals import *
import cubeslicer.model
import cubeslicer.geom
import cubeslicer.gui.viz
import cubeslicer.slicer


def encode_obj(obj):
	    return obj.__dict__

if __name__ == '__main__':
	logging.basicConfig(format='%(levelname)-6s %(message)s')
	rootLogger = logging.getLogger('')
	rootLogger.setLevel(logging.DEBUG)

	pygame.display.init()
	window = pygame.display.set_mode( (512,448) )

	pygame.display.set_caption('Super Cube Slice (Alpha)')
	world = cubeslicer.gui.viz.Viz_World(8)
	#df = ('ut', 'data', 'cube.stl')
	df = ('ut', 'data', 'hollow_pyramid.stl')
	pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25, 'filename': os.sep.join(df)})
	model = pipe.newModel()
	pipe.appendPlugin('cubeslicer.plugins.parse_stl')
	pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
	#pipe.appendPlugin('cubeslicer.plugins.find_polylines')
	pipe.runPipeline()

	import json
	print json.dumps( model.layers[3.0], default=encode_obj, indent=4)
	world.set_model(model)

	layer_accel = 0
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
			layer_accel=1
		if (evt.type == KEYDOWN and evt.key == K_DOWN):
			layer_accel=-1

		if (evt.type == KEYUP and (evt.key == K_UP or evt.key == K_DOWN)):
			layer_accel=0

		if (layer_accel == -1):
			world.layer_down()
			logging.info( "layer down: %d", world.viz_layer )

		if (layer_accel == 1):
			world.layer_up()
			logging.info( "layer up: %d", world.viz_layer )

		window.fill( (0,0,0) )
		world.paint_platform(window)
		#updates = updates.unionall( (updates,(sprite.x_pos,sprite.y_pos,244,244)) )
		pygame.display.update(updates)
		pygame.display.flip()
		pygame.time.wait(80)
