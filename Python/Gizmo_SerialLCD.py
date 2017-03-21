#######################################################
#	e-Gizmo Serial LCD 2 Driver
#	Get ir at: http://www.e-gizmo.com/oc/index.php?route=product/product&product_id=13&search=serial+lcd
#	nrafallo@gmail.com
#######################################################

from __future__ import print_function
from serial import Serial
import time

class Gizmo_SerialLCD(Serial):

	startChar	= b'\x02'
	endChar		= b'\x03'
	
	#command chars
	bLCD 			= "F"					#Initialize as 4x20 LCD Display, else 2x16
	clearDisp		= "c"					#Clear Display
	dispLine		= ("1", "2", "3", "4")	#Display to line 0-3
	clrLine			= ("5", "6", "7", "8")	#Clear & Display to line 0-3
	cursorPos		= ">"					#cursor position
	cmdScroll		= ("m", "M") 			#scroll display to line 0-1
	bLight			= "B"					#backlight Brightness 0-19
	cmdTestLCD		= "T"					#Test
	sAux			= ("R", "S")			#reset, set Aux Output
	readInput		= "I"					#Read input
	cmdIO			= ("i", "o")			#configure IO as input
	
	#config
	baudRate		= 9600
	sTime			= 5
	rTime			= 0.0
	
	def __init__(self, *args, **kwargs):
		if len(args) == 0:
			args = [ "/dev/ttyUSB0", self.baudRate ]
		elif len(args) == 1:
			args = [ args[0], self.baudRate ]
		else:
			baudrate = args[1]
			
		# i will use this later so I can get rid of wait_response() method
		self.byteTime = 11.0 / float(baudrate)

		Serial.__init__(self, *args, **kwargs)

	def wait_response(self):
		self.rTime  = time.time() + self.sTime
		rxchar = b'\x00'
		while(self.rTime - time.time() > 0):
			if (self.inWaiting()):
				rxchar=self.read(1)

			if (rxchar == b'\x03'): 
				self.rTime = 0.0
				return
		self.rTime = 0.0
		
	def write_command(self, message):
		self.write(self.startChar + message.encode() + self.endChar)
		self.wait_response()

	def write_to(self, line, message, pos):
		self.write_command(self.cursorPos + str(pos))
		self.write_command(self.dispLine[line] + message)

	def setIO(self, direction, port):
		self.write_command(self.cmdIO[direction] + str(port))
	
	def clearLine(self, line):
		self.write_command(self.clrLine[line])
	
	def setAux(self, direction, port):
		self.write_command(self.sAux[direction]+str([port]))
		
		
	def backLight(self, level):
		self.write_command(self.bLight+bytes([level]))
		
	def bigLCD(self):
		self.write_command(self.bLCD)
		
	def scroll(self, line, message):
		self.write_command(self.cmdScroll[line]+message)
		
	def testLCD(self):
		self.write_command(self.cmdTestLCD)
		
	def clear(self):
		self.write_command(self.clearDisp)