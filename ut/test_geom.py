import vlicer.geom
import unittest

class Test_Geometry(unittest.TestCase):

	def test_points(self):
		p = vlicer.geom.Point( 1, -2 )
		self.assertEqual( p.X, 1)
		self.assertEqual( p.Y, -2)
		self.assertEqual( p.Z, None)

	def test_lines(self):
		p1 = vlicer.geom.Point( 1, -2 )
		p2 = vlicer.geom.Point( 2, 3 , 0)
		l = vlicer.geom.Line( (p1, p2) )

		self.assertEqual( l.a().X, 1)

		l2 = vlicer.geom.Line.from_tupples( (0, 0, 0) , (10, 10, 10) )

		self.assertEqual( l2.b().X, 10)

		self.assertTrue( (l2.length() -  17.3205) < 0.0001 )

	def test_facet(self):
		
		p1 = vlicer.geom.Point(  0,  0,  0 )
		p2 = vlicer.geom.Point(  0, 10,  0 )
		p3 = vlicer.geom.Point(  0,  0, 10 )
		face = vlicer.geom.Facet( (p1, p2, p3) )

		l = face.intersect_line( 2 )
		self.assertEqual( 8, l.length() )
