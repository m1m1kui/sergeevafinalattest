import pygame
from pygame import *
import random

pygame.init()

pers = pygame.image.load('ball.gif')

W_WIDTH = 820
W_HEIGHT = 660
DISPLAY = (W_WIDTH, W_HEIGHT)
BACKGROUND = ('#FFCDD2')

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = ('#EF5350')

nuan = pygame.image.load('nyan_cat.png')
new_img = pygame.transform.scale(nuan, (50, 60))

MOVE_SPEED = 7
JUMP_SPEED = 10
GRAVITY = 0.2

COLOR = (255,0,0)
screen = pygame.display.set_mode(DISPLAY)
Text_col = (255, 255, 255)
font = pygame.font.Font(None, 32)
font1 = pygame.font.Font(None, 85)
state = 'game'

enemy_i = pygame.image.load('dino.png')
new_img_e = pygame.transform.scale(enemy_i, (32, 32))

ship_i = pygame.image.load('dino.png')
new_img_ship = pygame.transform.scale(ship_i, (45, 45))


gold_i = pygame.image.load('cactus.png')
gold_count = 10
heals = 5
new_gold_i = pygame.transform.scale(gold_i, (50, 50))

sbor_i = pygame.image.load('cactus.png')
new_sbor_i = pygame.transform.scale(sbor_i, (30, 30))

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callback_=[]
        self._current_option_index = 0
    def append_options(self,option,callback):
        self._option_surfaces.append(font1.render(option,True,(255,255,255)))
        self._callback_.append(callback)
    def switch(self, direction):
        self._current_option_index = max(0,min(self._current_option_index+direction,len(self._option_surfaces)-1))
    def select(self):
        self._callback_[self._current_option_index]()
    def draw(self,surf,x,y,option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x,y+i*option_y_padding)
            if i == self._current_option_index:
                draw.rect(surf,(0,100,0),option_rect)
            surf.blit(option,option_rect)

class Game_Over:
    def __init__(self):
        screen.fill((255, 255, 255))
        text1 = font1.render('Вы проиграли!', True, ('#EF5350'))
        screen.blit(text1, (200, 170))
class Game_WIN:
    def __init__(self):
        screen.fill((255, 255, 255))
        text1 = font1.render('Вы выиграли!', True, ('#66FF99'))
        screen.blit(text1, (200, 400))



class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.image = new_img
        self.rect = Rect(x, y, 50, 60)
    def update(self, left, right, up, platform):
        if up:
            if self.onGround:
                self.yvel = -JUMP_SPEED
        if left:
            self.xvel = -MOVE_SPEED
            self.image = pygame.transform.flip(new_img,True,False)
        if right:
            self.xvel = MOVE_SPEED
            self.image = new_img
        if not(left or right):
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0,self.yvel,platform)

        self.rect.x+=self.xvel
        self.collide(self.xvel,0,platform)
    def collide(self,xvel,yvel,platform):
        for p in platform:
            if sprite.collide_rect(self,p):
                if xvel>0:
                    self.rect.right = p.rect.left
                if xvel <0:
                    self.rect.left = p.rect.right
                if yvel >0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel <0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = new_img_e
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100,W_WIDTH-130)
        self.rect.y = random.randint(100,W_HEIGHT - 130)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = new_img_ship
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, W_WIDTH - 130)
        self.rect.y = random.randint(100, W_HEIGHT - 130)

class Gold(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = new_gold_i
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, W_WIDTH - 180)
        self.rect.y = random.randint(10, W_HEIGHT - 180)

class Sborr(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = new_sbor_i
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(10, W_WIDTH - 180)
        self.rect.y = random.randint(10, W_HEIGHT - 180)

enemy = pygame.sprite.Group()
ship = pygame.sprite.Group()
gold1 = pygame.sprite.Group()
sbor1 = pygame.sprite.Group()
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x,y,PLATFORM_WIDTH,PLATFORM_HEIGHT)
def draw_timer(screen, time_left):
    text = font.render("осталось времени: " + str(time_left), True, (255, 255, 255))
    screen.blit(text, (250, 250))
def main():
    global  gold_count
    hero = Player(55,55)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platform = []
    entities.add(hero)
    level = [
        '                          '
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '                          ',
        '    ----------            ',
        '                          ',
        '                          ',
        '                          ',
        '                    ----  ',
        '                          ',
        '                          ',
        '----- ----------  --------']
    timer = pygame.time.Clock()
    x=y=0
    for row in level:
        for col in row:
            if col == '-':
                pf = Platform(x,y)
                entities.add(pf)
                platform.append(pf)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    for i in range(5):
        enemy1 = Enemy()
        enemy.add(enemy1)
        entities.add(enemy1)

    for i in range(3):
        ship1 = Ship()
        ship.add(ship1)
        entities.add(ship1)

    for i in range(15):
        gold = Gold()
        entities.add(gold)
        gold1.add(gold)


    pygame.display.set_caption('собери')
    bg = Surface((W_WIDTH,W_HEIGHT))
    bg.fill(Color(BACKGROUND))

    time1 = 60
    pygame.time.set_timer(USEREVENT + 1, 1000)
    while 1:

        global state, heals
        if state == 'game':
            pass
        timer.tick(60)
        screen.blit(bg, (0, 0))
        hero.update(left,right,up,platform)
        entities.draw(screen)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            collected_gold = pygame.sprite.spritecollide(hero, gold1, True)
            if len(collected_gold)>0:
                gold_count -= len(collected_gold)
                if gold_count == 0:
                    state = 'win'


            collected_enemy = pygame.sprite.spritecollide(hero, enemy,True)
            if len(collected_enemy)>0:
                for i in range(5):
                    sbor = Sborr()
                    entities.add(sbor)
                    sbor1.add(sbor)


            collected_ship = pygame.sprite.spritecollide(hero, ship, True)
            if len(collected_ship)>0:
                collected_sbor = pygame.sprite.spritecollide(hero, sbor1, True)

            menu = Menu()
            menu.append_options('start', lambda: print('Hello World!'))
            menu.append_options('setting', lambda: print('Hello World!'))
            menu.append_options('quit', quit)

            if e.type==KEYDOWN:
                if e.key == K_m:
                    state = 'menu'
            if state == 'menu':
                if e.type == KEYDOWN:
                    if e.key == K_UP:
                        menu.switch(-1)
                    elif e.key == K_DOWN:
                        menu.switch(1)
                    elif e.key == K_RETURN:
                        menu.select()
            if state == 'game':
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == USEREVENT + 1:
                time1 -= 1

        if state =='menu':
            screen.fill((0,0,0))
            menu.draw(screen,100,100,100)
        if state == 'lose':
            Game_Over()
        if state == 'win':
            Game_WIN()


        if time1 == 0 and state!='win':
            state = 'lose'
        text = font.render(f"осталось времени:{time1}", True, ('#EF5350'))
        screen.blit(text, (30, 60))
        text = font.render(f"осталось собрать: {gold_count}  осталось жизней: {heals}  ", True, ('#EF5350'))
        screen.blit(text, (10, 20))
        pygame.display.update()

if __name__ == '__main__':
    main()