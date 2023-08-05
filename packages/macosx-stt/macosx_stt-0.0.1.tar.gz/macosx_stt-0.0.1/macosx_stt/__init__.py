import time
from pyobjus import autoclass, protocol
from pyobjus.dylib_manager import load_framework, INCLUDE
# load_framework(INCLUDE.AVFoundation)
# load_framework('/System/Library/Frameworks/AppKit.framework')
# load_framework('/System/Library/Frameworks/Foundation.framework')
# NSRunLoop = autoclass('NSRunLoop')
# NSDate = autoclass('NSDate')
# NSDefaultRunLoopMode = autoclass('NSDefaultRunLoopMode')
# Dispatcher = autoclass('Dispatcher')
# NSSpeechRecognizer = autoclass('NSSpeechRecognizer')
SFSpeechRecognizer = autoclass('SFSpeechRecognizer')

class MacosxSTTEngine:
	def __init__(self, proxy):
		auth = SFSpeechRecognizer.requestAuthorization { authStatus in

		self._stt = NSSpeechRecognizer.alloc()()
		if self._stt is None:
			raise Exception('stt driver init error')
		self._stt.delegate = self
		self._stt.commands = []
		self._stt.listenInForegroundOnly = True
		self._stt.blocksOtherRecognizers = True

	def setCommands(self, cmds):
		self._stt.commands = cmds

	def startListening(self):
		self._stt.startListening()

	def stopListening(self):
		self._stt.stopListening()

	def startLoop(self):
		loop = NSRunLoop.currentRunLoop()
		mode = loop.currentMode
		# self.dispatcher = Dispatcher()
		while loop.runMode(mode, beforeDate=time.time()+0.1):
			if not self.running:
				break

	def endLoop(self):
		self.running = False

	@protocol('NSSpeechRecognizerDelegate')
	def speechRecognizer_didRecognizeCommand(self, cmd):
		print('cmd recognized is', cmd)
	
