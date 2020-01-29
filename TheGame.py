import pygame
import random
import keyboard
import math


font_name = pygame.font.match_font('arial')
WIDTH = 1024
HEIGHT = 760

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCORE = 0

INITIAL_SIZE_NUMBER = 3
SIZE_MODIFICATOR = 10
INITIAL_SIZE = INITIAL_SIZE_NUMBER * SIZE_MODIFICATOR

HIGH_SPEED_FACTOR = 1
NORMAL_SPEED_FACTOR = 0.5
MEDIUM_SPEED_FACTOR = 0.3
LOW_SPEED_FACTOR = 0.2
NO_SPEED_FACTOR = 0

FPS = 60

# Przenikanie ze sciany na sciane
def moveToOtherSide(self):
    if self.rect.left > WIDTH:
        self.rect.right = 0
    if self.rect.right < 0:
        self.rect.left = WIDTH
    if self.rect.top > HEIGHT:
        self.rect.bottom = 0
    if self.rect.bottom < 0:
        self.rect.top = HEIGHT
def collideWithBorder(self):
    if self.rect.right > WIDTH:
        self.rect.right = WIDTH
    if self.rect.left < 0:
        self.rect.left = 0
    if self.rect.bottom > HEIGHT:
        self.rect.bottom = HEIGHT
    if self.rect.top < 0:
        self.rect.top = 0

class Player(pygame.sprite.Sprite):
    angle = 0
    angle_modificator = 4
    current_size = 0
    size_modificator = 0.1
    current_speed = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_size = INITIAL_SIZE
        self.original_surface = pygame.Surface((self.current_size, self.current_size))
        self.image = self.original_surface
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.image.fill(WHITE)
        pygame.draw.line(self.image, BLUE,
                         (self.current_size / 2, self.current_size / 2), (self.current_size / 2, 0), 4)
        pygame.draw.circle(self.image, BLUE,
                           (self.current_size / 2, self.current_size / 2), self.current_size / 2, 4)

    def eat(self):
        global SCORE
        collidedSprite = self.rect.collidedict(foodSprites.spritedict)
        if collidedSprite is not None:
            if isinstance(collidedSprite[0], Food):
                collidedSprite[0].kill()
                SCORE += 10

    def updateAngle(self, x):
        self.angle += x
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360

    def update(self):
        # Aktualizacja pozycji przy kliknieciu
        if keyboard.is_pressed("down_arrow"):
            self.move(True)
        if keyboard.is_pressed("up_arrow"):

            self.move(False)
        if keyboard.is_pressed("left_arrow"):
            self.image = pygame.transform.rotate(self.original_surface, self.angle)
            self.updateAngle(self.angle_modificator)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        if keyboard.is_pressed("right_arrow"):
            self.image = pygame.transform.rotate(self.original_surface, self.angle)
            self.updateAngle(-self.angle_modificator)
            x, y = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        self.eat()
        # Przenikanie ze sciany na sciane
        moveToOtherSide(self)

    def move(self, backward):
        direction = self.angle
        if backward:
            direction = direction - 180
            if direction < 0:
                direction = 360 + direction

        radians = math.radians(direction)
        self.rect.x -= 10 * math.sin(radians) * NORMAL_SPEED_FACTOR
        self.rect.y -= 10 * math.cos(radians) * NORMAL_SPEED_FACTOR

    def reduceSize(self):
        self.current_size -= 1
        if self.current_size == 0:
            self.kill()
    def kill(self):
        playersSprites.remove(self)

