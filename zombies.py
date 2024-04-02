from turtle import *
import random, time

"""
CLASSES AND FUNCTIONS
"""
def playing_area():
	t = Turtle()
	t.speed(0)
	t.ht()
	t.pu()
	t.goto(-250,250)
	t.color("light blue")
	t.pd()
	t.begin_fill()
	for i in range(4):
		t.forward(500)
		t.right(90)
	t.end_fill()

class Prize(Turtle):
	def __init__(self):
		super().__init__()
		self.speed(0)
		self.pu()
		self.color("orange","gold")
		self.shape("circle")
		self.place()
		
	def place(self):
		self.ht()
		x = random.randint(-240,240)
		y = random.randint(-240,240)
		self.goto(x,y)
		self.st()

	def move(self):
		if self.xcor() > 245 or self.xcor()<-245:
			self.speed(0)
			self.setheading(180-self.heading())
			self.speed(6)
		if self.ycor() > 245 or self.ycor()<-245:
			self.speed(0)
			self.setheading(-1*self.heading())
			self.speed(6)
		degree = random.choice([-2,2])
		self.circle(degree*5,20)

class Player(Turtle):
	def __init__(self,x,color,zombies,left_key, right_key, fire_key, bomb_key):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu()
		self.shape("turtle")
		self.color(color)
		self.goto(x,100)
		degree = self.towards(prize)
		self.setheading(degree)
		self.st()
		self.rounds = []
		self.zombies = zombies
		screen.onkeypress(self.turn_left,left_key)
		screen.onkeypress(self.turn_right,right_key)
		screen.onkey(self.fire, fire_key)
		screen.onkey(self.drop_bomb, bomb_key)

	def move(self):
	# Detect if turtle has left the right side of the playing area
		if self.xcor() > 245 or self.xcor()<-245:
			self.setheading(180-self.heading())
		if self.ycor() > 245 or self.ycor()<-245:
			self.setheading(-1*self.heading())
		self.forward(7)

	def turn_left(self):
		self.left(10)

	def turn_right(self):
		self.right(10)

	def fire(self):
		self.rounds.append(Bullet(self))

	def drop_bomb(self):
		self.ht()
		h = self.heading()
		self.sety(self.ycor()+150)
		self.setheading(0)
		self.pd()
		self.begin_fill()
		self.circle(-150,360)
		self.end_fill()
		self.sety(self.ycor()-150)
		for value,zombie in enumerate(self.zombies[:]):
			if self.distance(zombie)<150:
				# zombie.delete()
				zombie.ht()
				self.zombies.remove(zombie)
		self.pu()
		self.setheading(h)
		time.sleep(1)
		self.showturtle()
		self.clear()
		

class Zombie(Turtle):
	def __init__(self,player,list):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu()
		self.color("green")
		self.shape("turtle")
		x = random.randint(-240,240)
		y = random.randint(-240,240)
		self.goto(x,y)
		self.player = player
		self.list = list
		self.st()

	def move(self):
		self.setheading(self.towards(self.player))
		self.forward(2)

	def delete(self):
		self.ht()
		self.list.remove(self)


class Bullet(Turtle):
	def __init__(self,player):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu()
		self.color("white")
		self.player = player
		self.goto(self.player.xcor(),self.player.ycor())
		self.setheading(self.player.heading())
		self.forward(20)
		self.st()

	def move(self):
		self.forward(15)
		if self.ycor()>200 or self.ycor()<-200 or self.xcor()>200 or self.xcor()<-200:
			self.delete()

	def delete(self):
		self.ht()
		self.player.rounds.remove(self)


class ScoreBoard(Turtle):
	def __init__(self):
		super().__init__()
		self.speed(0)
		self.ht()
		self.penup()
		self.color("white")
		self.goto(0,0)

	def display(self, text):
		self.clear()
		self.color(text.lower())
		self.write("     Game Over!\n"+text+" Survives!", align = "center", font=("Times New Roman",40))

	def game_over(self):
		self.clear()
		self.color("red")
		self.write("GAME OVER!", align = "center", font=("Times New Roman",40))


def update():
	if len(players)==2:
		prize.move()
		for p in players:
			p.move()
			if p.distance(prize)<20:
				prize.place()
				zombies.append(Zombie(p1,zombies))
				zombies.append(Zombie(p2,zombies))
		for zombie in zombies:
			zombie.move()
			for player in players:
				if zombie.distance(player)<20:
					player.ht()
					players.remove(player)
		rounds = p1.rounds + p2.rounds
		for bullet in rounds:
			bullet.move()
			for zombie in zombies:
				if bullet.distance(zombie) < 20:
					bullet.ht()
					rounds.remove(bullet)
					zombie.delete()
		screen.ontimer(update,15)
	else:
		message = ScoreBoard()
		if players[0] == p1:
			message.display("Magenta")
		else:
			message.display("Maroon")
			
		
"""
SCREEN
"""
screen = Screen()
screen.bgcolor("black")
screen.listen()

playing_area()
"""
TURTLE AND OBJECT INSTANTIATION
"""
prize = Prize()
zombies = []
p1 = Player(-100,"magenta",zombies,"a","d","w","s")
p2 = Player(100,"maroon",zombies,"Left","Right","Up","Down")
players = [p1,p2]



"""
GAME LOOP
"""
update()
	
screen.mainloop()				
				
	