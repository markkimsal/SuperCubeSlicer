import math

class Point:

	def __init__(this, a, b, c=None):
		this.X = 0
		this.Y = 0
		this.Z = None

		this.X=a
		this.Y=b
		this.X=float('%.4f'%a)
		this.Y=float('%.4f'%b)
		this.Z=c
		if (c is not None):
			this.Z = round(this.Z, 4)

	def is_greater(this, point):
		if (this.X >= point.X and this.Y > point.Y):
			return 1
		else:
			return 0

	def is_equal(this, point):
		if (round(this.X,4) == round(point.X,4) and round(this.Y,4) == round(point.Y,4)):
			return 1
		else:
			return 0

	def __str__(this):
		if (this.Z is None):
			return '(%f, %f)'%(this.X, this.Y)
		else:
			return '(%f, %f)'%(this.X, this.Y)
			#return '(%f, %f, %f)'%(this.X, this.Y, this.Z)

	def __repr__(this):
		return this.__str__()


class Line:

	def __init__(this, p):
		#p = Point(points[0], points[1])
		#if (len(points) > 2):
		#	p.c = points[2]
		this.len    = None
		this.points = []
		if p[0].is_greater(p[1]):
			this.points.append( p[1] )
			this.points.append( p[0] )
		else:
			this.points.append( p[0] )
			this.points.append( p[1] )

	@classmethod
	def from_tupples(this, t1, t2):
		p1 = Point( t1[0], t1[1] )
		p2 = Point( t2[0], t2[1] )
		if (len(t1) > 2):
			p1.Z = t1[2]

		if (len(t2) > 2):
			p2.Z = t2[2]

		l = Line( (p1, p2) )
		return l

	def is_2d(this) :
		for p in this.points:
			if p.Z is None:
				return True
		return False

	def a(this):
		return this.points[0]

	def b(this):
		return this.points[len(this.points)-1]

	def length(this):
		if (this.len is not None):
			return this.len
		if (this.is_2d()):
			this.len = math.sqrt(  math.pow(this.b().X - this.a().X, 2) + math.pow(this.b().Y - this.a().Y, 2) )
		else:
			this.len = math.sqrt(  math.pow(this.b().X - this.a().X, 2) + math.pow(this.b().Y - this.a().Y, 2) + math.pow(this.b().Z - this.a().Z, 2))
		return this.len


import hashlib
class PolyLine(Line):

	def __init__(this, line1=None, line2=None):
		this.len    = None
		this.points = []
		if line1 == None:
			return
		if isinstance( line1, PolyLine):
			line1.extend(line2)
			this.points = line1.points
		elif isinstance( line2, PolyLine):
			line2.extend(line1)
			this.points = line2.points
		else:
			this.combine(line1, line2)

	def extend(this, line):
		"""There are three possibilities for extending a polyline with a line
		Case 1
		PolyLine:
		
				b
				|
			a---.

		New Line

			b
			|
			a

		Result

			a    b
			|    |
			.----.

		Case 2
		PolyLine:
		
				b
				|
			a---.

		New Line

			a---b

		Result

			b---.
			    |
			a---.

		Case 3
		PolyLine:
		
			b---.
			    |
			a---.

		New Line

			a
			|
			b

		Result

			 .---.
			 |   |
			a/b--.

		"""

		newpoints = []
		if this.a().is_equal(line.a()) \
			and this.b().is_equal(line.b()):
				this.points.append(line.a())
				return

		if this.a().is_equal(line.b()) \
			and this.b().is_equal(line.a()):
				this.points.append(line.b())
				return

		if this.a().is_equal(line.a()):
			newpoints.append(line.b())
			for p in this.points:
				newpoints.append( p )
			this.points = newpoints
			return

		if this.b().is_equal(line.b()):
			for p in this.points:
				newpoints.append( p )
			newpoints.append(line.a())
			this.points = newpoints
			return

		if this.b().is_equal(line.a()):
			for p in this.points:
				newpoints.append( p )
			newpoints.append(line.b())
			this.points = newpoints
			return

		if this.a().is_equal(line.b()):
			newpoints.append(line.a())
			for p in this.points:
				newpoints.append( p )
			this.points = newpoints
			return

	def combine(this, line1, line2):
		newpoints = []
		if line1.a().is_equal(line2.a()):
			newpoints.append(line2.b())
			for p in line1.points:
				newpoints.append( p )
			this.points = newpoints
			return

		if line1.b().is_equal(line2.b()):
			for p in line1.points:
				newpoints.append( p )
			newpoints.append(line2.a())
			this.points = newpoints
			return

		if line1.b().is_equal(line2.a()):
			for p in line1.points:
				newpoints.append( p )
			newpoints.append(line2.b())
			this.points = newpoints
			return

		if line1.a().is_equal(line2.b()):
			newpoints.append(line2.a())
			for p in line1.points:
				newpoints.append( p )
			this.points = newpoints
			return
	"""
	def combine(this, line1, line2):
		if line2.a().is_greater(line1.a()):
			greater      = line2
			lesser       = line1
		else:
			greater      = line1
			lesser       = line2

		newpoints = []
		newpoints.append(lesser.a())
		#this.points['A'] = lesser.a()

		newpoints.append(lesser.b())

		if (greater.b().X == lesser.b().X) and \
			(greater.b().Y == lesser.b().Y):
				newpoints.append( greater.a() )
		else:
				newpoints.append( greater.b() )
		this.points = newpoints
		"""

	@classmethod
	def combine_lines(this, line1, line2):
		poly = PolyLine()
		poly.points['A']           = line1.a()

		m = hashlib.sha1()
		m.update(str(line1.b()))
		poly.points[ m.digest() ]  = line1.b()

		poly.points['B']           = line2.b()
		return poly


class Facet():

	def __init__(this, verts):
		this.lines = dict()
		if len(verts) < 2:
			raise Exception ('not enough verts for facet')
		this.lines['A'] =  Line( (verts[0], verts[1]) )
		this.lines['B'] =  Line( (verts[1], verts[2]) )
		this.lines['C'] =  Line( (verts[2], verts[0]) )

	def get_max_z(this):
		max_z = 0
		for key, l in this.lines.iteritems():
			a = l.a()
			b = l.b()
			if (a.Z > max_z):
				max_z = a.Z

			if (b.Z > max_z):
				max_z = b.Z
		return max_z
			

	def intersect_line(this, z):
		smudge=0.00004
		points = []
		keys = this.lines.keys()
		keys.sort()
		for f in keys:
			fline = this.lines[f]
			a = fline.a()
			b = fline.b()

			# edge intersects the current layer; calculate intersection
			if ((a.Z < (z - smudge) and b.Z > (z + smudge)) or (b.Z < (z - smudge) and a.Z > (z + smudge))):
				p = Point( b.X + (a.X - b.X) * (z - b.Z) / (a.Z - b.Z),  b.Y + (a.Y - b.Y) * (z - b.Z) / (a.Z - b.Z), z)
				points.append( p ) 
				#print p.X, p.Y, p.Z
				#print 'plane ', z, ' intersects ', f, ' between ', a.Z, ' ',  b.Z
			else:
				pass
				#print f, ' line ', z, ' is not between ', a.Z, ' ',  b.Z

		if (len (points) == 2):
			line = Line ( (points[0], points[1]) )
			return line
		else:
			#print "plane didn't intersect 2 points ", len(points)
			pass
			#print points
		return None
