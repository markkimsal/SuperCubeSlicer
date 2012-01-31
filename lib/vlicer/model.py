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


