import sys
import time

sys.path.append('..')
import macosx_stt

x = macosx_stt.buildDriver(None)

x.startListening()
while True:
	time.sleep(0.001)
