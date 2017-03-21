import time, psutil, argparse, os, sys, subprocess
from Gizmo_SerialLCD import *

lcd = Gizmo_SerialLCD("COM6", 9600, timeout=5)

def setupser():
	lcd.bigLCD()
	lcd.clear()

	for i in range(0,10):
		lcd.setIO(1, i)
		lcd.setAux(1, i)
	

def sample():
	setupser()
	
	lcd.scroll(0, "          Philrobotics")
	time.sleep(1)
	lcd.scroll(1, "          (c) n0th1n6")
	time.sleep(10)
	
	cpu = psutil.cpu_percent()
	mem = psutil.virtual_memory()	

	lcd.clear()
	lcd.write_to(0,"CPU and Memory",3)
	lcd.write_to(1,"PyPiMoni", 6);
	lcd.write_to(2,"CPU Util: " + str(cpu) + "%    ", 0);
	lcd.write_to(3,"Mem Util: " + str(mem[2]) + "%    ", 0);
	
def showCpuMemory():
	while 1 != 0:
		cpu = psutil.cpu_percent()
		mem = psutil.virtual_memory()
		
		lcd.write_to(2,str(cpu) + "%    ", 10);
		lcd.write_to(3,str(mem[2]) + "%    ", 10);
		time.sleep(5)
		#lcd.clearLine(1)	

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-D', '--daemon', action="store_true", help="Fork and run in background")
	args = parser.parse_args()
	
	if args.daemon:

		if os.fork()==0:
			os.setsid()
			sys.stdout=open("/dev/null", 'w')
			sys.stdin=open("/dev/null", 'r')

			if os.fork()==0:
				sample()
				showCpuMemory()
			sys.exit(0)

	else:
		sample()
		showCpuMemory()
