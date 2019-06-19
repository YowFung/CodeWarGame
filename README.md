## 粤嵌实训日记（Day1）

*悠风    2019/06/17*

------

### 任务目标

- 了解 python 编程语言
- 掌握 python 的基础语法
- 利用 pygame 库做一个 “飞机大战” 小游戏

------

### “飞机大战” 小游戏制作

#### 游戏设计：



#### 准备工作：

> **开发环境：**
>
> - python 3.7
> - pip 19.1.3
> - Sublime Text 3
> - GitBash
>
> **安装相关 python 包：**
>
> ```shell
> pip install pygame
> ```
>
> **准备素材：**
>
> - 背景图片（350x500 像素）
> - 背景音乐文件
> - 音效文件（游戏开始音效，游戏结束音效，发射音效，击中音效，被炸毁音效）



#### 程序设计：

1. 在工程目录下创建一个 `main.py`，其代码如下：

```python
import sys
import pygame
import random
from pygame.locals import *


# 界面配置
BACKGROUND_IMAGE_PATH = "./img/bg.jpg"


# 对游戏进行初始化
pygame.init()


def main():
	# 创建一个窗口，用来显示内容
	screen = pygame.display.set_mode((350, 500))

	# 加载一张和窗口大小一致的图片来充当背景
	bg = pygame.image.load(BACKGROUND_IMAGE_PATH)

	# 把背景放到窗口中
	screen.blit(bg, (0, 0))

	# 生成一个时钟对象，控制移动速度
	clock = pygame.time.Clock()

	# 键盘检测
	while True:
		for event in pygame.event.get():
			# 判断是否为退出键（ESC）
			if event.type == pygame.QUIT:
				pygame.exit()
			# 如果类型是按下某个键
			elif event.type == pygame.KEYDOWN:
				if event.key in (K_a, K_LEFT):
					print("left")
				elif event.key in (K_d, K_RIGHT):
					print("right")
				elif event.key == K_SPACE:
					print("发射子弹")

		# 刷新屏幕
		pygame.display.update()

		# 生成一个时钟对象，控制移动速度
		clock.tick(5)


# 主程序入口
if __name__ == '__main__':
	main()
```



#### 运行效果：



### Python 的算法

#### 冒泡算法：

```python
def bubble_sort(lst):
    
```



### 学习总结

​	今天实训的内容还是很简单的！明天继续努力！



移动慢的情况，



### 作业

