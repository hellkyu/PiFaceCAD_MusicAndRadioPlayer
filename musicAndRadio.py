from pygame import mixer # Load the required library
import pifacecad
from time import sleep
import datetime
import threading
import os
import subprocess


cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.blink_off()
cad.lcd.cursor_off()

# music
song = ['Closer.mp3','Shape Of You.mp3','Starving.mp3','The Ocean.mp3','We Don\'t Talk Anymore.mp3']

# radio
path = '/tmp/mplayer-control'
channelLink = ["mms://211.181.136.136/livefm", "mms://114.108.140.39/magicfm_live",\
				"mms://live.febc.net/LiveFm","mms://vod.ysmbc.co.kr/YSFM",\
				"mms://121.254.230.3/FMLIVE","mms://210.96.79.102/Incheon"]
channelName = ["MBC", "SBS","SeoulFBEC","YeosooMBC","JIBS","TBN"]


pin = -1
remote = -1


def update_pin_text(event):
	 global pin
	 pin = event.pin_num

def print_ir_code(event):
	 global remote
	 remote = int(event.ir_code)
	 
def showTime():
	now = datetime.datetime.now()
	nowTime = now.strftime('%H:%M')
	cad.lcd.set_cursor(10,1)
	cad.lcd.write(nowTime)
	cad.lcd.set_cursor(0,0)

def musicMainfunc():
	global pin
	global remote
	
	play = True
	mute = False
	curSong = 0
	pin = -1
	remote = -1
	
	mixer.init()
	volume = mixer.music.get_volume()
	while True:
		if curSong == len(song):
			curSong = 0
		cad.lcd.clear()
		cad.lcd.blink_off()
		cad.lcd.cursor_off()
		mixer.music.load(song[curSong])
		cad.lcd.write(song[curSong])
		mixer.music.play()
		
		while mixer.music.get_busy() == True:
			showTime()
			
			# song control
			if pin == 1 or remote == 1:	# prev song
				curSong-=2
				if curSong==-2:
					curSong=len(song)-2
				pin = -1
				remote = -1
				break;
			elif pin == 3 or remote == 3:	# next song
				pin = -1
				remote = -1
				break;
				
			elif pin == 2 or remote == 2:	# play and pause
				if play:
					mixer.music.pause()
					play = False
				else:
					mixer.music.unpause()
					play = True
				pin = -1
				remote = -1
					
			# volume control
			elif pin == 6 or remote == 6:	# volume down
				while True:
					volume -= 0.05
					if volume < 0:
						volume = 0
					mixer.music.set_volume(volume)
					sleep(0.1)
					if not cad.switches[6].value:
						break
					pin = -1
					remote = -1
			elif pin == 7 or remote == 7:	# volume up
				while True:
					volume += 0.05
					if volume > 1:
						volume = 1
					mixer.music.set_volume(volume)
					sleep(0.1)
					if not cad.switches[7].value:
						break
				pin = -1
				remote = -1
			elif pin == 5 or remote == 5:	# mute
				if mute:
					mixer.music.set_volume(volume)
					mute = False
				else:
					mixer.music.set_volume(0)
					mute = True
				pin = -1
				remote = -1
			elif pin == 4 or remote == 4: 
				pin = -1
				remote = -1
				mixer.quit()
				return
		curSong+=1
		
		
def radioMainFunc():
	global pin
	global remote
	curNum = 0
	cad.lcd.clear()
	showTime()
	cad.lcd.write('CH : '+channelName[curNum])
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
		elif pin == 4 or remote == 4: 
				pin = -1
				remote = -1
				subprocess.call('echo \"quit\" > /tmp/mplayer-control', shell=True)
				return
			

def mainFunc():
	listener = pifacecad.SwitchEventListener(chip=cad)
	for i in range(8):
		listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
	listener.activate()

	remote_listener = pifacecad.IREventListener(prog='myprogram')
	for i in range(8):
		remote_listener.register(str(i), print_ir_code)
	remote_listener.activate()

	#musicMain = threading.Thread(target=musicMainfunc)
	radioMain = threading.Thread(target=radioMainFunc)
	while True:
		os.system('rm '+path)
		os.system('mkfifo '+path)
		musicMainfunc()
		radioMain = threading.Thread(target=radioMainFunc)
		radioMain.start()
		os.system('mplayer -slave -input file='+path+' '+channelLink[0])
		radioMain.join()
	
	
mainFunc()
			




