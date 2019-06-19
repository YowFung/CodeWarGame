import config
from game import Game


# 主程序入口
if __name__ == '__main__':
	# 创建一个游戏对象，并导入配置
	game = Game(config)

	# 运行游戏
	game.run()
