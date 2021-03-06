import pygame

from mundo import World
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((900, 600))

# Fontes e cores
font = "Retro.ttf"
white = (255, 255, 255)
blue = (0, 0, 255)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, False, textColor)
    return newText


class Player:
    def __init__(self, x, y, daltonism):
        self.imagesRight = []
        self.imagesLeft = []
        self.imagesDead = []
        for num in range(1, 6):
            imgRight = pygame.image.load(f'assets/img/{daltonism}/walk{num}.png')
            imgRight = pygame.transform.scale(imgRight, (40, 80))
            imgLeft = pygame.transform.flip(imgRight, True, False)
            self.imagesRight.append(imgRight)
            self.imagesLeft.append(imgLeft)
        for num in range(1, 7):
            imgDead = pygame.image.load(f'assets/img/{daltonism}/death{num}.png')
            imgDead = pygame.transform.scale(imgDead, (40, 80))
            self.imagesDead.append(imgDead)
        self.image = self.imagesRight[3]
        self.rect = self.image.get_rect()
        self.index = 0
        self.walkCounter = 0
        self.standCounter = 0
        self.lastUpdate = 0
        self.currentFrame = 0
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.walked = False
        self.direction = 0
        self.inAir = True

    def update(self, gameOver, world, enemy_group, lava_group, exit_group, keyCollected, vanity_coin, vanity_key):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if gameOver == 0:
            # Captura das teclas do usuário
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.inAir:
                self.vel_y = -15
                self.jumped = True
                self.standCounter = 0
                pygame.mixer.music.load('assets/sounds/jump.wav')
                pygame.mixer.music.play(0)
            if not key[pygame.K_SPACE]:
                self.jumped = False
                self.standCounter = 0
            if key[pygame.K_LEFT]:
                dx -= 5
                self.walked = True
                self.walkCounter += 1
                self.direction = -1
                self.standCounter = 0
            if key[pygame.K_RIGHT]:
                dx += 5
                self.walked = True
                self.walkCounter += 1
                self.direction = 1
                self.standCounter = 0
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.walkCounter = 0
                self.index = 0
                self.standCounter += 1
                if self.direction == 1:
                    self.image = self.imagesRight[3]
                if self.direction == -1:
                    self.image = self.imagesLeft[3]

            # Animação do personagem
            # Andando
            if self.walkCounter > walk_cooldown:
                self.walkCounter = 0
                self.index += 1
                if self.index >= len(self.imagesRight):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.imagesRight[self.index]
                if self.direction == -1:
                    self.image = self.imagesLeft[self.index]

            # Gravidade
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Checagem de colisão com os blocos
            self.inAir = True
            for tile in world.tile_list:
                # Checagem de colisão no eixo x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Checagem de colisão no eixo y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Pulando
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                        # Caindo
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.inAir = False

            # Checagem de colisão com os inimigos
            if pygame.sprite.spritecollide(self, enemy_group, False):
                pygame.mixer.music.load('assets/sounds/death-enemy.mp3')
                pygame.mixer.music.play(0)
                gameOver = -1
            # Checagem de colisão com a lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                pygame.mixer.music.load('assets/sounds/death-lava.wav')
                pygame.mixer.music.play(0)
                gameOver = -1

            # Checagem de colisão com a porta de saída
            if keyCollected == 1:
                if pygame.sprite.spritecollide(self, exit_group, False):
                    pygame.mixer.music.load('assets/sounds/win.wav')
                    pygame.mixer.music.play(0)
                    vanity_coin.remove(vanity_coin)
                    vanity_key.remove(vanity_key)
                    gameOver = 1

            # Atualização das coordenadas do jogador
            self.rect.x += dx
            self.rect.y += dy

        elif gameOver == -1:
            lose_text = text_format('VOCE PERDEU!', font, 75, white)
            screen.blit(lose_text, (600/2, -10))
            vanity_coin.remove(vanity_coin)
            vanity_key.remove(vanity_key)
            self.standCounter += 1
            self.image = self.imagesDead[self.index]
            if self.standCounter > 7:
                if self.index >= (len(self.imagesDead) - 1):
                    return gameOver
                else:
                    self.index += 1
                self.standCounter = 0

        # Desenhar o jogador na tela
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return gameOver
