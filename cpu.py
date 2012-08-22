##############################
#CPU Monitor
#author Jacob Mason
#
#requirements:
#python 2.x
#pygame
#sysstat installed
#tkinter
#############################

import pygame
from time import sleep
from sys import exit
from color import *
from Tkinter import *
import os
pygame.init()

class CPU():
	'''Cpu monitor class'''
	def __init__(self):
		self.size=[250,300]
		self.screen=pygame.display.set_mode(self.size)
		pygame.display.set_caption("Cpu Monitor")
		self.temp = 0
		self.coreInc = 0 #adds window area if needed
		self.delay = 1
		self.tools = False
		self.bgImage = pygame.image.load("background.jpg").convert() #load background

	def write(self,text,xy,size=30,color=whitish,default=None):
		'''write text to the screen'''
		self.font = pygame.font.Font(default, size)
		self.display = self.font.render(text,True,color)
		self.screen.blit(self.display, xy)

	def output(self,text,xy,color=whitish,size=17,default=None,optionalText=''):
		'''similar to write, formats/displays output data
		   displays optionalText >text'''
		self.count(optionalText) #for padding
		self.font = pygame.font.Font(default, size)
		self.display = self.font.render(text,True,color)
		self.screen.blit(self.display, [xy[0]+15+self.padding,xy[1]+5])
		self.font = pygame.font.Font(default, 23)
		self.display2 = self.font.render(optionalText + ' >',True,blueGreen)
		self.screen.blit(self.display2, xy)
	
	def warn(self):
		'''high CPU temp warning message'''
		msg = Message(text="High CPU temp! %sC" % self.temp)
		msg.config(bg='blue', font=('times', 16, 'bold'))
		msg.pack()
		mainloop()
	
	def usage(self):
		'''calculate CPU usage for each core'''
		use = os.popen('mpstat -P ALL').readlines()[4:]
		self.cores = []
		for core in use:
			self.cores.append(100-float(core.split()[-1])) 

	def bgDisplay(self):
		'''display background'''
		self.screen.blit(self.bgImage,[0,0])

	def maxTemp(self):
		'''get critical operating temp of CPU'''
		self.critTemp = float(os.popen('sensors').readlines()[2].split()[4][1:-4])

	def cpuTemp(self):
		self.lastTemp = self.temp
		self.temp = float(os.popen('sensors').readlines()[2].split()[1][1:-3])
		self.tempList = [self.temp] + self.tempList[:-1] 
		

		#rising/falling/stable status
		higher = 0
		lower = 0
		for i in self.tempList: 
			#check last 2 temps are > or < than old ones
			if self.temp > i and self.lastTemp > i:
				higher += 1
			elif self.temp < i and self.lastTemp < i:
				lower += 1
		if higher > lower:
			self.tempStatus = 'Rising' 
			self.tempColor = red
		elif higher < lower:
			self.tempStatus = 'Falling'
			self.tempColor = blueGreen
		else: 
			self.tempStatus = 'Stable'
			self.tempColor = green
		
	def cputype(self):
		'''Get cpu model'''
		self.cpuModel = os.popen('cat /proc/cpuinfo').readlines()[4].split()[4:]
		res = ''
		for i in self.cpuModel:
			res += i + ' '
		self.cpuModel = res
	
	def tempBar(self,xy,xy2):
		'''draw temp bar'''
		#temp bar
		if self.temp <= 69:
			self.line = pygame.draw.line(self.screen,blueish,xy,xy2,15)
		elif self.temp >= 70 and self.temp <= 80:
			self.line = pygame.draw.line(self.screen,orange,xy,xy2,15)
		elif self.temp >= 81:
			self.line = pygame.draw.line(self.screen,red,xy,xy2,15)
			self.warn()

	def count(self,s):
		'''counts a string, for use in padding output'''
		self.padding = 0
		for i in s:
			self.padding += 7.5

class Button():
	def __init__(self,text,image,xy,xyBuff):
		self.text = text #button text
		self.xy = xy #button location 
		self.xyBuff = xy #defines the area of the button.
		self.image = image #image to use for the button

	def clicked(self,mouseXY):
		'''Mouseclick inside button coords (returns True or False)'''
		if mouseXY[0] >= self.xy[0] and mouseXY[1] >= self.xy[1]:
			if mouseXY[0] <= self.xy[0] + self.xyBuff[0] and mouseXY[1] <= self.xy[1] + self.xyBuff[1]:
				#mouse inside button coords
				return True
		return False
	def show(self):
		'''Draw/Display button'''
		pass
			
def main():
	monitor = CPU()
	monitor.tempList = [0]*5 #holds last 50 temps
	monitor.cputype()
	monitor.usage()
	#add area to the window if needed (more cores to display)
	newSize = [monitor.size[0],monitor.size[1]+len(monitor.cores)]
	monitor.screen=pygame.display.set_mode(newSize)

	while True:
		inc = 20 #Y coord padding
		monitor.cpuTemp()
		monitor.usage()
		monitor.screen.fill(black)
		monitor.bgDisplay()
		monitor.write('CPU Model',[15,25])
		inc += 15
		monitor.output(monitor.cpuModel,[30,25+inc-15]) #cpu model
		inc += 15

		#display core use
		monitor.write('CPU Usage',[15,25+inc])
		inc += 20
		for i in xrange(len(monitor.cores)):
			monitor.output(str(monitor.cores[i]) + '%',[30,25+inc],whitish,23,None,'Core ' + str(i))
			inc += 15
		
		#cpu temp
		inc += 15
		monitor.write('CPU Temp',[15,25+inc])
		inc += 25
		monitor.write(monitor.tempStatus,[(monitor.temp*2)/2,25+inc],17,monitor.tempColor)
		inc += 20
		monitor.tempBar([30,25+inc],[monitor.temp*2,25+inc])
		monitor.write(str(monitor.temp)+'C',[(monitor.temp*2)/2+3,20+inc],23)
		pygame.display.flip()
		
		#tool options


		#mouse coords(x,y)
		pos = pygame.mouse.get_pos()
		
		#detect/handle user events
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print pos
				
		
		sleep(monitor.delay)

class Button():
	pass

if __name__ == '__main__':
	main()

