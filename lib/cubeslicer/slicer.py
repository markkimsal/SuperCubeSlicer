import cubeslicer.model

class Pipeline(object):


	def __init__(this, settings={}, model=None):
		this.model   = model
		this.plugins = []
		this.settings = settings
		this.currentStep=0

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

	def appendPlugin(this, plugName):
		#plugin =  __import__(plugName)
		plugin =  __import__(plugName, fromlist=['cubeslicer.plugins'])
		print plugin, plugName
		this.plugins.append(plugin)

	def resetPipleline(this, resetModel=False):
		this.currentStep = 0

	def runPipeline(this, steps=999):
		cur = this.currentStep
		if (cur + steps) >= len(this.plugins):
			steps = len(this.plugins) - cur

		for x in range(cur, cur+steps):
			print x, (this.plugins[this.currentStep])
			this.plugins[this.currentStep].process(this.model, this)
			this.currentStep = this.currentStep+1

	def step(this, steps=1):
		cur = this.currentStep
		if (cur + steps) >= len(this.plugins):
			steps = len(this.plugins) - cur

		for x in range(cur, cur+steps):
			print(this.plugins[this.currentStep])
			this.plugins[this.currentStep].process(this.model, this)
			this.currentStep+1

