from bullet import *
import pygame


# 定义常量
MOVE_DIR_LEFT = 0		# 向左移动
MOVE_DIR_RIGHT = 1		# 向右移动


class Hero(object):
	"""
	主角类
	"""

	# 定义类常量
	SOUND_TYPE_SHOOT = 0	# 射击
	SOUND_TYPE_HRUISE = 1	# 受伤
	SOUND_TYPE_BOOM = 1		# 爆炸

	def __init__(self, config, game):
		"""
		构造函数，初始化主角；类
		:param config: 		游戏配置对象
		:param game:		游戏对象
		"""
		self.config = config
		self.game = game

		# 主角属性
		self.blood = config.BLOOD_LARGE					# 主角血量
		self.alive = True								# 生存状态
		self.exploding = False							# 是否正在爆炸
		self.bullets = []								# 子弹库

		# 加载图像
		self.img = pygame.image.load(config.IMG_HERO)

		# 计算图像尺寸
		self.width = self.img.get_rect()[2]
		self.height = self.img.get_rect()[3]

		# 设置初始坐标
		x = config.DEFAULT_HERO_POS
		y = config.SCREEN_HEIGHT - self.height/2 - 8
		self.pos = [x, y]

		# 初始化类变量
		self.times_var = {}
		self.times_var['flash'] = self.config.FPS*2		# 闪烁计次
		self.times_var['explode'] = 0					# 爆炸计次

		# 初始化时钟变量
		self.tick = pygame.time.get_ticks()

	def move(self, direction):
		"""
		移动位置
		:param direction: 	移动方向（可选 MOVE_DIR_LEFT, MOVE_DIR_RIGHT）
		"""
		if self.exploding or self.alive == False:
			return

		# 向左移动
		if direction == MOVE_DIR_LEFT:
			self.pos[0] -= 10
			if self.pos[0] < 0:
				self.pos[0] = 0

		# 向右移动
		elif direction == MOVE_DIR_RIGHT:
			self.pos[0] += 10
			if self.pos[0] > self.config.SCREEN_WIDTH:
				self.pos[0] = self.config.SCREEN_WIDTH

	def shoot(self):
		"""
		发射子弹
		"""
		# 每次发弹之间的间隔最少为 0.3 秒
		tick = pygame.time.get_ticks()
		if self.alive and tick - self.tick >= 300:
			self.tick = tick

			# 创建子弹对象并初始化坐标
			# 子弹发射者为主角，飞行方向为向上
			bullet_pos = [self.pos[0], self.pos[1] - self.height/2]
			new_bullet = Bullet(self.config, self.game, bullet_pos, LAUNCHER_HERO, DIRECTION_UPWARD)

			# 将子弹添加到列表
			self.game.bullets.append(new_bullet)
			self.bullets.append(new_bullet)

			# 播放发射子弹的音效
			self._play_sound(self.SOUND_TYPE_SHOOT)

	def bruise(self):
		"""
		受伤减血
		"""
		if self.exploding == False and self.alive:
			# 减血
			self.blood -= self.config.BLOOD_LOSS

			# 判断是否已死亡
			if self.blood <= 0:
				self.times_var['boom'] = 0
				self.exploding = True
				self.boom()
			else:
				# 播放被攻击的音效
				self._play_sound(self.SOUND_TYPE_HRUISE)

				# 复位闪烁计次变量
				self.times_var['flash'] = 0

	def boom(self):
		"""
		被毁灭
		"""
		# 标记正在爆炸
		self.blood = 0
		self.exploding = True
		self.times_var['explode'] = 0

		# 清空子弹库
		for bullet in self.bullets:
			bullet.alive = False
			self.bullets.remove(bullet)

		# 播放爆炸的音效
		self._play_sound(self.SOUND_TYPE_BOOM)

	def show(self):
		"""
		显示主角
		"""
		if self.alive and self.exploding == False:
			x = self.pos[0] - self.width/2
			y = self.pos[1] - self.height/2

			if self.times_var['flash'] < self.config.FPS*2 and (self.times_var['flash']/2) == 0:
				self.times_var['flash'] += 1
			else:
				self.game.screen.blit(self.img, (x, y))

		# 如果是正在爆炸的话
		if self.exploding:
			# 显示爆炸动画
			img = pygame.image.load(self.config.IMG_BOOM_HERO[self.times_var['explode']])
			x = self.pos[0] - img.get_rect()[2]/2
			y = self.pos[1] - img.get_rect()[3]/2
			self.game.screen.blit(img, (x, y))

			self.times_var['explode'] += 1
			if self.times_var['explode'] >= len(self.config.IMG_BOOM_HERO):
				self.exploding = False

				# 爆炸结束，标记已死亡
				self.alive = False

	def refresh_bullets_list(self):
		"""
		刷新子弹库，删掉已标记死亡的子弹
		"""
		for bullet in self.bullets:
			if bullet.alive == False:
				self.bullets.remove(bullet)

	def _play_sound(self, sound_type):
		"""
		播放音效
		:param sound_type: 	音效类型
		"""
		sound_urls = {
			str(self.SOUND_TYPE_SHOOT): self.config.SOUND_HERO_SHOOT,
			str(self.SOUND_TYPE_HRUISE): self.config.SOUND_HERO_BRUISE,
			str(self.SOUND_TYPE_BOOM): self.config.SOUND_HERO_BOOM
		}
		sound = pygame.mixer.Sound(sound_urls[str(sound_type)])
		sound.play()
