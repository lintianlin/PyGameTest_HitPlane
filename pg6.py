import pygame
from sys import exit
import random


class Plane:
    def restart(self):
        self.x = 200
        self.y = 600

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.jpg').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x -= self.image.get_width() / 2
        y -= self.image.get_height() / 2
        self.x = x
        self.y = y


class Bullet:
    def __init__(self):
        self.x = 0
        self.y = -1
        self.speed_b = 1
        self.image = pygame.image.load('bullet.jpg').convert_alpha()
        # 默认不激活
        self.active = False

    def move(self):
        # 激活状态下向上移动
        if self.active:
            self.y -= self.speed_b
        # 当飞出屏幕，就设为不激活
        if self.y < 0:
            self.active = False

    def restart(self):
        # 重置子弹位置
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        # 激活子弹
        self.active = True


class Enemy:
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()

    def move(self):
        if self.y < 800:
            self.y += self.speed
        else:
            self.restart()

    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random() + 0.1


# 碰撞检测
def checkHit(enemy, bullet):
    # 如果字的你在敌机的图片范围之内
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (
                    bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        # 重置敌机
        enemy.restart()
        # 重置子弹
        bullet.active = False
        return True
    return False


def checkCrash(enemy, plane):
    if (plane.x + 0.7 * plane.image.get_width() > enemy.x) and (
                    plane.x + 0.3 * plane.image.get_width() < enemy.x + enemy.image.get_width()) and (
                    plane.y + 0.7 * plane.image.get_height() > enemy.y) and (
                    plane.y + 0.3 * plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False


# 游戏数据定义
num_bullet = 5
num_enemy = 3
score = 0
gameover = False

pygame.init()
screen = pygame.display.set_mode((450, 700), 0, 32)
pygame.display.set_caption('打飞机游戏')
background = pygame.image.load('back.jpg').convert()
# 设置分数文字
font = pygame.font.Font(None, 32)

# 创建一个我方飞机
plane = Plane()
# 创建子弹的list
bullets = []
# 向list中添加5发子弹
for i in range(num_bullet):
    bullets.append(Bullet())
# 子弹总数
count_b = len(bullets)
# 即将激活的子弹序号
index_b = 0
# 发射子弹的间隔
interval_b = 0

# 创建敌机的list
enemies = []
for i in range(num_enemy):
    enemies.append(Enemy())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            # 重置游戏
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    screen.blit(background, (0, 0))
    if not gameover:
        # 发射间隔递减
        interval_b -= 1
        # 当间隔小于0时，激发一颗子弹
        if interval_b < 0:
            bullets[index_b].restart()
            # 重置间隔时间
            interval_b = 500
            # 子弹序号周期性递增
            index_b = (index_b + 1) % count_b

        # 判断每个子弹的状态
        for b in bullets:
            # 处于激活状态的子弹，移动位置并绘制
            if b.active:
                # 检测每一颗active的子弹是否与enemy碰撞
                for e in enemies:
                    if checkHit(e, b):
                        score += 100
                b.move()
                screen.blit(b.image, (b.x, b.y))

        # 敌机群的移动
        for e in enemies:
            # 如果撞上敌机，设gameover为True
            if checkCrash(e, plane):
                gameover = True
            e.move()
            screen.blit(e.image, (e.x, e.y))

        plane.move()
        # 把飞机画到屏幕上
        screen.blit(plane.image, (plane.x, plane.y))
        text = font.render('Score:%d' % score, 1, (0, 0, 0))
        screen.blit(text, (0, 0))
    else:
        text1 = font.render('GAME OVER', 1, (0, 0, 0))
        text = font.render('Score:%d' % score, 1, (0, 0, 0))
        screen.blit(text1, (180, 300))
        screen.blit(text, (190, 350))
    # 刷新画面
    pygame.display.update()
