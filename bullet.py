import pygame


# 定义常量
DIRECTION_UPWARD = 0		# 方向：向上发射
DIRECTION_DOWNWARD = 1		# 方向：向下发射
LAUNCHER_HERO = 0			# 发射者：主角
LAUNCHER_ENEMY = 1			# 发射者：敌机


class Bullet(object):
	"""
	子弹类
	"""

	def __init__(self, config, game, default_pos, launcher, direction, bullet_type=0):
		"""
		构造方法：初始化子弹
		:param config: 		游戏配置对象
		:param game:		游戏对象
		:param default_pos: 子弹默认位置
		:param launcher: 	子弹发射者
		:param direction: 	子弹发射方向
		:param bullet_type:	子弹类型
		"""
		self.config = config
		self.game = game

		# 子弹属性
		self.pos = default_pos		# 子弹位置
		self.launcher = launcher 	# 子弹发射者
		self.direction = direction	# 子弹飞行方向
		self.alive = True			# 子弹生存状态
		self.acc = 5				# 子弹飞行加速度
		self.speed = 10				# 子弹飞行速度

		# 加载图像
		img_url = config.IMG_BULLET_HERO if launcher == LAUNCHER_HERO else config.IMG_BULLET_ENEMIES[bullet_type]
		self.img = pygame.image.load(img_url)

		# 计算图像尺寸
		self.width = self.img.get_rect()[2]
		self.height = self.img.get_rect()[3]

	def show(self):
		"""
		显示子弹
		"""
		x = self.pos[0] - self.width/2
		y = self.pos[1] - self.height/2
		self.game.screen.blit(self.img, (x, y))

	def fly(self):
		"""
		让子弹飞
		"""
		if self.alive == False:
			return

		# 更新飞行速度
		self.speed += self.acc

		# 向上飞
		if self.direction == DIRECTION_UPWARD:
			self.pos[1] -= self.speed 

		# 向下飞
		elif self.direction == DIRECTION_DOWNWARD:
			self.pos[1] += self.speed

		# 边界与碰撞检测
		if self.detect():
			# 标记该子弹已阵亡
			self.alive = False
		else:
			self.show()	# 刷新子弹位置

	def detect(self):
		"""
		碰撞检测和边界检测
		"""
		# 检测越界
		if self.direction == DIRECTION_UPWARD and self.pos[1] <= 0 - self.height/2:
			# 上边界越界了
			return True
		elif self.direction == DIRECTION_DOWNWARD and self.pos[1] >= self.config.SCREEN_HEIGHT - self.height/2:
			# 下边界越界了
			return True

		# 检测碰撞
		enemies = self.game.enemies if self.launcher == LAUNCHER_HERO else [self.game.hero]
		for enemy in enemies:
			x_range = [enemy.pos[0]-enemy.width/2-self.width, enemy.pos[0]+enemy.width/2+self.width]
			y_range1 = [0-self.speed, enemy.pos[1]+enemy.height/2]
			y_range2 = [enemy.pos[1]-enemy.height/2, self.config.SCREEN_HEIGHT+self.speed]
			y_range = y_range1 if self.launcher == LAUNCHER_HERO else y_range2
			if x_range[0] < self.pos[0] < x_range[1] and y_range[0] < self.pos[1] < y_range[1]:
				# 发生碰撞
				if self.launcher == LAUNCHER_HERO:
					# 让目标飞机开花
					enemy.boom()

					# 得分
					self.game.score += self.config.GET_SCORE
					self.game.kill_count += 1
				else:
					# 主角受伤
					enemy.bruise()
				return True

		# 无碰撞和越界
		return False
