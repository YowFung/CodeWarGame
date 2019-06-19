import random
import pygame
from pygame.locals import *
pygame.init() #对游戏进行初始化
#1/定义我方飞机类
class HeroPlane(object):
    def __init__(self,screen):


        # 添加我军飞机
        # 第一步;加载我军飞机的图片
        self.imageLoadname = './feiji/hero.png' #图片路径
        self.image = pygame.image.load(self.imageLoadname)
        # 第二步：设定一个初始位置
        self.x = 150
        self.y = 450
        #设置要显示的窗口
        self.screen = screen

        #设置子弹列表
        self.bulletlist = []  #子弹有很多，我们设置一个列表进行保存

    def move_left(self):
        #向左移动
        print('往左移动')
        self.x -= 10
        if self.x <= 0:
            self.x = 310

    def move_right(self):
        print('往右移动')
        self.x += 10
        if self.x > 310:
            self.x = 0
    def display(self):
        #显示飞机
        self.screen.blit(self.image,(self.x,self.y))
        #显示子弹
        #：将子弹夹中的子弹显示出来

        # 设置一个列表来存放已经越界的子弹并删除
        is_JudgeBullet = []
        for i in self.bulletlist:
            if i.judge() == True:
                is_JudgeBullet.append(i)

        #删除弹夹self.bulletlist里面的子弹
        for i in is_JudgeBullet:
            self.bulletlist.remove(i)

        for b in self.bulletlist:
            b.display() #显示子弹列表中子弹
            b.move()

    def shotBullet(self):
        #给我军分级添加一个发射子弹的方法
        newBullet = Bullet(self.x,self.y,self.screen)
        #子弹列表中添加刚刚生成的子弹
        self.bulletlist.append(newBullet)

#2/定义键盘检测函数
def key_pressd(hero):

    # 键盘检测，需要导入pygame.locals
    for event in pygame.event.get():
        # 判断是否按了退出按键
        if event.type == pygame.QUIT:
            # pygame.quit()
            exit()
        # 如果类型是按下某个按键
        elif event.type == pygame.KEYDOWN:
            # 如果按下了a 或者左箭头

            if event.key in (K_a, K_LEFT):
                hero.move_left()
            # 如果按下了d 或者右箭头
            elif event.key in (K_d, K_RIGHT):
                hero.move_right()
            # 如果按下了 空格键
            elif event.key == K_SPACE:
                print("发射子弹")
                hero.shotBullet()


#定义一个子弹类
class Bullet():
    def __init__(self,x,y,screen):
        #子弹是根据我方飞机的位置出现，所以需要传入飞机所在的位置数据
        self.x = x+13
        self.y = y-20
        self.screen = screen
        #生成子弹图片
        self.image = pygame.image.load('./feiji/bullet.png')
    def move(self):
        #向上移动
        self.y-=20
    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

    def judge(self):
        #判断子弹是否越界
        # return True if self.y<0 else False
        if self.y<0:
            return True
        else:
            return False






#3/定义主函数
def main():
    # 1.创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((350, 500))
    # 2.加载一张和窗口大小一致的图片充当背景
    background = pygame.image.load('./feiji/background.png')

    # 4.添加背景音乐
    pygame.mixer.init()
    #1、加载音乐
    pygame.mixer.music.load('./feiji/background.mp3')
    #2、设置音量
    pygame.mixer.music.set_volume(0.3)
    #3、播放并循环
    pygame.mixer.music.play(-1) #-1就表示无限循环
    clock = pygame.time.Clock()  # 生成一个时钟对象

    #创建一个英雄飞机对象
    hero = HeroPlane(screen)
    while True:
        pygame.display.flip()
        #把背景放到窗口中
        screen.blit(background, (0, 0))
        #显示飞机
        hero.display()
        #键盘检测，检测飞机移动
        key_pressd(hero)
        #4刷新屏幕
        pygame.display.update()
        #生成一个时钟对象
        clock.tick(50)
if __name__ == "__main__":
    main()