class BadPixel(pygame.sprite.Sprite):
    detectRange = 400
    cycle = 0
    angle = 0
    def __init__(self):
        CURRENT_SIZE = INITIAL_SIZE
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((CURRENT_SIZE, CURRENT_SIZE))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.center = (random.randint(1, WIDTH), random.randint(1, HEIGHT))
        pygame.draw.circle(self.image, RED, (CURRENT_SIZE / 2, CURRENT_SIZE / 2), CURRENT_SIZE / 2, CURRENT_SIZE / 2)

    def eat(self):
        collidedSprite = self.rect.collidedict(foodSprites.spritedict)
        if collidedSprite is not None:
            if isinstance(collidedSprite[0], Food):
                collidedSprite[0].kill()

    def update(self, *args):
        self.seekPlayer()
        self.eat()
        self.collideWithPlayer()
        moveToOtherSide(self)

    def seekPlayer(self):
        selfX = self.rect.center[0]
        selfY = self.rect.center[1]
        playerX = player.rect.center[0]
        playerY = player.rect.center[1]
        distanceToPlayer = math.sqrt((playerY - selfY) ** 2 + (playerX - selfX) ** 2)
        if distanceToPlayer <= self.detectRange:
            radians = math.atan2(playerY - selfY, playerX - selfX)
            self.rect.x += 10 * math.cos(radians) * MEDIUM_SPEED_FACTOR
            self.rect.y += 10 * math.sin(radians) * MEDIUM_SPEED_FACTOR
        else:
            self.seekFood()

    def seekFood(self):
        closestSprite = None
        smallestDistance = 400
        for sprite in foodSprites.sprites():
            selfX = self.rect.center[0]
            selfY = self.rect.center[1]
            spriteX = sprite.rect.center[0]
            spriteY = sprite.rect.center[1]
            distanceToFood = math.sqrt((spriteY - selfY) ** 2 + (spriteX - selfX) ** 2)
            if distanceToFood < smallestDistance:
                smallestDistance = distanceToFood
                closestSprite = sprite
        if closestSprite is not None:
            closestSpriteX = closestSprite.rect.center[0]
            closestSpriteY = closestSprite.rect.center[1]
            if smallestDistance < self.detectRange:
                radians = math.atan2(closestSpriteY - selfY, closestSpriteX - selfX)
                self.rect.x += 10 * math.cos(radians) * LOW_SPEED_FACTOR
                self.rect.y += 10 * math.sin(radians) * LOW_SPEED_FACTOR
        else:
            self.wonderAround()

    def collideWithPlayer(self):
        if self.rect.colliderect(player.rect):
            player.reduceSize()

    def wonderAround(self):
        if self.cycle % 90 == 0:
            self.angle = random.randint(0,360)
            self.cycle = 0
        radians = math.radians(self.angle)
        self.rect.x += 10 * math.cos(radians) * LOW_SPEED_FACTOR
        self.rect.y += 10 * math.sin(radians) * LOW_SPEED_FACTOR
        self.cycle += 1

class Food(pygame.sprite.Sprite):
    detectRange = 200
    current_size = 1
    def __init__ (self):
        self.current_size = INITIAL_SIZE
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.current_size, self.current_size))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.center = (random.randint(1, WIDTH), random.randint(1, HEIGHT))
        pygame.draw.circle(self.image, GREEN, (self.current_size/2, self.current_size/2), self.current_size/2, self.current_size/2)
    def update(self):
        self.collideWithFood()
        self.detectAndRunAwayFromPlayer()
        collideWithBorder(self)
    def kill(self):
        foodSprites.remove(self)


    def collideWithFood(self):
        dictWithoutSelf = foodSprites.copy()
        dictWithoutSelf.remove(self)
        dictWithoutSelf.remove(player)
        collidedSprite = self.rect.collidedict(dictWithoutSelf.spritedict)
        if collidedSprite is not None:
            selfX = self.rect.center[0]
            selfY = self.rect.center[1]
            spriteX = collidedSprite[0].rect.center[0]
            spriteY = collidedSprite[0].rect.center[1]
            distanceToSprite = math.sqrt((spriteY - selfY) ** 2 + (spriteX - selfX) ** 2)
            if distanceToSprite < self.current_size:
                radians = math.atan2(spriteY - selfY, spriteX - selfX)
                degrees = math.degrees(radians)
                degrees += 180 % 360
                radians = math.radians(degrees)
                self.rect.x += (10 * math.cos(radians))
                self.rect.y += (10 * math.sin(radians))

    def detectAndRunAwayFromPlayer(self):
        selfX = self.rect.center[0]
        selfY = self.rect.center[1]
        playerX = player.rect.center[0]
        playerY = player.rect.center[1]
        distanceToPlayer = math.sqrt((playerY - selfY)**2 + (playerX - selfX)**2)
        if distanceToPlayer < self.detectRange:
            radians = math.atan2(playerY-selfY, playerX - selfX)
            degrees = math.degrees(radians)
            degrees += 180 % 360
            radians = math.radians(degrees)
            self.rect.x += 10 * math.cos(radians) * LOW_SPEED_FACTOR
            self.rect.y += 10 * math.sin(radians) * LOW_SPEED_FACTOR


class SpriteGenerator():
    def generateFood(self):
        return Food()
    def generateBadPixel(self):
        return BadPixel()


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TheGame")
clock = pygame.time.Clock()

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

generator = SpriteGenerator()

foodSprites = pygame.sprite.Group()
badPixelsSprites = pygame.sprite.Group()
playersSprites = pygame.sprite.Group()

player = Player()
playersSprites.add(player)

for i in range(90):
   foodSprites.add(generator.generateFood())
for i in range(5):
    badPixelsSprites.add(generator.generateBadPixel())
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    foodSprites.update()
    badPixelsSprites.update()
    playersSprites.update()

    screen.fill(WHITE)
    draw_text(screen, "SCORE:", 20, WIDTH/2-50, 10)
    draw_text(screen, str(SCORE), 20, WIDTH/2, 10)


    foodSprites.draw(screen)
    badPixelsSprites.draw(screen)
    playersSprites.draw(screen)

    pygame.display.flip()
pygame.quit()