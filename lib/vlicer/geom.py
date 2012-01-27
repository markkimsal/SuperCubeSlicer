import math

class Point:

	def __init__(this, a, b, c=None):
		this.X = 0
		this.Y = 0
		this.Z = None
		this.X=a
		this.Y=b
		this.Z=c

class Line:


	def __init__(this, p):
		#p = Point(points[0], points[1])
		#if (len(points) > 2):
		#	p.c = points[2]
		this.len    = None
		this.points = dict()
		this.points['A'] = p[0]
		this.points['B'] = p[1]

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
			if this.points[p].Z is None:
				return True
		return False

	def a(this):
		return this.points['A']

	def b(this):
		return this.points['B']

	def length(this):
		if (this.len is not None):
			return this.len
		if (this.is_2d()):
			this.len = math.sqrt(  math.pow(this.b().X - this.a().X, 2) + math.pow(this.b().Y - this.a().Y, 2) )
		else:
			this.len = math.sqrt(  math.pow(this.b().X - this.a().X, 2) + math.pow(this.b().Y - this.a().Y, 2) + math.pow(this.b().Z - this.a().Z, 2))
		return this.len


class PolyLine(Line):
	pass


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
