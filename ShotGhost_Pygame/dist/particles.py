import pygame
import random


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Explosion, self).__init__()
		self.x = x
		self.y = y
		self.win = win
		self.scale = 0.6

		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f'Assets/Explosion/exp{num}.png').convert_alpha()
			img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
			self.images.append(img)

		self.frame_index = 0
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0
			
	def update (self, screen_scroll):
		#scroll
		self.rect.x += screen_scroll

		EXPLOSION_SPEED = 5
		self.counter += 1

		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			if self.frame_index >= len(self.images):
				self.kill()
			else:
				self.image = self.images[self.frame_index]

		