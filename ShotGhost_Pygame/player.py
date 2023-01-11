import pygame
import os
from pygame.draw import rect
from pygame.locals import *

WIDTH, HEIGHT = 640, 384

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y

		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.scale = 1.5
		self.flip = False

		animation_types = ['Idle', 'Walk', 'Jump', 'Hit', 'Death', 'Attack']
		for animation in animation_types:
			temp_list = []

			num_of_frames = len(os.listdir(f'Assets/Player/{animation}'))

			for i in range(num_of_frames):
				img = pygame.image.load(f'Assets/Player/{animation}/{i}.png')
				img = pygame.transform.scale(img, (int(img.get_width()*self.scale), int(img.get_height()*self.scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect(center=(x, y))
		self.width = self.image.get_width()
		self.height = self.image.get_height()

		self.idle_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0

		self.jump_height = 16.5
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False

		self.grenades = 5
		self.health = 100

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			#check for collision in x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					self.jump = False
					self.vel = self.jump_height
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
			

		# Checking collision with rocks & stones
		for tile in world.rock_list:
			#check for collision in x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					self.jump = False
					self.vel = self.jump_height
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.animation_list[4]):
					self.alive = False
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.animation_list[5]):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.animation_list[3]):
						self.hit_index = 0
						self.hit = False			
				if self.direction == -1 or self.direction == 1 or self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.animation_list[0])
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.animation_list[4][self.death_index]
			elif self.attack:
				self.image = self.animation_list[5][self.attack_index]
			elif self.hit:
				self.image = self.animation_list[3][self.hit_index]
			else:
				self.image = self.animation_list[0][self.idle_index]


	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.flip = True
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.flip = False

		if self.jump:
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity

			if self.vel < -16.5:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

		
	def draw(self, win):
		win.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
