import math
import pygame
from particles import Explosion

WIDTH, HEIGHT = 640, 384

pygame.mixer.init()
grenade_blast_fx = pygame.mixer.Sound('Sounds/grenade blast.wav')


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, color, type_, win):
		pygame.sprite.Sprite.__init__(self)

		self.x = x
		self.y = y
		self.direction = direction
		self.color = color
		self.type = type_
		self.win = win

		self.speed = 10
		self.radius = 4
		
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)
		self.rect.center = (x, y)

	def update(self, screen_scroll, world):
		self.x += (self.direction * self.speed) + screen_scroll

		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > WIDTH:
			self.kill()

		for tile in world.ground_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, win):
		super(Grenade, self).__init__()
		self.direction = direction
		self.win = win

		self.speed = 8
		self.vel_y = -12
		self.timer = 15
		self.scale = 0.6

		if self.direction == 0:
			self.direction = 1
		
		img = pygame.image.load(f'Assets/grenade.png').convert_alpha()
		self.image = pygame.transform.scale(img, (int(img.get_width()*self.scale), int(img.get_height()*self.scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self, screen_scroll, p, enemy_group, explosion_group, world):
		self.vel_y += 1 #gravity
		dx = self.direction * self.speed
		dy = self.vel_y

		for tile in world.ground_list:
			#check collision with walls
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				self.direction *= -1
				dx = self.direction * self.speed
			#check collision in the y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				self.speed = 0
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				elif self.vel_y >= 0:
					self.vel_y = 0
					dy = tile[1].top - self.rect.bottom

		for tile in world.rock_list:
			#check collision with walls
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				self.direction *= -1
				dx = self.direction * self.speed
			#check collision in the y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				self.speed = 0
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				elif self.vel_y >= 0:
					self.vel_y = 0
					dy = tile[1].top - self.rect.bottom


		if self.speed == 0:
			self.timer -= 1
			if self.timer <= 0:
				grenade_blast_fx.play()
				explosion = Explosion(self.rect.x, self.rect.y, self.win)
				explosion_group.add(explosion)

				p_distance = math.sqrt((p.rect.centerx - self.rect.x) ** 2 + (p.rect.centery - self.rect.y) ** 2 )
				if p_distance <= 100:
					if p_distance > 80:
						p.health -= 20
					elif p_distance > 40:
						p.health -= 50
					elif p_distance >= 0:
						p.health -= 80
					p.hit = True

				for e in enemy_group:
					e_distance = math.sqrt((e.rect.centerx - self.rect.x) ** 2 + (e.rect.centery - self.rect.y) ** 2)
					if e_distance < 80:
						e.health -= 100

				self.kill()
 
		self.rect.x += dx + screen_scroll 
		self.rect.y += dy
	def sound_nade(n):
		grenade_blast_fx.set_volume(n)