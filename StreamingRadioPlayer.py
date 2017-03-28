import os
from time import sleep
import subprocess
import pifacecad
import threading
import datetime


path = '/tmp/mplayer-control'
curNum = 0
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.blink_off()
cad.lcd.cursor_off()
channelLink = ["mms://211.181.136.136/livefm", "mms://114.108.140.39/magicfm_live",\
				"mms://live.febc.net/LiveFm","mms://vod.ysmbc.co.kr/YSFM",\
				"mms://121.254.230.3/FMLIVE","mms://210.96.79.102/Incheon"]
channelName = ["MBC", "SBS","SeoulFBEC","YeosooMBC","JIBS","TBN"]
cad.lcd.write('CH : '+channelName[curNum])

pin = -1
remote = -1

def showTime():
	now = datetime.datetime.now()
	nowTime = now.strftime('%H:%M')
	cad.lcd.set_cursor(10,1)
	cad.lcd.write(nowTime)
	cad.lcd.set_cursor(0,0)

def print_ir_code(event):
	 global remote 
	 remote = int(event.ir_code)

def update_pin_text(event):
	 global pin
	 pin = event.pin_num
		
def radioMainFunc():
	global pin
	global curNum
	global remote
	while True:
		showTime()
		# play control
		if pin in [2, 5] or remote in [2, 5]:		# pause and unpause and mute
			subprocess.call('echo \"pause\" > /tmp/mplayer-control', shell=True)
			pin = -1
			remote = -1
		elif pin == 3 or remote == 3:	# next channel
			curNum = (curNum + 1) % len(channelLink)
			subprocess.call('echo \"loadfile '+channelLink[curNum] +'\" > /tmp/mplayer-control', shell=True)
			cad.lcd.clear()
			showTime()
			cad.lcd.write('CH : '+channelName[curNum])
			pin = -1
			remote = -1
		elif pin == 1 or remote == 1:	# prev channel
			if curNum == 0:
				curNum = len(channelLink)-1
			else:
				curNum -= 1
			subprocess.call('echo \"loadfile '+channelLink[curNum] +'\" > /tmp/mplayer-control', shell=True)
			cad.lcd.clear()
			showTime()
			cad.lcd.write('CH : '+channelName[curNum])
			pin = -1
			remote = -1
		# volume control
		elif pin == 6 or remote == 6:	# volume down
			while True:
				subprocess.call('echo \"volume -1\" > /tmp/mplayer-control', shell=True)
				sleep(0.1)
				remote = -1
				if not cad.switches[6].value:
					break
			pin = -1
		elif pin == 7 or remote == 7:	# volume up
			while True:
				subprocess.call('echo \"volume 1\" > /tmp/mplayer-control', shell=True)
				sleep(0.1)
				remote = -1
				if not cad.switches[7].value:
					break
			pin = -1
		
		
main = threading.Thread(target=radioMainFunc)
main.start()

			
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
listener.activate()

remote_listener = pifacecad.IREventListener(prog='myprogram')
for i in range(8):
	remote_listener.register(str(i), print_ir_code)
remote_listener.activate()

os.system('mplayer -slave -input file='+path+' '+channelLink[0])


	
