import random

class Player:
    def __init__(self, name,
                 hp=100, mp=100, bp=100,
                 heal_pot=5, energy_pot=5,
                 physical_min_dmg=10, physical_max_dmg=20,
                 magical_min_dmg=10, magical_max_dmg=30):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.bp = bp
        self.heal_pot = heal_pot
        self.energy_pot = energy_pot
        self.physical_min_dmg = physical_min_dmg
        self.physical_max_dmg = physical_max_dmg
        self.magical_min_dmg = magical_min_dmg
        self.magical_max_dmg = magical_max_dmg
    
    def physical_attack(self, enemy):
        damage = random.randint(self.physical_min_dmg,
                                self.physical_max_dmg)
        crit = random.random()
        # if (crit < 0.10):
        #     damage *= 1.5
        enemy.hp -= damage
        return damage

    def magical_attack(self, enemy):
        damage = random.randint(self.magical_min_dmg,
                                self.magical_max_dmg)
        crit = random.random()
        self.mp -= damage
        # if (crit < 0.10):
        #     damage *= 1.5
        enemy.hp -= damage
        return damage

    def block(self, damage):
        result = self.bp - damage
        if (result < 0):
            self.hp -= damage
            return damage, True
        self.bp -= damage
        return damage, False

    def heal_hp(self):
        if (self.heal_pot > 0):
            heal = 20
            result = self.hp + heal
            if (result > 100):
                self.hp += heal - (result - 100) # only stay at 100
                return True
            self.hp = result
            return True
        return False

    def heal_mp(self):
        if (self.energy_pot > 0):
            heal = 20
            result = self.mp + heal
            if (result > 100):
                self.mp += heal - (result - 100) # only stay at 100
                return True
            self.mp = result
            return True
        return False

class Enemy(Player):
    pass

player1 = Player("Test1")
player2 = Enemy("Test2")

# player1 = Player(input("Player Name: "))
# player2 = Enemy(input("Enemy Name: "))