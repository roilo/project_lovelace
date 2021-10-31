#imports all from the random module
#imports time to pause yourself from the heat of the battle
from random import *
import time

#the whole game is made of a class
class Play:

	#stat attributes of both player and enemy
	def __init__ (self, name = input("Before playing this game, what is your name? ")):
		self.name = name
		self.healthCount = 100
		self.energyCount = 100
		self.blockCount = 50
		self.healthPotionCount = 4
		self.energyPotionCount = 4
		self.firstTurn = randint(0, 1)
		self.damagePhysical = randint(10, 20)
		self.damageMagical = randint(5, 30)
		self.damageEnemy = randint(5, 30)
		self.criticalChance = random()
		self.statusChance = random()
		self.move = bool(getrandbits(1))

	#player's perspective
	def turnPlayer (self, enemy):
		print()
		answer = input("Your move: ").upper()
		if answer == "ATTACK":
			self.attackPlayer(enemy)
			return
		if answer == "HEAL":
			self.healPlayer(enemy)
			return
		if answer == "BLOCK":
			self.block(enemy)
			return
		if answer == "CHECK":
			self.statusCheck(enemy)
			return
		if answer == "QUIT":
			self.quitGame(enemy)
			return
		print("Move not known.")
		print("Try again.")
		time.sleep(1)
		self.turnPlayer(enemy)
		return

	#choices
	#attack part I - attack type choices
	def attackPlayer (self, enemy):
		print()
		attackAnswer = input("Your attack: ").upper()
		if attackAnswer == "PHYSICAL":
			self.physicalStrike(enemy)
			return
		if attackAnswer == "MAGICAL":
			self.energyCheck(enemy)
			return
		print("Error.")
		print("Try again.")
		time.sleep(1)
		self.attackPlayer(enemy)

	#attack part II - physical strikes
	def physicalStrike(self, enemy):
		print()
		print("Drawing your trusted weapon...")
		time.sleep(1)
		if self.criticalChance <= 0.015:
			self.criticalStrike(enemy)
			return
		enemy.healthCount -= self.damagePhysical
		print("... you made %s damage to your opponent!" % self.damagePhysical)
		time.sleep(1)
		print()
		print("Your enemy, %s, has %s health remaining." % (enemy.name, enemy.healthCount))
		self.winAgainst(enemy)

	#attack part IIIa - energy check
	def energyCheck(self, enemy):
		print()
		print("As you focus your mind into gathering energies...")
		time.sleep(1)
		if self.energyCount >= 0:
			self.magicalStrike(enemy)
			return
		print("... you ran out of energy to gather.")
		print("Try again.")
		time.sleep(1)
		self.attackPlayer(enemy)

	#attack part IIIb - magical strikes
	def magicalStrike(self, enemy):
		enemy.healthCount -= self.damageMagical
		self.energyCount -= self.damageMagical
		print("... you release them to harm your opponent for %s!" % self.damageMagical)
		time.sleep(1)
		print("Be wary of gathering too much energies...")
		time.sleep(1)
		print("... as you only have %s energy remaining..." % self.energyCount)
		time.sleep(1)
		print()
		print("Your enemy, %s, has %s health remaining." % (enemy.name, enemy.healthCount))
		self.winAgainst(enemy)

	#attack part IV - critical strikes
	def criticalStrike(self, enemy):
		criticalDamage = self.damagePhysical * 2
		enemy.healthCount -= criticalDamage
		print("... you made %s damage to your opponent as a critical hit!" % criticalDamage)
		time.sleep(1)
		print()
		print("Your enemy, %s, has %s health remaining." % (enemy.name, enemy.healthCount))
		self.winAgainst(enemy)

	#block part I - shield health check
	def block (self, enemy):
		print()
		print("As your enemy strikes you...")
		time.sleep(1)
		if self.blockCount >= 0:
			self.blockDamage(enemy)
			return
		self.healthCount -= enemy.damageEnemy
		print("... you realize your shield is broken...")
		time.sleep(1)
		print("... and you took %s damage!" % enemy.damageEnemy)
		time.sleep(1)
		print()
		print("You, %s, have a total of %s health remaining." % (self.name, self.healthCount))
		self.loseAgainst(enemy)

	#block part II - return damage
	def blockDamage (self, enemy):
		self.blockCount -= enemy.damageEnemy
		returnDamage = self.blockCount - 5
		enemy.healthCount -= returnDamage
		print("... you use your sturdy shield to block...") 
		time.sleep(1)
		print("... and returned %s damage to your opponent!" % returnDamage)
		time.sleep(1)
		print()
		print("You have %s shield health remaining." % self.blockCount)
		time.sleep(1)
		print()
		print("Your enemy, %s, has %s health remaining." % (enemy.name, enemy.healthCount))
		self.winAgainst(enemy)

	#regain health or energy - choice
	def healPlayer(self, enemy):
		print()
		healOrEnergy = input("A health potion or energy potion? ").upper()
		if healOrEnergy == "HEALTH POTION":
			self.healCheck(enemy)
			return
		if healOrEnergy == "ENERGY POTION":
			self.energyHealCheck(enemy)
			return
		print("Move not known.")
		print("Try again.")
		time.sleep(1)
		self.healPlayer(enemy)

	#regain health part I - potion number check
	def healCheck (self, enemy):
		print()
		print("As you check your inventory...")
		time.sleep(1)
		if self.healthPotionCount != 0:
			self.healthHeal(enemy)
			return
		print("You're out of health potions.")
		print("Try again.")
		time.sleep(1)
		self.turnPlayer(enemy)

	#regain health part II - heal health
	def healthHeal (self, enemy):
		self.healthPotionCount -= 1
		self.healthCount += 20
		print("... you found a health potion and drank it...")
		time.sleep(1)
		print("... and your life force was restored for 20 health.")
		time.sleep(1)
		print()
		print("You, %s, have a total of %s health remaining." % (self.name, self.healthCount))
		self.turnPlayer(enemy)

	#regain energy part I - potion number check
	def energyHealCheck (self, enemy):
		print()
		print("As you check your inventory...")
		time.sleep(1)
		if self.energyPotionCount != 0:
			self.energyHeal(enemy)
			return
		print("You're out of energy potions.")
		print("Try again.")
		time.sleep(1)
		self.turnPlayer(enemy)

	#regain energy part II = heal energy
	def energyHeal (self, enemy):
		self.energyPotionCount -= 1
		self.energyCount += 20
		print("... you found an energy potion and drank it...")
		time.sleep(1)
		print("... and your remaining energies was restored for 20 energy.")
		time.sleep(1)
		print()
		print("You, %s, have a total of %s energy remaining." % (self.name, self.healthCount))
		self.turnPlayer(enemy)

	#status check
	def statusCheck (self, enemy):
		print()
		print("Checking status...")
		time.sleep(3)
		print("Player's Name: %s" % self.name)
		time.sleep(1)
		print("Health: %s" % self.healthCount)
		time.sleep(1)
		print("Energy: %s" % self.energyCount)
		time.sleep(1)
		print("Block: %s" % self.blockCount)
		time.sleep(1)
		print("Enemy's Name: %s" % enemy.name)
		time.sleep(1)
		print("Enemy Health: %s" % enemy.healthCount)
		time.sleep(1)
		print()
		print("Checking done.")
		self.turnPlayer(enemy)

	#enemy's perspective
	#damages the player
	def turnEnemy (self, enemy):
		self.healthCount -= enemy.damageEnemy
		print()
		print("Your enemy draws close in an attempt to hit you...")
		time.sleep(1)
		print("%s is successful and you, %s, took %s damage!" % (enemy.name, self.name, enemy.damageEnemy))
		time.sleep(1)
		print()
		print("You, %s, have a total of %s health remaining." % (self.name, self.healthCount))
		time.sleep(1)
		self.loseAgainst(enemy)

	#loop functions
	#break the loop
	#also a choice to exit game
	def quitGame (self, enemy):
		print()
		print("The battle has ended...")
		time.sleep(1)
		print("The announcer and spectators have left...")
		time.sleep(1)
		print("Only you and your enemy are the only ones left.")
		time.sleep(1)
		print("This one is just one of the fights in the arena.")
		time.sleep(1)
		print("There are more battles to come...")
		time.sleep(1)
		print("Better prepare for the next.")
		time.sleep(3)
		return

	#check if player can continue
	def loseAgainst (self, enemy):
		if self.healthCount >= 0:
			self.turnPlayer(enemy)
			return
		print()
		print("You lost the battle!")
		time.sleep(1)
		print("As your corpse falls to the ground, the crowd cheers your enemy's name.")
		time.sleep(3)
		self.quitGame(enemy)

	#check if enemy can continue
	def winAgainst(self, enemy):
		if enemy.healthCount >= 0:
			self.turnEnemy(enemy)
			return
		print()
		print("The enemy has been defeated!")
		time.sleep(1)
		print("The crowd cheers for your victory.")
		time.sleep(3)
		self.quitGame(enemy)

	#function to be used to play
	#only called one time
	def playGame (self, enemy):
		print()
		print("The crowd is cheering for the battle between you, %s and your enemy, %s..." % (self.name, enemy.name))
		time.sleep(3)
		print("Who's gonna win?")
		time.sleep(1)
		print("Who's gonna lose?")
		time.sleep(1)
		print("The winner takes all!")
		time.sleep(1)
		print("You step in the arena...")
		time.sleep(1)
		print("Your enemy also steps in the arena...")
		time.sleep(1)
		print("The announcer shouts...")
		time.sleep(1)
		print("'THE BATTLE BEGINS!'")
		time.sleep(1)
		self.firstMove(enemy)

	#function to check if the first move belongs to the enemy or the player
	#only called one time
	def firstMove(self, enemy):
		if self.move == True:
			print()
			print("You get the first turn to strike down your enemy.")
			print("Use it well.")
			self.turnPlayer(enemy)
			return
		print()
		print("%s gets the first turn." % enemy.name)
		self.turnEnemy(enemy)

#Calls the class to create the player
thePlayer = Play()

#Calls the class to create the enemy
enemyName = ["Batman", "Magikarp", "Gandalf"]
theEnemy = Play(choice(enemyName))

#Prompts user to fight or not
def prompt():
	gamePlay = input("Would you like to play this game? ").upper()
	if gamePlay == "YES":
		thePlayer.playGame(theEnemy)
		return
	print("Okay.")
	print("Game exiting...")
	time.sleep(3)
	return

#Fight!
prompt()