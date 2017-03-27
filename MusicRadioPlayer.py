from pygame import mixer # Load the required library
import pifacecad
from time import sleep
import datetime

song = ['Closer.mp3','Shape Of You.mp3','Starving.mp3','The Ocean.mp3','We Don\'t Talk Anymore.mp3']
cad = pifacecad.PiFaceCAD()
cad.lcd.backlight_on()
mixer.init()
curNum = 0

while True:
	if curNum == len(song):
		curNum = 0
	cad.lcd.clear()
	mixer.music.load(song[curNum])
	cad.lcd.write(song[curNum])
	mixer.music.play()
	
	while mixer.music.get_busy() == True:
		now = datetime.datetime.now()
		nowTime = now.strftime('%H:%M')
		cad.lcd.set_cursor(10,1)
		cad.lcd.write(nowTime)
		continue
