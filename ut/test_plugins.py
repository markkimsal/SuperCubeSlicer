import vlicer.geom
import vlicer.model
import vlicer.slicer
import unittest

class Test_Plugins(unittest.TestCase):

	def test_points(self):
		df = ('ut', 'data', 'cube.stl')

		model = vlicer.model.Model2d()
		lay = model.make_layer(1)

		p1 = vlicer.geom.Point(   10,   10 )
		p2 = vlicer.geom.Point(  -10,  -10 )
		l = vlicer.geom.Line( (p1, p2) )

		lay.lines.append( l )

		p1 = vlicer.geom.Point(   10,   10 )
		p2 = vlicer.geom.Point(   20,   20 )
		l = vlicer.geom.Line( (p1, p2) )

		lay.lines.append( l )

		pipe = vlicer.slicer.Pipeline({'layerheight': 0.25}, model)
		#model = pipe.newModel()
		#pipe.appendPlugin('vlicer.plugins.parse_stl')
		pipe.appendPlugin('vlicer.plugins.combine_straight_lines')
		pipe.runPipeline()

if __name__ == '__main__':
	    unittest.main()
