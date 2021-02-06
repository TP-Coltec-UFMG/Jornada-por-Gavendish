# Trabalho feito em pygame pelo grupo João Lucas, Arthur Feu, Gustavo Paiva e Caio Augusto

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('AVENTURA?')

# Variaveis do jogo
tile_size = 50
# Carregando as imagens
bg_img = pygame.image.load('img/bg1.jpg')

clock = pygame.time.Clock()
fps = 60

class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left = []
		self.image_standing = pygame.image.load('img/standing.png')
		self.image_standing = pygame.transform.scale(self.image_standing, (40, 80))
		self.index = 0
		self.counter = 0
		for num in range(1, 9):
			img_right = pygame.image.load(f'img/R{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.image.load(f'img/L{num}.png')
			img_left = pygame.transform.scale(img_left, (40, 80))
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 5

		# Captura das teclas do usuário
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.jumped == False:
			self.vel_y = -15
			self.jumped = True
		if key[pygame.K_SPACE] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			dx -= 5
			self.counter += 1
			self.direction = -1
		if key[pygame.K_RIGHT]:
			dx += 5
			self.counter += 1
			self.direction = 1
		if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
			self.counter = 0
			self.index = 0
			if self.direction == 1:
				self.image = self.images_right[self.index]
			if self.direction == -1:
				self.image = self.images_left[self.index]
			else:
				self.image = self.image_standing


		# Animação de caminhar
		if self.counter > walk_cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images_right):
				self.index = 0
			if self.direction == 1:
				self.image = self.images_right[self.index]
			if self.direction == -1:
				self.image = self.images_left[self.index]
		# Gravidade
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y
		# Checagem de colisão
		for tile in world.tile_list:
			# Checagem de colisão no eixo X
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			# Checagem de colisão no eixo Y
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				# Checagem se está abaixo do solo, pulando
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				# Checagem se está acima do solo, caindo
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
		# Atualização das coordenadas do jogador
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > 600:
			self.rect.bottom = 600
		# Desenhar o jogador na tela
		screen.blit(self.image, self.rect)
		# pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class World():
	def __init__(self, data):
		self.tile_list = []
		# Carregando as imagens do solo
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			# pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 5, 2, 2],
[1, 7, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 0, 4, 0, 0, 0, 0, 3, 1, 2, 3, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, 600 - 130)
world = World(world_data)

run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))

	world.draw()

	player.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()