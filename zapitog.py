import pygame
import pygame as pg
from pygame import *
import random
from config import *

pygame.init()

nuan = pygame.image.load('nyan_cat.png')
new_img = pygame.transform.scale(nuan, (70, 60))
screen = pygame.display.set_mode(DISPLAY)
font = pygame.font.Font(None, 32)
font1 = pygame.font.Font(None, 85)
enemy_i = pygame.image.load('dino.png')
new_img_e = pygame.transform.scale(enemy_i, (32, 32))
ship_i = pygame.image.load('dino.png')
new_img_ship = pygame.transform.scale(ship_i, (0.5, 0.5))
gold_i = pygame.image.load('cactus.png')
new_gold_i = pygame.transform.scale(gold_i, (50, 50))
pg.mixer.music.load('Nyan Cat - Nyan Cat Theme.mp3')
pg.mixer.music.play()
PARTICLE_EVENT = pygame.USEREVENT
pygame.time.set_timer(PARTICLE_EVENT,80)

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callback_=[]
        self._current_option_index = 0

    def append_options(self,option,callback):
        self._option_surfaces.append(font1.render(option,True,(0,255,255)))
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
                draw.rect(surf,(0,200,0),option_rect)
            surf.blit(option,option_rect)

class Game_Over:
    def __init__(self):
        screen.fill((123, 103, 255))
        text1 = font1.render('поражение!', True, (255, 210, 49))
        screen.blit(text1, (280, 250))
class Game_WIN:
    def __init__(self):
        screen.fill((123, 103, 255))
        text1 = font1.render('победа!', True, (255, 210, 49))
        screen.blit(text1, (280, 250))



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


enemy = pygame.sprite.Group()
ship = pygame.sprite.Group()
gold1 = pygame.sprite.Group()
class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH,PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x,y,PLATFORM_WIDTH,PLATFORM_HEIGHT)
def draw_timer(screen, time_left):
    text = font.render("осталось времени: " + str(time_left), True, (255, 255, 255))
    screen.blit(text, (250, 250))
class Button:
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.clicked = False

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


def menu_pauzy(running, menu_state):


    resume_img = pygame.image.load('buttons/button_resume.jpg')
    options_img = pygame.image.load('buttons/button_options.jpg')
    quit_img = pygame.image.load('buttons/button_quit.jpg')

    resume_button = Button(300, 125, resume_img)
    options_button = Button(300, 250, options_img)
    quit_button = Button(300, 375, quit_img)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if menu_state == "main":
                if resume_button.draw(screen):
                    return
                elif options_button.draw(screen):
                    print('правила: собрать 10 печенек за 20 секунд')

                elif quit_button.draw(screen):
                    pygame.mixer.music.pause()
            elif menu_state == "options":
                if back_button.draw(screen):
                    menu_state = "main"
            pygame.display.update()

def main():
    global gold_count, heals, state
    running = True
    game_pause = False
    menu_state = 'main'
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
    enemies = pygame.sprite.Group()
    for i in range(5):
        enemy = Enemy()
        enemies.add(enemy)
        entities.add(enemy)

    for i in range(1):
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

    time1 = 20
    pygame.time.set_timer(USEREVENT + 1, 1000)

    PARTICLE_EVENT = pygame.USEREVENT
    pygame.time.set_timer(PARTICLE_EVENT, 80)

    from particle_style import ParticleStyle
    particle_img_path = 'dino.png'
    particle_style = ParticleStyle()

    while running:

        global state, heals
        if state == 'game':
            pass
        timer.tick(60)
        screen.blit(bg, (0, 0))
        hero.update(left,right,up,platform)
        entities.draw(screen)

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    game_pause = True
                    menu_state = "main"
                    menu_pauzy(running, menu_state)

            collected_gold = pygame.sprite.spritecollide(hero, gold1, True)
            if len(collected_gold)>0:
                gold_count -= len(collected_gold)
                if gold_count == 0:
                    state = 'win'


            collected_enemy = pygame.sprite.spritecollide(hero, enemies, True)
            if len(collected_enemy)>0:
                particle_style.add_particles()
                for enemy in collected_enemy:
                    for i in range(5):
                        gold = Gold()
                        entities.add(gold)
                        gold1.add(gold)
                        if gold_count == 0:
                            state = 'win'

            collected_ship = pygame.sprite.spritecollide(hero, ship, True)
            if len(collected_ship)>0:
                for enemy in collected_enemy:
                    for i in range(2):
                        gold = Gold()
                        entities.add(gold)
                        gold1.add(gold)


            menu = Menu()

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
        text = font.render(f"осталось времени:{time1}", True, (255, 237, 78))
        screen.blit(text, (30, 60))
        text = font.render(f"осталось собрать: {gold_count}", True, (255, 237, 78))
        particle_style.process()
        screen.blit(text, (10, 20))
        pygame.display.update()

if __name__ == '__main__':
    main()