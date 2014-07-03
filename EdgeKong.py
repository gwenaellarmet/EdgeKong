import EdgeLaser
import time
import Asset
import random

game = EdgeLaser.LaserGame('EdgeKong')
font = EdgeLaser.LaserFont('lcd.elfc')

game.setResolution(500).setDefaultColor(EdgeLaser.LaserColor.LIME)
game.setFrameRate(40)

while True:

	while game.isStopped():
		game.receiveServerCommands()
		time.sleep(0.05)


	player   = Asset.Player(game)
	princess = Asset.Princess(game)

	#definition des plateformes

	p1  = Asset.Platform(game, 10 ,450,350,450)
	p2  = Asset.Platform(game, 100,350,475,350)
	p3  = Asset.Platform(game, 10 ,250,400,250)
	p4  = Asset.Platform(game, 100,150,475,150)
	p5  = Asset.Platform(game, 425,100,475,100)
	p6  = Asset.Platform(game, 425,450,475,450)

	p7  = Asset.Platform(game, 10 ,10 ,10 ,450)
	p8  = Asset.Platform(game, 475,10 ,475,100)
	p9  = Asset.Platform(game, 475,150,475,450)
	p10 = Asset.Platform(game, 10 ,10 ,475,10 )

	world  = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
	world2 = [p1,p2,p3,p4,p5,p6]
	barrels = []
	win  = False
	lost = False
	rate = 50


	while not game.isStopped():
		game.receiveServerCommands()

		if not win and not lost:
			commands = game.receiveServerCommands()

			if rate >= 50:
				r = random.randint(1,100)
				if (r < 10):
					barrels.append(Asset.Barrel(game))
					rate = 0
			else:
				rate += 1

			if game.player1_keys:
				if game.player1_keys.xn :
					player.left(world)
				if game.player1_keys.xp :
					player.right(world)
				if not game.player1_keys.xp and not game.player1_keys.xn:
					player.stopx()
				if game.player1_keys.a :
					player.a()
			
			player.fall(world)

			win = player.collision(princess)

			player.draw()
			princess.draw()

			for p in world2:
				p.draw()

			for c in barrels:
				c.draw()
				if not c.alive:
					barrels.remove(c)

			for c in barrels:
				if c.hit(player):
					lost = True

			#Out of Bounds
			if player.y1 > 470 or player.y1 < 10 or player.x1 > 470 or player.x1 < 10:
				lost = True
			
			game.refresh()
			time.sleep(0.05)
		else:
			if win:
				animation = True

				animation = Asset.Animation(game)

				while not animation.isFinished():
					animation.anim()
					time.sleep(0.05)
					game.refresh()

				Asset.Coeur(game).draw()
				animation.draw()
				game.refresh()
			else:
				font.render(game, "LOST", 50, 200, EdgeLaser.LaserColor.LIME, 10)
				game.refresh()
			
			time.sleep(1)
			game.pause()
			