#!/usr/bin/env python
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#		It's my first actual game-making attempt. I know code could be much better 
#		with classes or defs but I tried to make it short and understandable with very 
#		little knowledge of python and pygame(I'm one of them). Enjoy.

import pygame
from pygame.locals import *
from sys import exit
import random
import rospy
from sensor_msgs.msg import Joy

class game():

	def __init__(self):
		
		# ROS Subscribers
		joy1 = rospy.Subscriber("/joy", Joy, self.joy1_callback)
		self.axes = 0.

		pygame.init()

		self.screen=pygame.display.set_mode((640,480),0,32)
		pygame.display.set_caption("Pong Pong!")

		#Creating 2 bars, a ball and background.
		self.back = pygame.Surface((640,480))
		self.background = self.back.convert()
		self.background.fill((0,0,0))
		self.bar = pygame.Surface((10,50))
		self.bar1 = self.bar.convert()
		self.bar1.fill((0,0,255))
		self.bar2 = self.bar.convert()
		self.bar2.fill((255,0,0))
		self.circ_sur = pygame.Surface((15,15))
		self.circ = pygame.draw.circle(self.circ_sur,(0,255,0),(15/2,15/2),15/2)
		self.circle = self.circ_sur.convert()
		self.circle.set_colorkey((0,0,0))

		# some definitions
		self.bar1_x, self.bar2_x = 10. , 620.
		self.bar1_y, self.bar2_y = 215. , 215.
		self.circle_x, self.circle_y = 307.5, 232.5
		self.bar1_move, self.bar2_move = 0. , 0.
		self.speed_x, self.speed_y, self.speed_circ = 250., 250., 250.
		self.bar1_score, self.bar2_score = 0,0
		#clock and font objects
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("calibri",40)
		self.ai_speed = 0.

	def joy1_callback(self,msg):
		# Macbook motion joy
		self.axes = float(msg.axes[1])
		print self.axes
		# print self.axes

	def animate(self):
	
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			# if event.type == KEYDOWN:
			# 	if event.key == K_UP:
			# 		self.bar1_move = -self.self.ai_speed
			# 	elif event.key == K_DOWN:
			# 		self.bar1_move = self.ai_speed
			# elif event.type == KEYUP:
			# 	if event.key == K_UP:
			# 		self.bar1_move = 0.
			# 	elif event.key == K_DOWN:
			# 		self.bar1_move = 0.
		# print self.ai_speed
		# print type(self.ai_speed)
		self.bar1_move = -2*self.ai_speed*self.axes
		
		score1 = self.font.render(str(self.bar1_score), True,(255,255,255))
		score2 = self.font.render(str(self.bar2_score), True,(255,255,255))

		self.screen.blit(self.background,(0,0))
		frame = pygame.draw.rect(self.screen,(255,255,255),Rect((5,5),(630,470)),2)
		middle_line = pygame.draw.aaline(self.screen,(255,255,255),(330,5),(330,475))
		self.screen.blit(self.bar1,(self.bar1_x,self.bar1_y))
		self.screen.blit(self.bar2,(self.bar2_x,self.bar2_y))
		self.screen.blit(self.circle,(self.circle_x,self.circle_y))
		self.screen.blit(score1,(250.,210.))
		self.screen.blit(score2,(380.,210.))

		self.bar1_y += self.bar1_move
		
	# movement of circle
		time_passed = self.clock.tick(30)
		time_sec = time_passed / 1000.0
		
		self.circle_x += self.speed_x * time_sec
		self.circle_y += self.speed_y * time_sec
		self.ai_speed = self.speed_circ * time_sec
	#AI of the computer.
		if self.circle_x >= 305.:
			if not self.bar2_y == self.circle_y + 7.5:
				if self.bar2_y < self.circle_y + 7.5:
					self.bar2_y += self.ai_speed
				if  self.bar2_y > self.circle_y - 42.5:
					self.bar2_y -= self.ai_speed
			else:
				self.bar2_y == self.circle_y + 7.5
		
		if self.bar1_y >= 420.: self.bar1_y = 420.
		elif self.bar1_y <= 10. : self.bar1_y = 10.
		if self.bar2_y >= 420.: self.bar2_y = 420.
		elif self.bar2_y <= 10.: self.bar2_y = 10.
	#since i don't know anything about collision, ball hitting bars goes like this.
		if self.circle_x <= self.bar1_x + 10.:
			if self.circle_y >= self.bar1_y - 7.5 and self.circle_y <= self.bar1_y + 42.5:
				self.circle_x = 20.
				self.speed_x = -self.speed_x
		if self.circle_x >= self.bar2_x - 15.:
			if self.circle_y >= self.bar2_y - 7.5 and self.circle_y <= self.bar2_y + 42.5:
				self.circle_x = 605.
				self.speed_x = -self.speed_x
		if self.circle_x < 5.:
			self.bar2_score += 1
			self.circle_x, self.circle_y = 320., 232.5
			self.bar1_y,self.bar_2_y = 215., 215.
		elif self.circle_x > 620.:
			self.bar1_score += 1
			self.circle_x, self.circle_y = 307.5, 232.5
			self.bar1_y, self.bar2_y = 215., 215.
		if self.circle_y <= 10.:
			self.speed_y = -self.speed_y
			self.circle_y = 10.
		elif self.circle_y >= 457.5:
			self.speed_y = -self.speed_y
			self.circle_y = 457.5

		pygame.display.update()

##############################
#### Main Function to Run ####
##############################
if __name__ == '__main__':
	# Initialize Node
	rospy.init_node('PongGame')

	# set rate
	hz = 100.0
	rate = rospy.Rate(hz)

	# init path_manager_base object
	pong = game()

	# Loop
	while not rospy.is_shutdown():
		pong.animate()
		rate.sleep()