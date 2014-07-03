import EdgeLaser

speedxcap = 10
speedycap = 15

class Asset:

	def __init__(self, game, x1, y1, x2, y2):
		self.game = game

		#coin sup gauche
		self.x1 = x1
		self.y1 = y1

		#coin inf droite
		self.x2 = x2
		self.y2 = y2


#----Player

class Player(Asset):

	def __init__(self, game):
		Asset.__init__(self, game, 450, 422, 0, 0)
		self.speedx = 0
		self.speedy = 0
		self.jumping = False


	def draw(self):
		self.game.addRectangle(self.x1, self.y1, self.x1+12, self.y1+25, EdgeLaser.LaserColor.LIME)

	def right(self, world):
		if self.speedx < 0:
			self.speedx = 0
		if self.speedx <= speedxcap:
			self.speedx += 1
		self.x1 += self.speedx
		for p in world:
			if self.collision(p):
				self.x1 -= self.speedx
				self.speedx = 0

	def left(self, world):
		if self.speedx > 0:
			self.speedx = 0
		if self.speedx >= -speedxcap:
			self.speedx -= 1
		self.x1 += self.speedx
		for p in world:
			if self.collision(p):
				self.x1 -= self.speedx
				self.speedx = 0

	def stopx(self):
		if self.speedx > 0:
			self.speedx -= 1
		if self.speedx < 0:
			self.speedx += 1

	def fall(self, world):
		if self.speedy <= speedycap:
			self.speedy += 1
		self.y1 += self.speedy
		for p in world:
			if self.collision(p):
				if self.speedy > 0:#on tombe
					self.jumping = False
				self.y1 -= self.speedy
				self.speedy = 0

	def collision(self, p1):
		self.x2 = self.x1 + 12
		self.y2 = self.y1 + 25
		if (self.x1 <= p1.x2 and self.x2 >= p1.x1 and self.y1 <= p1.y2 and self.y2 >= p1.y1):
			return True
		return False


	def resetColl(self):
		self.coll = False

	def a(self):
		if not self.jumping:
			self.speedy = -speedycap
			self.jumping = True


#---------------Platform

class Platform(Asset):

	def __init__(self, game, x1, y1, x2, y2):
		Asset.__init__(self, game, x1, y1, x2, y2)

	def draw(self):
		self.game.addLine(self.x1, self.y1, self.x2, self.y2, EdgeLaser.LaserColor.YELLOW)

class Princess(Asset):

	def __init__(self, game):
		Asset.__init__(self, game, 440, 75, 460, 99)

	def draw(self):
		self.game.addRectangle(self.x1, self.y1, self.x2, self.y2, EdgeLaser.LaserColor.FUCHSIA)

class Barrel:

	def __init__(self, game):
		self.game = game
		self.x = 468
		self.y = 135
		self.dia = 20
		self.alive = True

	def draw(self):

		if (self.x > 80 and self.x < 90) or (self.x > 410 and self.x < 420 and self.y > 200 and self.y < 400) or (self.x > 370 and self.x < 380 and self.y > 400):
			self.y += 5 # descente
		if (self.y > 130 and self.y < 140) or (self.y > 330 and self.y < 340):
			self.x -= 5 # Gauche
		if (self.y > 230 and self.y < 240) or (self.y > 430 and self.y < 440):
			self.x += 5 #droite
		if self.y > 490:
			self.alive = False

		self.game.addCircle(self.x, self.y, self.dia, EdgeLaser.LaserColor.RED)

	def hit(self, player):
		player.x2 = player.x1 + 12
		player.y2 = player.y1 + 25
		return (self.x+(self.dia/2) > player.x1 and self.x-(self.dia/2) < player.x2 and self.y+(self.dia/2) > player.y1 and self.y-(self.dia/2) < player.y2)

class Animation:

	def __init__(self, game):
		self.game = game
		self.x1 = 50
		self.y1 = 300
		self.x2 = 400
		self.y2 = 300
		self.finish = False

	def anim(self):
		if not self.x1 > 190:
			self.x1 += 5
			self.x2 -= 5
		else:
			self.finish = True
		self.draw()
		#self.game.addRectangle(self.x1, self.y1, self.x1+50, self.y1+100, EdgeLaser.LaserColor.LIME)
		#self.game.addRectangle(self.x2, self.y2, self.x2+50, self.y1+100, EdgeLaser.LaserColor.FUCHSIA)

	def draw(self):
		self.game.addRectangle(self.x1, self.y1, self.x1+50, self.y1+100, EdgeLaser.LaserColor.LIME)
		self.game.addRectangle(self.x2, self.y2, self.x2+50, self.y1+100, EdgeLaser.LaserColor.FUCHSIA)

	def isFinished(self):
		return self.finish

class Coeur:
	def __init__(self, game):
		self.game = game
		self.x = 250
		self.y = 260

	def draw(self):
		self.game.addLine(self.x     ,self.y     ,self.x + 30,self.y - 70, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x + 30,self.y - 70,self.x + 25,self.y - 80, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x + 25,self.y - 80,self.x + 5 ,self.y - 80, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x + 5 ,self.y - 80,self.x     ,self.y - 70, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x     ,self.y - 70,self.x - 5 ,self.y - 80, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x - 5 ,self.y - 80,self.x - 25,self.y - 80, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x - 25,self.y - 80,self.x - 30,self.y - 70, EdgeLaser.LaserColor.RED)
		self.game.addLine(self.x - 30,self.y - 70,self.x     ,self.y     , EdgeLaser.LaserColor.RED)