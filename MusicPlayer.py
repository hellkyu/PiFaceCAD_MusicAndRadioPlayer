from pygame import mixer # Load the required library
import pifacecad
from time import sleep
import datetime

pin = -1
remote = -1
volume = 50
play = True
mute = False

song = ['Closer','Shape Of You','Starving','The Ocean','We Don\'t Talk Anymore','Happy'\
		,'Daft Punk', 'Chandelier','The Greatest', 'Lean On']

# init LCD
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
cad.lcd.blink_off()
cad.lcd.cursor_off()

# bitmap
bmp_note = pifacecad.LCDBitmap([2,3,2,2,14,30,12,0])
bmp_play = pifacecad.LCDBitmap([0,8,12,14,12,8,0,0])
bmp_pause = pifacecad.LCDBitmap([0,27,27,27,27,27,0,0])
bmp_clock = pifacecad.LCDBitmap([0,14,21,23,17,14,0,0])
bmp_vol1 = pifacecad.LCDBitmap([1,3,15,15,15,3,1,0])
bmp_vol2 = pifacecad.LCDBitmap([8,16,0,24,0,16,8,0])

cad.lcd.store_custom_bitmap(0, bmp_note)
cad.lcd.store_custom_bitmap(1, bmp_play)
cad.lcd.store_custom_bitmap(2, bmp_pause)
cad.lcd.store_custom_bitmap(3, bmp_clock)
cad.lcd.store_custom_bitmap(4, bmp_vol1)
cad.lcd.store_custom_bitmap(5, bmp_vol2)

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
	cad.lcd.write_custom_bitmap(3)
	cad.lcd.write(nowTime)
	cad.lcd.set_cursor(0,0)
	
def writeVolume():
	global volume
	global mute
	cad.lcd.set_cursor(0,1)
	cad.lcd.write_custom_bitmap(4)
	cad.lcd.write_custom_bitmap(5)
	if mute:
		cad.lcd.write('mute')
	else:
		cad.lcd.write(str(volume).rjust(4))
	
def updateVolume():
	global volume
	cad.lcd.set_cursor(2,1)
	if mute:
		cad.lcd.write('mute')
	else:
		cad.lcd.write(str(volume).rjust(4))
	
def writeBottomLine():
	global play
	showTime()
	writeVolume()
	cad.lcd.set_cursor(7,1)
	if play:
		cad.lcd.write_custom_bitmap(1)
	else:
		cad.lcd.write_custom_bitmap(2)
	cad.lcd.set_cursor(0,0)
	 
listener = pifacecad.SwitchEventListener(chip=cad)
for i in range(8):
	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
listener.activate()

remote_listener = pifacecad.IREventListener(prog='myprogram')
for i in range(8):
	remote_listener.register(str(i), print_ir_code)
remote_listener.activate()


def musicMainfunc():
	global pin
	global remote
	global volume
	global play
	global mute
	
	curSong = 0
	pin = -1
	remote = -1
	
	mixer.init()
	mixer.music.set_volume(float(volume)/100)
	while True:
		if curSong == len(song):
			curSong = 0
		cad.lcd.clear()
		cad.lcd.blink_off()
		cad.lcd.cursor_off()
		mixer.music.load(song[curSong]+'.mp3')
		cad.lcd.write_custom_bitmap(0)
		cad.lcd.write(song[curSong])
		mixer.music.play()
		
		while mixer.music.get_busy() == True:
			writeBottomLine()
			
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
					volume -= 3
					if volume < 0:
						volume = 0
					mixer.music.set_volume(float(volume)/100)
					updateVolume();
					sleep(0.2)
					if not cad.switches[6].value:
						break
				pin = -1
				remote = -1
			elif pin == 7 or remote == 7:	# volume up
				while True:
					volume += 3
					if volume > 100:
						volume = 100
					mixer.music.set_volume(float(volume)/100)
					updateVolume();
					sleep(0.2)
					if not cad.switches[7].value:
						break
				pin = -1
				remote = -1
			elif pin == 5 or remote == 5:	# mute
				if mute:
					mixer.music.set_volume(float(volume)/100)
					mute = False
				else:
					mixer.music.set_volume(0)
					mute = True
				pin = -1
				remote = -1
			elif pin == 4 or remote == 4:	# quit
				pin = -1
				remote = -1
				mixer.quit()
				return
		curSong+=1
	
musicMainfunc()
