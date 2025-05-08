#Создай собственный Шутер!

from pygame import *
from time import time as timer
from random import randint




font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'



asteroid1_img = 'asteroid.png'
asteroid2_img = 'asteroid.png'
asteroid3_img = 'asteroid.png'
asteroid4_img = 'asteroid.png'



win_width = 700
win_height = 500



score = 0
goal = 10
lost = 0 
max_lost = 3
real_time = False
num_fire = 0
life = 3


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play
fire_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
display.set_caption('strelylka')
background = transform.scale(image.load(img_back), (win_width, win_height))



class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 540:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0 
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


ship = Player(img_hero, 5, win_height - 100, 80, 100,10)

asteroids = sprite.Group()

monsters = sprite.Group()

asteroid1 = Enemy(asteroid1_img, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
asteroid2 = Enemy(asteroid2_img, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
asteroid3 = Enemy(asteroid3_img, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
asteroid4 = Enemy(asteroid4_img, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))

asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
asteroids.add(asteroid4)


for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)



run = True
FPS = 60
clock = time.Clock()
finish = False

bullets = sprite.Group()


while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True

    if not finish:

        window.blit(background, (0,0))


        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()


        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)


        text = font2.render('Счёт: ' + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))

        text2 = font2.render('Пропущенно: ' + str(lost), 1, (255,255,255))
        window.blit(text2, (10, 50))

        if real_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            
        if sprite.spritecollide(ship, monsters , False) or sprite.spritecollide(ship, asteroids , False):
            sprite.spritecollide(ship, monsters , True)
            sprite.spritecollide(ship, asteroids , True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Счёт: ' + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))

        text2 = font2.render('Пропущенно: ' + str(lost), 1, (255,255,255))
        window.blit(text2, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150,0, 0)


        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()
    time.delay(50)