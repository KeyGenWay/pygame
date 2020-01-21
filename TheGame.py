import pygame
import random
import keyboard

WIDTH = 800
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



HIGH_SPEED = 4
#MID_SPEED = 3 Aktualnie nie wykorzystywane, moze zostac uzyte aby uplynnic poruszanie sie gracza
LOW_SPEED = 2
NO_SPEED = 0

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
        pygame.draw.circle(self.original_surface, RED, (25, 25), 30, 4)
    def update(self):

        # Aktualizacja pozycji przy kliknieciu
        if keyboard.is_pressed("down_arrow"):
            self.move(True)
        if keyboard.is_pressed("up_arrow"):
            self.move(False)
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
        moveToOtherSide(self)

    def move(self, backward):
        direction = self.angle;
        if backward:
            direction = direction - 180
            if direction < 0:
                direction = 360 + direction
        # Zmiana pozycji przy poruszaniu sie w kierunku  w  konkretnych cwiartkach
        if 0 < direction < 45:
            self.rect.x -= LOW_SPEED
            self.rect.y -= HIGH_SPEED
        if 45 < direction < 90:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= LOW_SPEED
        if 90 < direction < 135:
            self.rect.x -= HIGH_SPEED
            self.rect.y += LOW_SPEED
        if 135 < direction < 180:
            self.rect.x -= LOW_SPEED
            self.rect.y += HIGH_SPEED
        if 180 < direction < 225:
            self.rect.x += LOW_SPEED
            self.rect.y += HIGH_SPEED
        if 225 < direction < 270:
            self.rect.x += HIGH_SPEED
            self.rect.y += LOW_SPEED
        if 270 < direction < 315:
            self.rect.x += HIGH_SPEED
            self.rect.y -= LOW_SPEED
        if 315 < direction < 460:
            self.rect.x += LOW_SPEED
            self.rect.y -= HIGH_SPEED

        ## Wartosci progowe w cwiartkach
        if direction == 0:
            self.rect.x -= NO_SPEED
            self.rect.y -= HIGH_SPEED
        if direction == 45:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= HIGH_SPEED
        if direction == 90:
            self.rect.x -= HIGH_SPEED
            self.rect.y -= NO_SPEED
        if direction == 135:
            self.rect.x -= HIGH_SPEED
            self.rect.y += HIGH_SPEED
        if direction == 180:
            self.rect.x += NO_SPEED
            self.rect.y += HIGH_SPEED
        if direction == 225:
            self.rect.x += HIGH_SPEED
            self.rect.y += HIGH_SPEED
        if direction == 270:
            self.rect.x += HIGH_SPEED
            self.rect.y -= 0
        if direction == 315:
            self.rect.x += HIGH_SPEED
            self.rect.y -= HIGH_SPEED


class RockGenerator():
    def generateRock(self):
        return Rock()

class Rock(pygame.sprite.Sprite):
    __dx = 0
    __dy = 0
    __cycle = 60*FPS
    detectRange = 200
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        self.rect.center = (random.randint(1, WIDTH), random.randint(1, HEIGHT))
        pygame.draw.circle(self.image, GREEN, (25,25), 15, 15)
    def update(self):
        #self.rect.x += self.__dx
        #self.rect.y += self.__dy
        #if self.__cycle == 0:
        #    self.__dx = random.randint(-2, 2)
        #    self.__dy = random.randint(-2, 2)
        #    self.__cycle = 60*FPS
        #self.__cycle -= FPS
        self.collideWithPlayer()
        self.detectAndRunAwayFromPlayer()
        collideWithBorder(self)
        self.collideWithSecondRock()
    def collideWithPlayer(self):
        #Kolizja z graczem (prost wersja na punktach srodkowych)
        if self.rect.collidepoint(player.rect.midtop):
            self.rect.y -= HIGH_SPEED
        if self.rect.collidepoint(player.rect.midbottom):
            self.rect.y += HIGH_SPEED
        if self.rect.collidepoint(player.rect.midleft):
            self.rect.x -= HIGH_SPEED
        if self.rect.collidepoint(player.rect.midright):
            self.rect.x += HIGH_SPEED
        #Kolizja na punktach katowych
        if self.rect.collidepoint(player.rect.topleft):
            self.rect.y -= HIGH_SPEED
            self.rect.x -= HIGH_SPEED
        if self.rect.collidepoint(player.rect.topright):
            self.rect.y -= HIGH_SPEED
            self.rect.x += HIGH_SPEED
        if self.rect.collidepoint(player.rect.bottomleft):
            self.rect.y += HIGH_SPEED
            self.rect.x -= HIGH_SPEED
        if self.rect.collidepoint(player.rect.bottomright):
            self.rect.y += HIGH_SPEED
            self.rect.x += HIGH_SPEED
    def collideWithSecondRock(self):
         collidedSprite = self.rect.collidedict(allSprites.spritedict)
         print("Collision")
         print(collidedSprite[0].rect.center)
    def detectAndGoAfterPlayer(self):
        # Ponizszy kod zamiast uciekac goni gracza
        if abs(self.rect.center[0] - player.rect.center[0]) < self.detectRange and abs(self.rect.center[1] - player.rect.center[1]) < self.detectRange:
            if self.rect.x > player.rect.x:
                if self.rect.y > player.rect.y:
                    #print("He is left above!")
                    self.rect.y -= HIGH_SPEED
                    self.rect.x -= HIGH_SPEED
                else:
                    #print("He is left below!")
                    self.rect.y += HIGH_SPEED
                    self.rect.x -= HIGH_SPEED
            else:
                if self.rect.y > player.rect.y:
                    #print("He is right above!")
                    self.rect.y -= HIGH_SPEED
                    self.rect.x += HIGH_SPEED
                else:
                    #print("He is right below!")
                    self.rect.y += HIGH_SPEED
                    self.rect.x += HIGH_SPEED

    def detectAndRunAwayFromPlayer(self):
        # Uciekanie przed graczem
        if abs(self.rect.center[0] - player.rect.center[0]) < self.detectRange and abs(
                self.rect.center[1] - player.rect.center[1]) < self.detectRange:
            if self.rect.x > player.rect.x:
                if self.rect.y > player.rect.y:
                    #print("He is left above!")
                    self.rect.y += LOW_SPEED
                    self.rect.x += LOW_SPEED
                else:
                    #print("He is left below!")
                    self.rect.y -= LOW_SPEED
                    self.rect.x += LOW_SPEED
            else:
                if self.rect.y > player.rect.y:
                    #print("He is right above!")
                    self.rect.y += LOW_SPEED
                    self.rect.x -= LOW_SPEED
                else:
                    #print("He is right below!")
                    self.rect.y -= LOW_SPEED
                    self.rect.x -= LOW_SPEED




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
for i in range(10):
   allSprites.add(generator.generateRock())
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