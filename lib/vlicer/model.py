import vlicer.geom

class Model2d:

	def __init__(this, zh=0.25):
		this.layers = dict()
		this.layer_height = zh

	def make_layer(this, lh):
		if not this.layers.has_key(lh):
			this.layers[lh] = Layer(lh)
		return this.layers[lh]

	def get_layer_z(this, layidx):
		k = this.layers.keys()
		k.sort()
		return k[layidx]

	def get_max_z(this):
		return len(this.layers)-1

class Layer:

	def __init__(this, h):
		this.height  = h
		this.lines   = []
		this.areas   = []


def parse_stl(filename, lh):
	try:
		fh = open(filename)
	except IOError:
		print "Cannot open file: ", filename
		return Model2d(0)
	except:
		print "Unexpected error: ", filename, sys.exc_info()[0]
		return Model2d(0)

	m = Model2d(lh)

	current_lh = 0.0
	facet = stl_read_facet_ascii(fh)
	facet_count = 0
	while (facet):
		facet_count+=1
		layer_height = frange(0, facet.get_max_z(), lh)
		for this_lh in layer_height:
			#this_lh = layer_height[lhidx]
			lay = m.make_layer(this_lh)
			#print facet_count
			#print facet.lines['C'].a().Z
			l = facet.intersect_line( this_lh )
			#print facet
			if l is not None:
				lay.lines.append( l )

		facet = stl_read_facet_ascii(fh)

	fh.close()
	return m


def stl_read_facet_ascii(fh):
	infacet = 0

	verts = []

	line = fh.readline().strip()
	while (line):
		if (infacet):
			if (line.find('endfacet') != -1):
				infacet = 0
				print "end facet", line
				break

			if (line.find('endloop') != -1):
				infacet = 0
				line = fh.readline().strip()
				continue

			if (line.find('vertex ') != -1):
				parts = line.split(' ')
				#print float(parts[-3]), float(parts[-2]), float(parts[-1])
				verts.append( vlicer.geom.Point( float(parts[-3]), float(parts[-2]), float(parts[-1])) ) 
			else :
				line = fh.readline().strip()
				continue

		if (not infacet):
			if (line.find('facet nor') != -1):
				infacet = 1
			if (line.find('endfacet') != -1):
				infacet = 0
				break


		line = fh.readline().strip()

	if (len(verts) == 3):
		face = vlicer.geom.Facet( verts )
		#print face
		return face
	else:
		print "not enough verticies!", len(verts)
	return None

def frange(start, stop=None, step=1.0, delta=0.0000001):
	"""
	a range generator that handles floating point numbers
	uses delta fuzzy logic to avoid float rep errors
	eg. stop=6.4 --> 6.3999999999999986 would slip through
	"""
	# if start is missing it defaults to zero
	if stop == None:
		stop = start
		start = 0.0
	# allow for decrement
	if step <= 0:
		while start > (stop + delta):
			yield start
			start += step
	else:
		while start < (stop - delta):
			yield start
			start += step
