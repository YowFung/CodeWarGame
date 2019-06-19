import pygame
import random
import time
from hero import *
from enemy import *


class Game(object):
	"""
	游戏类
	"""

	# 定义类常量：游戏状态
	STATUS_WAIT = 0				# 等待游戏开始
	STATUS_READY = 1			# 游戏准备开始
	STATUS_RUN = 2				# 游戏正在进行
	STATUS_OVER = 3				# 游戏已结束

	# 定义类常量：菜单类型
	MENU_TYPE_WAIT = 0			# 等待状态时的菜单
	MENU_TYPE_OVER = 1			# 游戏结束后的菜单

	# 定义类常量：菜单按钮
	MENU_BTN_START = 0			# “开始游戏” 按钮
	MENU_BTN_AGAIN = 1			# “再来一次” 按钮
	MENU_BTN_EXIT = 2			# “退出游戏” 按钮

	# 定义类常量：音效类型
	SOUND_TYPE_READY_GO = 0		# ready go
	SOUND_TYPE_SELECT_MENU = 1	# 选择菜单
	SOUND_TYPE_GAME_OVER = 2	# game over

	def __init__(self, config):
		"""
		构造方法，类初始化
		:param config: 		游戏配置对象
		"""
		# 加载游戏配置对象
		self.config = config

		# 初始化 pygame
		pygame.init()

		# 生成一个时钟对象
		self.clock = pygame.time.Clock()

		# 创建显示窗体
		size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
		self.screen = pygame.display.set_mode(size)

		# 设置窗体标题
		pygame.display.set_caption(config.GAME_NAME)

		# 加载背景图片
		self.bg = pygame.image.load(config.IMG_BG_WAIT)
		self.screen.blit(self.bg, (0, 0))

		# 加载背景音乐并播放
		pygame.mixer.music.load(config.MUSIC_WAIT)
		pygame.mixer.music.set_volume(config.BGM_VOLUME)
		pygame.mixer.music.play(-1)

		# 初始化游戏角色和武器容器
		self.hero = None			# 主角对象
		self.enemies = []			# 敌机对象列表
		self.bullets = []			# 子弹对象列表

		# 初始化菜单选项
		self.menu_btns = []
		self.menu_btn_selected = self.MENU_BTN_START

		# 初始化动画帧计次变量
		self.times_var = {}
		self.times_var['last_tick'] = pygame.time.get_ticks()

		# 允许清屏
		self.screen_clear_enable = True

		# 设置被记录的按键
		self.press_keys = []

		# 初始化游戏得分和杀敌数
		self.score = 0
		self.kill_count = 0

		# 初始化游戏进行中时背景地图
		self.map = {"max_height": 0, "y_pos": 0}

		# 设置默认游戏状态
		self.status = self.STATUS_WAIT

	def run(self):
		"""
		游戏运行
		"""
		while True:
			# 事件处理
			for event in pygame.event.get():
				# 是否为退出事件
				if event.type == pygame.QUIT:
					# 退出游戏
					exit()

				# 是否为按键按下事件
				elif event.type == pygame.KEYDOWN:
					self.press_keys.append(event.key)

				# 是否为按键弹起事件
				elif event.type == pygame.KEYUP:
					self.press_keys.remove(event.key)

			# 执行按键事件
			if len(self.press_keys):
				self._process_keys_event()

			# 更新游戏画面显示
			self._update_screen()

			# 如果正在游戏中，则自动产生敌机
			if self.status == self.STATUS_RUN:
				self._auto_make_enemy()

			# 刷新屏幕
			pygame.display.update()

			# 更新时钟
			self.clock.tick(self.config.FPS)

	def _create_btn(self, btn_id, y_pos, sel=False):
		"""
		创建菜单按钮
		:param btn_id:		按钮 ID
		:param y_pos: 		垂直方向坐标
		:param sel:			是否被选中
		:return:			{btn object}
		"""
		if btn_id == self.MENU_BTN_START:
			img = self.config.IMG_MENU_START_SEL if sel else self.config.IMG_MENU_START_DEF
		elif btn_id == self.MENU_BTN_AGAIN:
			img = self.config.IMG_MENU_AGAIN_SEL if sel else self.config.IMG_MENU_AGAIN_DEF
		elif btn_id == self.MENU_BTN_EXIT:
			img = self.config.IMG_MENU_EXIT_SEL if sel else self.config.IMG_MENU_EXIT_DEF
		else:
			return None

		img = pygame.image.load(img)
		w = img.get_rect()[2]
		h = img.get_rect()[3]
		x = self.config.SCREEN_WIDTH/2 - w/2
		y = y_pos - h/2

		return {
			"img": img,
			"width": w,
			"height": h,
			"x_pos": x + w/2,
			"y_pos": y_pos,
			"seleted": sel
		}

	def _update_screen(self):
		"""
		更新画面显示
		"""
		# 清屏
		if self.screen_clear_enable:
			self.screen.fill((0, 0, 0))

		# 恢复允许清屏
		self.screen_clear_enable = True

		# 如果游戏未开始
		if self.status == self.STATUS_WAIT:
			# 重画背景
			self.screen.blit(self.bg, (0, 0))

			# 更新菜单选中情况
			self._set_menu(self.MENU_TYPE_WAIT, self.menu_btn_selected)

			# 显示游戏按键说明
			font = pygame.font.Font(self.config.FONT_HELP['file'], self.config.FONT_HELP['size'])
			text = u"-- [W] [S] [A] [D] [Space] --"
			surface = font.render(text, True, self.config.FONT_HELP['color'])
			x = self.config.SCREEN_WIDTH/2 - surface.get_rect()[2]/2
			y = self.config.SCREEN_HEIGHT - 60
			self.screen.blit(surface, (x, y))

		# 如果游戏即将开始
		elif self.status == self.STATUS_READY:
			# 显示 ready 画面
			if self.times_var['ready'] < len(self.config.IMG_TEXT_READY)*2:
				img = pygame.image.load(self.config.IMG_TEXT_READY[int(self.times_var['ready']/2)])
				x = self.config.SCREEN_WIDTH/2 - img.get_rect()[2]/2
				y = self.config.SCREEN_HEIGHT/2 - img.get_rect()[3]/2
				self.screen.blit(img, (x, y))
				self.times_var['ready'] += 1

			# 画面停留一秒
			elif self.times_var['ready'] < len(self.config.IMG_TEXT_READY) + self.config.FPS:
				self.screen_clear_enable = False
				self.times_var['ready'] += 1

			# 显示 go 画面
			elif self.times_var['go'] < len(self.config.IMG_TEXT_GO)*2:
				img = pygame.image.load(self.config.IMG_TEXT_GO[int(self.times_var['go']/2)])
				x = self.config.SCREEN_WIDTH/2 - img.get_rect()[2]/2
				y = self.config.SCREEN_HEIGHT/2 - img.get_rect()[3]/2
				self.screen.blit(img, (x, y))
				self.times_var['go'] += 1

			# 画面停留一秒
			elif self.times_var['go'] < len(self.config.IMG_TEXT_GO) + self.config.FPS:
				self.screen_clear_enable = False
				self.times_var['go'] += 1

			# ready 完成，正式开始游戏
			else:
				self._game_start()

		# 如果游戏正在进行中
		elif self.status == self.STATUS_RUN:
			# 清屏
			self.screen.fill((0, 0, 0))

			# 刷新背景图片
			self.screen.blit(self.bg, (0, self.map['y_pos']))
			self.map['y_pos'] += 5
			if self.map['y_pos'] > 0:
				self.map['y_pos'] = 0 - self.map['max_height'] + self.config.SCREEN_HEIGHT

			# 刷新显示子弹
			self._refresh_bullets()

			# 刷新显示敌机
			self._refresh_enmies()

			# 刷新主角状态
			if self.hero.alive:
				# 主角还活着，刷新显示主角
				self.hero.show()

				# 显示主角血量
				for i in range(self.config.BLOOD_LARGE):
					img = self.config.IMG_BLOOD_HAS if i < self.hero.blood else self.config.IMG_BLOOD_LOSS
					img = pygame.image.load(img)
					x = 10 + i*20
					y = 10 if i < self.hero.blood else 12
					self.screen.blit(img, (x, y))

				# 显示游戏得分
				font = pygame.font.Font(self.config.FONT_SCORE['file'], self.config.FONT_SCORE['size'])
				surface = font.render(str(self.score), True, self.config.FONT_SCORE['color'])
				x = self.config.SCREEN_WIDTH - surface.get_rect()[2] - 10
				y = 10
				self.screen.blit(surface, (x, y))
			else:
				# 主角已死亡，标记游戏结束
				self._game_over()

		# 如果游戏已结束
		elif self.status == self.STATUS_OVER:
			# 动态闪烁 Game Over 标题，每秒闪一次
			self.screen.fill((0, 0, 0))
			self.times_var['over'] += 1
			if self.times_var['over'] > self.config.FPS:
				self.times_var['over'] = 0

			if self.times_var['over'] < self.config.FPS/2:
				img = pygame.image.load(self.config.IMG_TEXT_GAME_OVER[0])
			else:
				img = pygame.image.load(self.config.IMG_TEXT_GAME_OVER[1])

			x = self.config.SCREEN_WIDTH/2 - img.get_rect()[2]/2
			y = self.config.SCREEN_HEIGHT/2 - img.get_rect()[3]/2 - 150
			self.screen.blit(img, (x, y))

			# 更新菜单选中情况
			self._set_menu(self.MENU_TYPE_OVER, self.menu_btn_selected)

			# 显示游戏得分结果
			font = pygame.font.Font(self.config.FONT_RESULT['file'], self.config.FONT_RESULT['size'])
			text_score = "SCORE: " + str(self.score)
			surface_score = font.render(text_score, True, self.config.FONT_RESULT['color'])
			x = self.config.SCREEN_WIDTH/2 - surface_score.get_rect()[2]/2
			y = self.config.SCREEN_HEIGHT/2 - img.get_rect()[3]/2 + 20
			self.screen.blit(surface_score, (x, y))

			# 显示游戏杀敌数结果
			font = pygame.font.Font(self.config.FONT_RESULT['file'], self.config.FONT_RESULT['size'])
			text_kill = "KILL: " + str(self.kill_count) 
			surface_kill = font.render(text_kill, True, self.config.FONT_RESULT['color'])
			x = self.config.SCREEN_WIDTH/2 - surface_kill.get_rect()[2]/2
			y = self.config.SCREEN_HEIGHT/2 - img.get_rect()[3]/2 + 40
			self.screen.blit(surface_kill, (x, y))

	def _set_menu(self, menu_type, sel_btn):
		"""
		设置菜单
		:param menu_type:	菜单类型
		:param sel_btn:		选中哪个按钮
		"""
		# 删除原有的菜单按钮
		for btn in self.menu_btns:
			self.menu_btns.remove(btn)
			del(btn)

		# 显示等待状态时的菜单
		if menu_type == self.MENU_TYPE_WAIT:
			btn1 = self._create_btn(self.MENU_BTN_START, 300, sel_btn == self.MENU_BTN_START)
			btn2 = self._create_btn(self.MENU_BTN_EXIT, 380, sel_btn == self.MENU_BTN_EXIT)
			self.menu_btns.append(btn1)
			self.menu_btns.append(btn2)

		# 显示游戏结束时的菜单
		if menu_type == self.MENU_TYPE_OVER:
			btn1 = self._create_btn(self.MENU_BTN_AGAIN, 300, sel_btn == self.MENU_BTN_AGAIN)
			btn2 = self._create_btn(self.MENU_BTN_EXIT, 380, sel_btn == self.MENU_BTN_EXIT)
			self.menu_btns.append(btn1)
			self.menu_btns.append(btn2)

		for btn in self.menu_btns:
			if btn:
				x = btn['x_pos'] - btn['width']/2
				y = btn['y_pos'] - btn['height']/2
				self.screen.blit(btn['img'], (x, y))

	def _refresh_enmies(self):
		"""
		刷新敌机列表，去除已毁灭的敌机，让活着的敌机继续飞
		"""
		for enemy in self.enemies:
			if enemy.alive == False:
				# 移除对象并垃圾回收
				self.enemies.remove(enemy)
			else:
				# 继续飞
				enemy.fly()

	def _refresh_bullets(self):
		"""
		刷新子弹列表，去除已消失的子弹
		"""
		for bullet in self.bullets:
			if bullet.alive == False:
				# 移除对象并垃圾回收
				self.bullets.remove(bullet)
			else:
				# 继续飞
				bullet.fly()

	def _game_ready(self):
		"""
		游戏准备开始处理事件
		"""
		# 清除菜单选中项
		self.menu_btn_selected = None

		# 设置游戏状态
		self.status = self.STATUS_READY

		# 初始化帧动画计次变量
		self.times_var['ready'] = 0
		self.times_var['go'] = 0

		# 创建主角对象
		self.hero = Hero(self.config, self)

		# 停止播放背景音乐
		pygame.mixer.music.stop()

		# 播放游戏准备开始的音效
		self._play_sound(self.SOUND_TYPE_READY_GO)

	def _game_start(self):
		"""
		游戏正式开始
		"""
		# 设置游戏状态
		self.status = self.STATUS_RUN

		# 播放游戏进行时的背景音乐
		pygame.mixer.music.load(self.config.MUSIC_RUN)
		pygame.mixer.music.set_volume(self.config.BGM_VOLUME)
		pygame.mixer.music.play(-1)

		# 清屏
		self.screen.fill((0, 0, 0))

		# 设置游戏背景
		self.bg = pygame.image.load(self.config.IMG_BG_RUN)
		w = self.bg.get_rect()[2]
		h = self.bg.get_rect()[3]
		s = float(w/self.config.SCREEN_WIDTH)
		self.map['max_height'] = int(h/s)
		self.bg = pygame.transform.scale(self.bg, (self.config.SCREEN_WIDTH, self.map['max_height']))
		self.map['y_pos'] = 0 - self.map['max_height'] + self.config.SCREEN_HEIGHT

		# 初始化得分和杀敌数
		self.score = 0
		self.kill_count = 0

	def _game_over(self):
		"""
		游戏结束处理事件
		"""
		# 设置游戏状态
		self.status = self.STATUS_OVER

		# 设置菜单默认选中项
		self.menu_btn_selected = self.MENU_BTN_AGAIN
		 
		# 销毁所有子弹
		for bullet in self.bullets:
			del(bullet)

		# 销毁所有敌机
		for enemy in self.enemies:
			enemy.boom()

		# 清理战场
		self.hero = None
		self.enemies = []
		self.bullets = []

		# 播放游戏结束音效
		self._play_sound(self.SOUND_TYPE_GAME_OVER)

		# 停止播放背景音乐
		pygame.mixer.music.stop()

		# 初始化帧动画计次变量
		self.times_var['over'] = 0

	def _auto_make_enemy(self):
		"""
		自动产生敌机
		"""
		tick = pygame.time.get_ticks()

		# 每隔两秒产生敌机
		if tick - self.times_var['last_tick'] >= 2000:
			self.times_var['last_tick'] = tick

			# 每次产生0个或1个敌机
			num = 0 if random.random() < 0.3 else 1
			if num > 0:
				# 创建一个敌机并设置随机坐标
				x = int(random.random()*self.config.SCREEN_WIDTH)
				y = -100
				enemy = Enemy(self.config, [x, y], self)

				# 添加到敌机列表中
				self.enemies.append(enemy)

	def _process_keys_event(self):
		"""
		处理按键事件
		"""
		for key in self.press_keys:
			# 当游戏处于等待状态时
			if self.status == self.STATUS_WAIT:
				if key in self.config.KEY_UP:
					# 选中菜单按钮：开始游戏
					self.menu_btn_selected = self.MENU_BTN_START
					self._play_sound(self.SOUND_TYPE_SELECT_MENU)
				elif key in self.config.KEY_DOWN:
					# 选中菜单按钮：退出游戏
					self.menu_btn_selected = self.MENU_BTN_EXIT
					self._play_sound(self.SOUND_TYPE_SELECT_MENU)
				elif key in self.config.KEY_SELECT:
					# 执行选中的菜单事件
					if self.menu_btn_selected == self.MENU_BTN_EXIT:
						# 退出游戏
						exit()
					elif self.menu_btn_selected == self.MENU_BTN_START:
						# 开始准备游戏
						self._game_ready()

			# 当游戏正在运行时
			elif self.status == self.STATUS_RUN:
				if key in self.config.KEY_LEFT:
					# 让主角向左移动
					self.hero.move(MOVE_DIR_LEFT)
				elif key in self.config.KEY_RIGHT:
					# 让主角向右移动
					self.hero.move(MOVE_DIR_RIGHT)
				elif key in self.config.KEY_SHOOT:
					# 让主角发射子弹
					self.hero.shoot()

			# 当游戏结束时
			elif self.status == self.STATUS_OVER:
				if key in self.config.KEY_UP:
					# 选中菜单按钮：再来一次
					self.menu_btn_selected = self.MENU_BTN_AGAIN
					self._play_sound(self.SOUND_TYPE_SELECT_MENU)
				elif key in self.config.KEY_DOWN:
					# 选中菜单按钮：退出游戏
					self.menu_btn_selected = self.MENU_BTN_EXIT
					self._play_sound(self.SOUND_TYPE_SELECT_MENU)
				elif key in self.config.KEY_SELECT:
					# 执行选中的菜单事件
					if self.menu_btn_selected == self.MENU_BTN_EXIT:
						# 退出游戏
						exit()
					elif self.menu_btn_selected == self.MENU_BTN_AGAIN:
						# 开始准备游戏
						self._game_ready()

	def _play_sound(self, sound_type):
		"""
		播放音效
		:param sound_type: 	音效类型
		"""
		sound_urls = {
			str(self.SOUND_TYPE_READY_GO): self.config.SOUND_READY_GO,
			str(self.SOUND_TYPE_SELECT_MENU): self.config.SOUND_SELECT,
			str(self.SOUND_TYPE_GAME_OVER): self.config.SOUND_GAME_OVER
		}
		sound = pygame.mixer.Sound(sound_urls[str(sound_type)])
		sound.play()
