import os
import cubeslicer.geom
import cubeslicer.model
import unittest

class Test_Stl(unittest.TestCase):

	def test_ascii(self):
		df = ('ut', 'data', 'cube.stl')
		pipe = cubeslicer.slicer.Pipeline({'layerheight': 0.25, 'filename': os.sep.join(df)})
		model = pipe.newModel()
		pipe.appendPlugin('cubeslicer.plugins.parse_stl')
		#pipe.appendPlugin('cubeslicer.plugins.combine_straight_lines')
		pipe.runPipeline()


		#x = cubeslicer.model.parse_stl('/'.join(df), 0.25)
		for line in model.layers[0.25].lines:
			if line is None:
				print "None"
				continue
			#line = x.layers[0.2].lines[l]
			#print line.a().X, line.a().Y
			#print line.b().X, line.b().Y
