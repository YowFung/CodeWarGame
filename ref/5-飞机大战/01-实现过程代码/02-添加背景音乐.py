import random
import pygame
from pygame.locals import *
pygame.init() #对游戏进行初始化
def main():
    # 1.创建一个窗口，用来显示内容
    screen = pygame.display.set_mode((350, 500))
    # 2.加载一张和窗口大小一致的图片充当背景
    background = pygame.image.load('./feiji/background.png')
    # 3.把背景放到窗口中
    screen.blit(background, (0, 0))
    # 4.添加背景音乐
    pygame.mixer.init()
    #1、加载音乐
    pygame.mixer.music.load('./feiji/background.mp3')
    #2、设置音量
    pygame.mixer.music.set_volume(0.3)
    #3、播放并循环
    pygame.mixer.music.play(-1) #-1就表示无限循环


    clock = pygame.time.Clock()  # 生成一个时钟对象
    while True:
        #键盘检测，需要导入pygame.locals
        for event in pygame.event.get():
            #判断是否按了退出按键
            if event.type == pygame.QUIT:
                # pygame.quit()
                exit()
            #如果类型是按下某个按键
            elif event.type == pygame.KEYDOWN:
                #如果按下了a 或者左箭头
                if event.key in (K_a,K_LEFT):
                    print('往左移动')
                # 如果按下了d 或者右箭头
                elif event.key in (K_d,K_RIGHT):
                    print('往右移动')
                #如果按下了 空格键
                elif event.key == K_SPACE:
                    print('发射子弹')
        #4刷新屏幕
        pygame.display.update()
        #生成一个时钟对象
        clock.tick(5)
if __name__ == "__main__":
    main()
