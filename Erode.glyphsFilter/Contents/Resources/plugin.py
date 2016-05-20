# encoding: utf-8
from GlyphsApp.plugins import *
from random import random

class Erode(FilterWithDialog):
	# Definitions of IBOutlets
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	# Text field in dialog
	segmentsUI = objc.IBOutlet()
	segProbabilityUI = objc.IBOutlet()
	spikinessUI = objc.IBOutlet()

	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Erode'})

		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog')

	# On dialog show
	def start(self):
		self.segmentsUI.setStringValue_(Glyphs.defaults['org.simon-cozens.erode.segments'] or 200)
		self.segProbabilityUI.setFloatValue_(Glyphs.defaults['org.simon-cozens.erode.segProbability'] or 0.6)
		self.spikinessUI.setFloatValue_(Glyphs.defaults['org.simon-cozens.erode.spikiness'] or 5)
		self.segmentsUI.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_( self, sender ):
		# Store values coming in from dialog
		Glyphs.defaults['org.simon-cozens.erode.segments'] = self.segmentsUI.stringValue()
		Glyphs.defaults['org.simon-cozens.erode.segProbability'] = self.segProbabilityUI.floatValue()
		Glyphs.defaults['org.simon-cozens.erode.spikiness'] = self.spikinessUI.intValue()
		# Trigger redraw
		self.update()

	# Actual filter
	def filter(self, layer, inEditView, customParameters):
		# Called on font export, get value from customParameters
		if customParameters.has_key('segments'):
			segments = float(customParameters['segments'])
			segProbability = customParameters['segProbability']
			spikiness = customParameters['spikiness']
		else:
			segments = float(Glyphs.defaults['org.simon-cozens.erode.segments'])
			spikiness = Glyphs.defaults['org.simon-cozens.erode.spikiness']
			segProbability = Glyphs.defaults['org.simon-cozens.erode.segProbability']

		for p1 in layer.paths:
			pathTime = p1.countOfNodes()

			while pathTime > 0:
				pathTime -= 1.0/segments
				if random() < segProbability:
					p1.insertNodeWithPathTime_(pathTime)
					pathTime -= 0.5/segments
					n1 = p1.insertNodeWithPathTime_(pathTime)
					if n1:
						uv = p1.unitVectorAtNodeAtIndex_(p1.indexOfNode_(n1))
						if uv.x > 0: uv.x =1 
						else: uv.x = -1
						if uv.y > 0: uv.y = 1
						else: uv.x = -1
						n1.position = (n1.position.x - random()*spikiness*uv.y, n1.position.y + random() * spikiness*uv.x)
					pathTime -= 0.5/segments
					p1.insertNodeWithPathTime_(pathTime)

	def generateCustomParameter( self ):
		return "%s; teeth:%s;" % (self.__class__.__name__, Glyphs.defaults['org.simon-cozens.erode.teeth'] )
