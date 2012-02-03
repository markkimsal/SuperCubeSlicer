import cubeslicer.geom
import cubeslicer.model
import cubeslicer.slicer
import unittest
import json
import os

class Test_Plugins(unittest.TestCase):

	def test_points(self):

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

	def test_complex_layer(self):

		model = cubeslicer.model.Model2d()
		lay = model.make_layer(1)
		
		df = ('ut', 'data', 'test_plugins_layer.json')
		filename = os.sep.join(df);

		struct = json.loads(open(filename).read())

		for line in struct['lines']:
			points = []
			for point in line['points']:
				p = cubeslicer.geom.Point( point['X'], point['Y'] )
				points.append( p ) 
			newline = cubeslicer.geom.Line( (points[0], points[1]) )
			lay.lines.append(newline)


		pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25}, model)
		#model = pipe.newModel()
		#pipe.appendPlugin('cubeslicer.plugins.parse_stl')
		pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
		pipe.runPipeline()

		print lay.lines
		self.assertEqual( 4, len(lay.lines))

if __name__ == '__main__':
	    unittest.main()
