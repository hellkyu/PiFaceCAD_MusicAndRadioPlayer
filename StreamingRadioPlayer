import os
from time import sleep
import subprocess
import pifacecad


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
cad.lcd.write(channelName[curNum])


def print_ir_code(event):
	 global remote
	 remote = int(event.ir_code)

def update_pin_text(event):
	# play control
	if event.pin_num in [2, 5]:		# pause and unpause and mute
		subprocess.call('echo \"pause\" > /tmp/mplayer-control', shell=True)
	elif event.pin_num == 3:	# next channel
		global curNum
		curNum = (curNum + 1) % len(channelLink)
		subprocess.call('echo \"loadfile '+channelLink[curNum] +'\" > /tmp/mplayer-control', shell=True)
		cad.lcd.clear()
		cad.lcd.write(channelName[curNum])
	elif event.pin_num == 1:	# prev channel
		global curNum
		if curNum == 0:
			curNum = len(channelLink)-1
		else:
			curNum -= 1
		subprocess.call('echo \"loadfile '+channelLink[curNum] +'\" > /tmp/mplayer-control', shell=True)
		cad.lcd.clear()
		cad.lcd.write(channelName[curNum])
	# volume control
	elif event.pin_num == 6:	# volume down
		while cad.switches[6].value:
			subprocess.call('echo \"volume -1\" > /tmp/mplayer-control', shell=True)
			sleep(0.1)
	elif event.pin_num == 7:	# volume up
		while cad.switches[7].value:
			subprocess.call('echo \"volume 1\" > /tmp/mplayer-control', shell=True)
			sleep(0.1)
	
		
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
listener.activate()

os.system('mplayer -slave -input file='+path+' '+channelLink[0])
