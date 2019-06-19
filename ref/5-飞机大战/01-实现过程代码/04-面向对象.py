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

#2/定义键盘检测函数
def key_pressd(hero_temp):

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
                hero_temp.move_left()
            # 如果按下了d 或者右箭头
            elif event.key in (K_d, K_RIGHT):
                hero_temp.move_right()
            # 如果按下了 空格键
            elif event.key == K_SPACE:
                print('发射子弹')



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
