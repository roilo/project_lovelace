### NOTES
# UI to be updated

import random
import copy

class Player:
    def __init__(self, name,
                 hp=100, mp=50, bp=50,
                 heal_pot=3, magic_pot=2,
                 physical_min_dmg=15, physical_max_dmg=20,
                 magical_min_dmg=10, magical_max_dmg=25):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.bp = bp
        self.heal_pot = heal_pot
        self.magic_pot = magic_pot
        self.physical_min_dmg = physical_min_dmg
        self.physical_max_dmg = physical_max_dmg
        self.magical_min_dmg = magical_min_dmg
        self.magical_max_dmg = magical_max_dmg
        self.move = None # this is int
        self.valid_moves = [
            (0, "Physical Attack"),
            (1, "Magical Attack"),
            (2, "Block Attack"),
            (3, "Use Health Potion"),
            (4, "Use Magic Potion"),
            (5, "Skip Turn")
        ]

    def physical_attack(self, enemy):
        damage = random.randint(self.physical_min_dmg,
                                self.physical_max_dmg)
        # crit = random.random()
        # if (crit < 0.05):
        #     damage *= 1.5
        if enemy.move == enemy.valid_moves[2]:
            return block(damage)
        enemy.hp -= damage
        return damage, True

    def magical_attack(self, enemy):
        damage = random.randint(self.magical_min_dmg,
                                self.magical_max_dmg)

        if self.mp == 0:
            return 0, False

        result = self.mp - damage
        if result < 0:
            damage = copy.deepcopy(self.mp) # use up all remaining mp
            self.mp = 0
        else:
            self.mp = result
        # crit = random.random()
        # if (crit < 0.05):
        #     damage *= 1.5
        if enemy.move == enemy.valid_moves[2]:
            return block(damage)
        enemy.hp -= damage
        return damage, True

    def block(self, damage):
        result = self.bp - damage
        if result < 0:
            self.bp = 0
            self.hp -= abs(result)
            return damage, True
        self.bp -= damage
        return damage, False

    def heal_hp(self):
        if self.heal_pot > 0:
            heal = 20
            result = self.hp + heal
            if result > 100:
                self.hp += heal - (result - 100) # only stay at 100
            else:
                self.hp = result
            self.heal_pot -= 1
            return heal, True
        return 0, False

    def heal_mp(self):
        if self.magic_pot > 0:
            heal = 25
            result = self.mp + heal
            if result > 50:
                self.mp += heal - (result - 50) # only stay at 50
            else:
                self.mp = result
            self.magic_pot -= 1
            return heal, True
        return 0, False

class Enemy(Player):
    def __init__(self, name=None):
        Player.__init__(self, name)
        self.move_chance = self.update_behavior()

    def enemy_choice(self):
        choice = random.random()
        if self.move_chance[0][0] <= choice < self.move_chance[0][1]:
            return self.valid_moves[0][0] # physical attack
        if self.move_chance[1][0] <= choice < self.move_chance[1][1]:
            return self.valid_moves[1][0] # magical attack
        if self.move_chance[2][0] <= choice < self.move_chance[2][1]:
            return self.valid_moves[2][0] # block attack
        if self.move_chance[3][0] <= choice < self.move_chance[3][1]:
            return self.valid_moves[3][0] # use health potion
        if self.move_chance[4][0] <= choice < self.move_chance[4][1]:
            return self.valid_moves[4][0] # use magic potion
        return self.valid_moves[5][0] # skip
    
    def update_behavior(self, behavior=None):
        # problem: how to dynamically edit distribution
        chance = []
        if behavior == "aggressive":
            chance = [
                [0.60, 1.00], # physical attack, 40%
                [0.20, 0.60], # magical attack, 40%
                [0.00, 0.20], # block attack, 20%
                [-1.00, -1.00], # use health potion, 0%
                [-1.00, -1.00]  # use magic potion, 0%
            ]
        elif behavior == "defensive":
            chance = [
                [0.85, 1.00], # physical attack, 15%
                [0.70, 0.85], # magical attack, 15%
                [0.40, 0.70], # block attack, 30%
                [0.20, 0.40], # use health potion, 20%
                [0.00, 0.20]  # use magic potion, 20%
            ]
        else:
            # default behavior
            chance = [
                [0.70, 1.00], # physical attack, 30%
                [0.40, 0.70], # magical attack, 30%
                [0.20, 0.40], # block attack, 20%
                [0.10, 0.20], # use health potion, 10%
                [0.00, 0.10]  # use magic potion, 10%
            ]
        if self.mp == 0:
            chance[1] = [-1.00, -1.00] # no longer use magic
        if self.bp == 0:
            chance[2] = [-1.00, -1.00] # no longer use shield
        if self.heal_pot == 0:
            chance[3] = [-1.00, -1.00] # no longer use healing potion
        if self.magic_pot == 0:
            chance[4] = [-1.00, -1.00] # no longer use magic potion
        return chance

def status_check(player):
    print("Current status of", player.name)
    print("Health points remaining:", player.hp)
    print("Magic points remaining:", player.mp)
    print("Block points remaining:", player.bp)
    print("Healing potions remaining:", player.heal_pot)
    print("Magic potions remaining:", player.magic_pot)
    print()

player1 = Player(input("Player Name: "))
player2 = Enemy(input("Enemy Name: "))

# first_turn = random.getrandbits(1) # 0 = enemy, 1 = player
first_turn = 1
turn = 0

is_running = True
while is_running:
    turn += 1 # increment turn
    print("Turn", turn) # display turn
    print("Choices:") # display choices
    for i, j in player1.valid_moves:
        print("[" + str(i) + "] " + j)
    print()

    # player turn
    while True:
        choice = int(input("Choice: "))
        is_found = [item for item in player1.valid_moves
                    if item[0] == choice]
        if is_found: # list is not empty
            player1.move = is_found[0][0]
            break
        print("Try again.")

    # enemy turn
    player2.move = player2.enemy_choice()

    # player1 moves
    if player1.move == 0: player1.physical_attack(player2)
    elif player1.move == 1: player1.magical_attack(player2)
    elif player1.move == 2: pass
    elif player1.move == 3: player1.heal_hp()
    elif player1.move == 4: player1.heal_mp()
    elif player1.move == 5: pass

    # player2 moves
    if player2.move == 0: player2.physical_attack(player1)
    elif player2.move == 1: player2.magical_attack(player1)
    elif player2.move == 2: pass
    elif player2.move == 3: player2.heal_hp()
    elif player2.move == 4: player2.heal_mp()
    elif player2.move == 5: pass

    # change enemy behavior depending on health
    if 100 <= player2.hp < 75:
        player2.update_behavior()
    elif 75 <= player2.hp < 50:
        player2.update_behavior("aggressive")
    elif 50 <= player2.hp <= 0:
        player2.update_behavior("defensive")

    # check status
    status_check(player1)
    status_check(player2)

    # end game
    if player1.hp <= 0:
        is_running = False
    elif player2.hp <= 0:
        is_running = False