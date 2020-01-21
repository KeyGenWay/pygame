import pygame
import random
import keyboard

WIDTH = 400
HEIGHT = 400

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HIGH_SPEED = 4
LOW_SPEED = 2
NO_SPEED = 0

FPS = 240

class Player(pygame.sprite.Sprite):
    angle = 0

    def updateAngle(self, x):
        self.angle += x;
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_surface = pygame.Surface((50, 50))
        self.image = self.original_surface
        self.image.fill(WHITE)
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        pygame.draw.line(self.original_surface, RED, (25,25), (25,0), 4)
        pygame.draw.circle(self.original_surface, RED, (25, 25), 25, 4)
    def update(self):

        # Aktualizacja pozycji przy kliknieciu
        if keyboard.is_pressed("down_arrow"):
            self.rect.y += 1
        if keyboard.is_pressed("up_arrow"):
            self.moveForward()
        if keyboard.is_pressed("left_arrow"):
            self.image = pygame.transform.rotate(self.original_surface, self.angle)
            self.updateAngle(4)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        if keyboard.is_pressed("right_arrow"):
            self.image = pygame.transform.rotate(self.original_surface, self.angle)
            self.updateAngle(-4)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


        # Przenikanie ze sciany na sciane
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT

        #Kolizja z kamieniem (prost wersja na punktach srodkowych)
        if self.rect.collidepoint(rock.rect.midtop):
            self.rect.bottom = rock.rect.top
        if self.rect.collidepoint(rock.rect.midleft):
            self.rect.right = rock.rect.left
        if self.rect.collidepoint(rock.rect.midright):
            self.rect.left = rock.rect.right
        if self.rect.collidepoint(rock.rect.midbottom):
            self.rect.top = rock.rect.bottom
    def moveForward(self):
        # Zmiana pozycji przy poruszaniu sie w kierunku  w  konkretnych cwiartkach
        if 0 < self.angle < 45:
            self.rect.x -= LOW_SPEED
            self.rect.y -= HIGH_SPEED
        if 45 < self.angle < 90:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= LOW_SPEED
        if 90 < self.angle < 135:
            self.rect.x -= HIGH_SPEED
            self.rect.y += LOW_SPEED
        if 135 < self.angle < 180:
            self.rect.x -= LOW_SPEED
            self.rect.y += HIGH_SPEED
        if 180 < self.angle < 225:
            self.rect.x += LOW_SPEED
            self.rect.y += HIGH_SPEED
        if 225 < self.angle < 270:
            self.rect.x += HIGH_SPEED
            self.rect.y += LOW_SPEED
        if 270 < self.angle < 315:
            self.rect.x += HIGH_SPEED
            self.rect.y -= LOW_SPEED
        if 315 < self.angle < 460:
            self.rect.x += LOW_SPEED
            self.rect.y -= HIGH_SPEED

        ## Wartosci progowe w cwiartkach
        if self.angle == 0:
            self.rect.x -= NO_SPEED
            self.rect.y -= HIGH_SPEED
        if self.angle == 45:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= HIGH_SPEED
        if self.angle == 90:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= NO_SPEED
        if self.angle == 135:
            self.rect.x -= HIGH_SPEED
            self.rect.y += HIGH_SPEED
        if self.angle == 180:
            self.rect.x += NO_SPEED
            self.rect.y += HIGH_SPEED
        if self.angle == 225:
            self.rect.x += HIGH_SPEED
            self.rect.y += HIGH_SPEED
        if self.angle == 270:
            self.rect.x += HIGH_SPEED
            self.rect.y -= 0
        if self.angle == 315:
            self.rect.x += HIGH_SPEED
            self.rect.y -= HIGH_SPEED


class RockGenerator():
    def generateRock(self):
        return Rock()

class Rock(pygame.sprite.Sprite):
    __dx = 0
    __dy = 0
    __cycle = 60*FPS
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((random.randint(30, 60), random.randint(30, 60)))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(2, WIDTH), random.randint(2, HEIGHT))
    def update(self):
        self.rect.x += self.__dx
        self.rect.y += self.__dy
        if self.__cycle == 0:
            self.__dx = random.randint(-2, 2)
            self.__dy = random.randint(-2, 2)
            self.__cycle = 60*FPS
        self.__cycle -= FPS

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TheGame")
clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
player = Player()
generator = RockGenerator()
rock = Rock()
allSprites.add(player)
allSprites.add(rock)
#for i in range(10):
#   allSprites.add(generator.generateRock())
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    allSprites.update()
    screen.fill(WHITE)
    allSprites.draw(screen)
    pygame.display.flip()




pygame.quit()