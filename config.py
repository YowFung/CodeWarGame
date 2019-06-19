import pygame
from pygame.locals import *


# 游戏名称
GAME_NAME = "代码大战之高空战神"

# 坐标及尺寸配置
SCREEN_WIDTH = 360			# 窗口宽度
SCREEN_HEIGHT = 500			# 窗口高度
DEFAULT_HERO_POS = 180		# 主角默认位置

# 时钟配置
FPS = 10					# 帧速率

# 游戏规则配置
BLOOD_LARGE = 5				# 最大血量值
BLOOD_LOSS = 1				# 每次被打损失的血量
GET_SCORE = 50				# 每次打死一个敌机得多少分

#声音配置
BGM_VOLUME = 0.5			# 背景音乐音量

# 按键配置
KEY_SHOOT = [K_SPACE]		# 发射键
KEY_SELECT = [K_SPACE]		# 选中键
KEY_LEFT = [K_a, K_LEFT]	# 左移动键
KEY_RIGHT = [K_d, K_RIGHT]	# 右移动键
KEY_UP = [K_w, K_UP]		# 上光标键
KEY_DOWN = [K_s, K_DOWN]	# 下光标键

# 字体素材配置
FONT_SCORE = {				# 得分文本
	"file": "./fonts/font70.ttf",
	"size": 24,
	"color": (255, 234, 0)
}
FONT_RESULT = {				# 游戏结果文本
	"file": "./fonts/font70.ttf",
	"size": 24,
	"color": (255, 255, 255)
}
FONT_HELP = {				# 游戏按键说明
	"file": "./fonts/font70.ttf",
	"size": 18,
	"color": (255, 255, 180)
}


# 图像素材配置
IMG_BG_WAIT = "./img/bg_wait.png"
IMG_BG_RUN = "./img/bg_run.png"
IMG_TEXT_READY = ['./img/ready1.png', './img/ready2.png', './img/ready3.png']
IMG_TEXT_GO = ['./img/go1.png', './img/go2.png', './img/go3.png']
IMG_TEXT_GAME_OVER = ['./img/game_over1.png', './img/game_over2.png']
IMG_HERO = "./img/plane_hero.png"
IMG_ENEMIES = ['./img/plane1.png', './img/plane2.png', './img/plane3.png', './img/plane4.png', './img/plane5.png', './img/plane6.png']
IMG_BULLET_HERO = "./img/bullet_hero.png"
IMG_BULLET_ENEMIES = ['./img/bullet1.png', './img/bullet2.png', './img/bullet3.png', './img/bullet4.png', './img/bullet5.png', './img/bullet6.png']
IMG_BLOOD_HAS = "./img/blood_has.png"
IMG_BLOOD_LOSS = "./img/blood_loss.png"
IMG_BOOM_HERO = ['./img/boom_hero1.png', './img/boom_hero2.png', './img/boom_hero3.png', './img/boom_hero4.png', 
				'./img/boom_hero5.png', './img/boom_hero6.png', './img/boom_hero7.png', './img/boom_hero8.png', './img/boom_hero9.png']
IMG_BOOM_ENEMIES = ['./img/boom_enemies1.png', './img/boom_enemies2.png', './img/boom_enemies3.png', './img/boom_enemies4.png', 
				'./img/boom_enemies5.png', './img/boom_enemies6.png', './img/boom_enemies7.png', './img/boom_enemies8.png', './img/boom_enemies9.png']
IMG_MENU_START_DEF = "./img/menu_start_default.png"
IMG_MENU_START_SEL = "./img/menu_start_selected.png"
IMG_MENU_EXIT_DEF = "./img/menu_exit_default.png"
IMG_MENU_EXIT_SEL = "./img/menu_exit_selected.png"
IMG_MENU_AGAIN_DEF = "./img/menu_again_default.png"
IMG_MENU_AGAIN_SEL = "./img/menu_again_selected.png"

# 音乐素材配置
MUSIC_WAIT = "./sounds/bgm_wait.mp3"
MUSIC_RUN = "./sounds/bgm_run.mp3"
SOUND_SELECT = "./sounds/select.wav"
SOUND_READY_GO = "./sounds/ready_go.ogg"
SOUND_GAME_OVER = "./sounds/game_over.wav"
SOUND_HERO_SHOOT = "./sounds/shoot.wav"
SOUND_HERO_BOOM = "./sounds/boom_hero.wav"
SOUND_HERO_BRUISE = "./sounds/bruise.wav"
SOUND_ENEMY_BOOM = "./sounds/boom_enemy.wav"
