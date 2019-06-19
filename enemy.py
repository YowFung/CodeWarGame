from bullet import *
import pygame
import random


class Enemy(object):
	"""
	敌机类
	"""

	def __init__(self, config, pos, game):
		"""
		构造方法，初始化敌机
		:param config:		游戏配置对象
		:param pos:			初始坐标位置
		:param game:		游戏对象
		"""
		self.config = config
		self.game = game

		# 战机属性
		self.exploding = False					# 是否正在爆炸
		self.alive = True						# 生存状态
		self.bullets = []						# 子弹库
		self.pos = pos 							# 坐标

		# 加载图像
		self.type = int(random.random()*len(config.IMG_ENEMIES))
		self.img = pygame.image.load(config.IMG_ENEMIES[self.type])

		# 计算图像尺寸
		self.width = self.img.get_rect()[2]
		self.height = self.img.get_rect()[3]

		# 初始化类变量
		self.times_var = {}
		self.times_var['explode'] = 0					# 爆炸计次

		# 初始化时钟变量
		self.tick = pygame.time.get_ticks()

	def fly(self):
		"""
		敌机出击
		"""
		if self.alive:
			# 前进
			self.pos[1] += 5

			if self.exploding == False:
				if self.detect_crash():
					# 发生碰撞，爆炸身亡
					self.boom()

					# 让主角受伤
					self.game.hero.bruise()
				elif self.detect_border():
					# 越界，标记已死亡
					self.alive = False
				else:
					# 发射子弹
					self.shoot()

			self.show()

	def show(self):
		"""
		显示敌机
		"""
		if self.alive and self.exploding == False:
			x = self.pos[0] - self.width/2
			y = self.pos[1] - self.height/2
			self.game.screen.blit(self.img, (x, y))

		# 如果是正在爆炸的话
		if self.exploding:
			# 显示爆炸动画
			img = pygame.image.load(self.config.IMG_BOOM_ENEMIES[self.times_var['explode']])
			x = self.pos[0] - img.get_rect()[2]/2
			y = self.pos[1] - img.get_rect()[3]/2
			self.game.screen.blit(img, (x, y))

			self.times_var['explode'] += 1
			if self.times_var['explode'] >= len(self.config.IMG_BOOM_ENEMIES):
				self.exploding = False

				# 爆炸结束，标记已死亡
				self.alive = False

	def shoot(self):
		"""
		敌机发射子弹
		"""
		# 每隔两秒发射一颗子弹
		tick = pygame.time.get_ticks()
		if self.alive and tick - self.tick >= 2000:
			self.tick = tick

			# 创建子弹对象并初始化坐标
			# 子弹发射者为敌机，飞行方向为向下
			bullet_pos = [self.pos[0], self.pos[1] + self.height/2]
			bullet_type = self.type
			new_bullet = Bullet(self.config, self.game, bullet_pos, LAUNCHER_ENEMY, DIRECTION_DOWNWARD, bullet_type=bullet_type)

			# 将子弹添加到列表
			self.game.bullets.append(new_bullet)
			self.bullets.append(new_bullet)

	def detect_border(self):
		"""
		边界检测
		"""
		return self.pos[1] - self.height/2 > self.config.SCREEN_HEIGHT

	def detect_crash(self):
		"""
		碰撞检测
		"""
		x_min = self.game.hero.pos[0] - self.game.hero.width/2 - self.width/2
		x_max = self.game.hero.pos[0] + self.game.hero.width/2 + self.width/2
		crash_x = x_min <= self.pos[0] <= x_max
		crash_y = self.pos[1] + self.height/2 >= self.game.hero.pos[1] - self.game.hero.height/2
		return crash_x and crash_y

	def boom(self):
		"""
		敌机毁灭
		"""
		# 标记正在爆炸
		self.exploding = True
		self.times_var['explode'] = 0

		# 清空子弹库
		for bullet in self.bullets:
			bullet.alive = False
			self.bullets.remove(bullet)

		# 播放爆炸音效
		sound = pygame.mixer.Sound(self.config.SOUND_ENEMY_BOOM)
		sound.play()
