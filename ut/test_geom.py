import cubeslicer.geom
import unittest

class Test_Geometry(unittest.TestCase):

	def test_points(self):
		p = cubeslicer.geom.Point( 1, -2 )
		self.assertEqual( p.X, 1)
		self.assertEqual( p.Y, -2)
		self.assertEqual( p.Z, None)

	def test_lines(self):
		p1 = cubeslicer.geom.Point( 1, -2 )
		p2 = cubeslicer.geom.Point( 2, 3 , 0)
		l = cubeslicer.geom.Line( (p1, p2) )

		self.assertEqual( l.a().X, 1)

		l2 = cubeslicer.geom.Line.from_tupples( (0, 0, 0) , (10, 10, 10) )

		self.assertEqual( l2.b().X, 10)

		self.assertTrue( (l2.length() -  17.3205) < 0.0001 )

	def test_facet(self):
		
		p1 = cubeslicer.geom.Point(  0,  0,  0 )
		p2 = cubeslicer.geom.Point(  0, 10,  0 )
		p3 = cubeslicer.geom.Point(  0,  0, 10 )
		face = cubeslicer.geom.Facet( (p1, p2, p3) )

		l = face.intersect_line( 2 )
		self.assertEqual( 8, l.length() )
