import cubeslicer.geom
import cubeslicer.model
import cubeslicer.slicer
import unittest

class Test_Plugins(unittest.TestCase):

	def test_points(self):
		df = ('ut', 'data', 'cube.stl')

		model = cubeslicer.model.Model2d()
		lay = model.make_layer(1)

		p1 = cubeslicer.geom.Point(   10,   10 )
		p2 = cubeslicer.geom.Point(  -10,  -10 )
		l = cubeslicer.geom.Line( (p1, p2) )

		lay.lines.append( l )

		p1 = cubeslicer.geom.Point(   10,   10 )
		p2 = cubeslicer.geom.Point(   20,   20 )
		l = cubeslicer.geom.Line( (p1, p2) )

		lay.lines.append( l )

		pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25}, model)
		#model = pipe.newModel()
		#pipe.appendPlugin('cubeslicer.plugins.parse_stl')
		pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
		pipe.runPipeline()

if __name__ == '__main__':
	    unittest.main()
