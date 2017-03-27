from pygame import mixer # Load the required library
import pifacecad
from time import sleep
import datetime


def print_ir_code(event):
	 global remote
	 remote = int(event.ir_code)
	 
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
listener = pifacecad.IREventListener(prog='myprogram')
for i in range(8):
	listener.register(str(i), print_ir_code)
listener.activate()


song = ['Closer.mp3','Shape Of You.mp3','Starving.mp3','The Ocean.mp3','We Don\'t Talk Anymore.mp3']
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
mixer.init()

play = True
mute = False
curSong = 0
volume = mixer.music.get_volume()
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
		if cad.switches[1].value or remote == 1:	# prev song
			sleep(0.3)
			curSong-=2
			if curSong==-2:
				curSong=len(song)-2
			remote = -1
			break;
		if cad.switches[3].value or remote == 3:	# next song
			sleep(0.3)
			remote = -1
			break;
			
		if cad.switches[2].value or remote == 2:	# play and pause
			sleep(0.2)
			if play:
				mixer.music.pause()
				play = False
			else:
				mixer.music.unpause()
				play = True
			remote = -1
				
		# volume control
		if cad.switches[6].value or remote == 6:	# volume down
			sleep(0.1)
			volume -= 0.05
			if volume < 0:
				volume = 0
			mixer.music.set_volume(volume)
			remote = -1
		if cad.switches[7].value or remote == 7:	# volume up
			sleep(0.1)
			volume += 0.05
			if volume > 1:
				volume = 1
			mixer.music.set_volume(volume)
			remote = -1
		if cad.switches[5].value or remote == 5:
			sleep(0.2)
			if mute:
				mixer.music.set_volume(volume)
				mute = False
			else:
				mixer.music.set_volume(0)
				mute = True
			remote = -1
	curSong+=1
