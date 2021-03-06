# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from random import random
from GlyphsApp.plugins import *


class Erode(FilterWithDialog):
	# Definitions of IBOutlets
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	# Text field in dialog
	segmentsUI = objc.IBOutlet()
	segProbabilityUI = objc.IBOutlet()
	spikinessUI = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Erode'})
		NSUserDefaults.standardUserDefaults().registerDefaults_({'org.simon-cozens.erode.segments':200,
																 'org.simon-cozens.erode.segProbability': 0.6,
																 'org.simon-cozens.erode.spikiness': 5})
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		self.segmentsUI.setStringValue_(Glyphs.defaults['org.simon-cozens.erode.segments'])
		self.segProbabilityUI.setFloatValue_(Glyphs.defaults['org.simon-cozens.erode.segProbability'])
		self.spikinessUI.setFloatValue_(Glyphs.defaults['org.simon-cozens.erode.spikiness'])
		self.segmentsUI.becomeFirstResponder()

	# Action triggered by UI
	@objc.IBAction
	def setValue_(self, sender):
		# Store values coming in from dialog
		Glyphs.defaults['org.simon-cozens.erode.segments'] = self.segmentsUI.stringValue()
		Glyphs.defaults['org.simon-cozens.erode.segProbability'] = self.segProbabilityUI.floatValue()
		Glyphs.defaults['org.simon-cozens.erode.spikiness'] = self.spikinessUI.intValue()
		# Trigger redraw
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		# Called on font export, get value from customParameters
		if 'segments' in customParameters:
			segments = float(customParameters['segments'])
			segProbability = customParameters['segProbability']
			spikiness = customParameters['spikiness']
		else:
			segments = float(Glyphs.defaults['org.simon-cozens.erode.segments'])
			spikiness = Glyphs.defaults['org.simon-cozens.erode.spikiness']
			segProbability = Glyphs.defaults['org.simon-cozens.erode.segProbability']

		layer.beginChanges()
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
		layer.endChanges()

	@objc.python_method
	def generateCustomParameter(self):
		return "%s; teeth:%s;" % (self.__class__.__name__, Glyphs.defaults['org.simon-cozens.erode.teeth'])
