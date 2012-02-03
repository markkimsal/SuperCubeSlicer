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


	def test_polyline(self):
		p1      = cubeslicer.geom.Point( 1, 1 )
		p2      = cubeslicer.geom.Point( 3, 3)
		line1   = cubeslicer.geom.Line( (p1, p2) )

		p3      = cubeslicer.geom.Point( 3, 3 )
		p4      = cubeslicer.geom.Point( 5, 5)
		line2   = cubeslicer.geom.Line( (p3, p4) )

		p5      = cubeslicer.geom.Point( 5, 5 )
		p6      = cubeslicer.geom.Point( 10, 5)
		line3   = cubeslicer.geom.Line( (p5, p6) )

		polyline = cubeslicer.geom.PolyLine(line1, line2)
		self.assertEqual( 3, len(polyline.points) )

		polyline2 = cubeslicer.geom.PolyLine(polyline, line3)
		self.assertEqual( 4, len(polyline2.points) )

	def test_irregular_polyline(self):
		p1      = cubeslicer.geom.Point( 1, 1 )
		p2      = cubeslicer.geom.Point( 3, 3)
		line1   = cubeslicer.geom.Line( (p1, p2) )

		p3      = cubeslicer.geom.Point( 5, 5 )
		p4      = cubeslicer.geom.Point( 3, 3)
		line2   = cubeslicer.geom.Line( (p3, p4) )

		p5      = cubeslicer.geom.Point( 10, 5 )
		p6      = cubeslicer.geom.Point( 1, 1)
		line3   = cubeslicer.geom.Line( (p5, p6) )

		polyline = cubeslicer.geom.PolyLine(line2, line1)
		self.assertEqual( 3, len(polyline.points) )
		
		self.assertEqual(  5, polyline.b().X )
		self.assertEqual(  5, polyline.b().Y )

		self.assertEqual(  1, polyline.a().X )
		self.assertEqual(  1, polyline.a().Y )


		polyline2 = cubeslicer.geom.PolyLine(polyline, line3)
		for pnt in polyline2.points:
			print pnt.X, pnt.Y
	
		self.assertEqual( 4, len(polyline2.points) )

		#self.assertEqual( 10, polyline2.points['B'].X )
		#self.assertEqual(  5, polyline2.points['B'].Y )

		#self.assertEqual(  1, polyline2.points['A'].X )
		#self.assertEqual(  1, polyline2.points['A'].Y )

		#for idx, pnt in polyline2.points.iteritems():
		#	print idx, pnt.X, pnt.Y
	
