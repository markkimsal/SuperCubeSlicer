import vlicer.geom
import vlicer.model
import unittest

class Test_Stl(unittest.TestCase):

	def test_ascii(self):
		df = ('ut', 'data', 'cube.stl')
		x = vlicer.model.parse_stl('/'.join(df), 0.25)
		for line in x.layers[0.2].lines:
			if line is None:
				print "None"
				continue
			#line = x.layers[0.2].lines[l]
			print line.a().X, line.a().Y
			print line.b().X, line.b().Y
