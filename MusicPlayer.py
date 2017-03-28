from pygame import mixer # Load the required library
import pifacecad
from time import sleep
import datetime
import threading


def update_pin_text(event):
	 global pin
	 pin = event.pin_num

def print_ir_code(event):
	 global remote
	 remote = int(event.ir_code)
	 	 
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
	 
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
listener.activate()

remote_listener = pifacecad.IREventListener(prog='myprogram')
for i in range(8):
	remote_listener.register(str(i), print_ir_code)
remote_listener.activate()


song = ['Closer.mp3','Shape Of You.mp3','Starving.mp3','The Ocean.mp3','We Don\'t Talk Anymore.mp3']

def musicMainfunc():
	global pin
	global remote
	
	mixer.init()
	play = True
	mute = False
	curSong = 0
	volume = mixer.music.get_volume()
	pin = -1
	remote = -1
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
			now = datetime.datetime.now()
			nowTime = now.strftime('%H:%M')
			cad.lcd.set_cursor(10,1)
			cad.lcd.write(nowTime)
			
			# song control
			if pin == 1 or remote == 1:	# prev song
				curSong-=2
				if curSong==-2:
					curSong=len(song)-2
				pin = -1
				remote = -1
				break;
			if pin == 3 or remote == 3:	# next song
				pin = -1
				remote = -1
				break;
				
			if pin == 2 or remote == 2:	# play and pause
				if play:
					mixer.music.pause()
					play = False
				else:
					mixer.music.unpause()
					play = True
				pin = -1
				remote = -1
					
			# volume control
			if pin == 6 or remote == 6:	# volume down
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
			if pin == 7 or remote == 7:	# volume up
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
			if pin == 5 or remote == 5:
				if mute:
					mixer.music.set_volume(volume)
					mute = False
				else:
					mixer.music.set_volume(0)
					mute = True
				pin = -1
				remote = -1
		curSong+=1
		
main = threading.Thread(target=musicMainfunc)
main.start()
