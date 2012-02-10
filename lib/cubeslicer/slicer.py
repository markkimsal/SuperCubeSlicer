import cubeslicer.model

class Pipeline(object):


	def __init__(this, settings={}, model=None):
		this.model          = model
		this.model_plugins  = []
		this.layer_plugins  = []
		this.settings       = settings
		this.currentStep      = 0
		this.currentStepLayer = 0
		this.currentLayer     = 0

	def newModel(this, lh=None):
		if lh is not None:
			this.setLayerHeight(lh)
		else:
			lh = this.getSetting('layerheight')
		this.model = cubeslicer.model.Model2d(lh)
		return this.model

	def setFilename(this, fn):
		this.settings['filename'] = fn

	def setLayerHeight(this, lh):
		this.settings['layerheight'] = lh

	def getSetting(this, key):
		return this.settings[ key ]

	def appendPlugin(this, plugName, scope='model'):
		#plugin =  __import__(plugName)
		plugin =  __import__(plugName, fromlist=['cubeslicer.plugins'])
		if scope == 'model':
			this.model_plugins.append(plugin)
		if scope == 'layer':
			this.layer_plugins.append(plugin)

	def resetPipleline(this, resetModel=False):
		this.currentStep       = 0
		this.currentStepLayer  = 0
		this.currentLayer  = 0
		if resetModel:
			this.model.reset()

	def runPipeline(this, steps=999):
		cur = this.currentStep
		if (cur + steps) >= len(this.model_plugins):
			steps = len(this.model_plugins) - cur

		for x in range(cur, cur+steps):
			#print x, (this.model_plugins[this.currentStep])
			this.model_plugins[this.currentStep].process(this.model, this)
			this.currentStep = this.currentStep+1

	def stepLayer(this, layer_id, steps=999):
		cur = this.currentStepLayer
		if (cur + steps) >= len(this.layer_plugins):
			steps = len(this.layer_plugins) - cur

		for x in range(cur, cur+steps):
			#print x, (this.plugins[this.currentStep])
			this.layer_plugins[this.currentStepLayer].process_layer(this.model, this.model.layers[ this.model.get_layer_z(layer_id)], this)
			this.currentStepLayer+1

	def step(this, steps=1):
		cur = this.currentStep
		if (cur + steps) >= len(this.model_plugins):
			steps = len(this.model_plugins) - cur

		for x in range(cur, cur+steps):
			#print(this.model_plugins[this.currentStep])
			this.model_plugins[this.currentStep].process(this.model, this)
			this.currentStep+1

