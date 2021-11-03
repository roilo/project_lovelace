"""[Project Lovelace]

Description
-----------
A turn-based combat game with text-based user interface.
Updated old code from 2016 to current knowledge of Python.

Notes
-----
Docstrings partially follow the Numpy Docstring Standard.
Python version used is 3.8.2.
"""
import copy
import random
import time

class Player:
    """A class to represent a Player.

    Attributes
    ----------
    name : str
        Name of Player
    hp : int
        Health points
    mp : int
        Magic points
    bp : int
        Block points
    heal_pot : int
        Amount of healing potions available
    magic_pot : int
        Amount of magic potions available
    physical_min_dmg : int
        Lower limit of physical damage
    physical_max_dmg : int
        Upper limit of physical damage
    magical_min_dmg : int
        Lower limit of magical damage
    magical_max_dmg : int
        Upper limit of magical damage
    move : tuple(int, str)
        Selected move by Player
    valid_moves : list(tuple(int, str))
        List of selectable moves by Player

    Methods
    -------
    __init__(name)
        Construct attributes
    physical_attack(enemy)
        Deals physical damage to enemy
    magical_attack(enemy)
        Deals magical damage to enemy
    block_attack(damage)
        Nullifies damage
    heal_hp()
        Restore player's health points
    heal_mp()
        Restore player's magic points
    perform_move(enemy)
        Calls method based on selected move
    """
    def __init__(self, name,
                 hp = 100, mp = 50, bp = 50,
                 heal_pot = 3, magic_pot = 2,
                 physical_min_dmg = 15, physical_max_dmg = 20,
                 magical_min_dmg = 10, magical_max_dmg = 25):
        """Construct variables for use by Player class methods.

        Parameters
        ----------
        name : str
            Name of Player
        hp : int
            Health points
        max_hp : int
            Maximum health points
        mp : int
            Magic points
        max_mp : int
            Maximum magic points
        bp : int
            Block points
        max_bp : int
            Maximum health points
        heal_pot : int
            Amount of healing potions available
        magic_pot : int
            Amount of magic potions available
        physical_min_dmg : int
            Lower limit of physical damage
        physical_max_dmg : int
            Upper limit of physical damage
        magical_min_dmg : int
            Lower limit of magical damage
        magical_max_dmg : int
            Upper limit of magical damage
        move : tuple(int, str)
            Selected move by Player
        valid_moves : list(tuple(int, str))
            List of selectable moves by Player
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.bp = bp
        self.max_bp = bp
        self.heal_pot = heal_pot
        self.magic_pot = magic_pot
        self.physical_min_dmg = physical_min_dmg
        self.physical_max_dmg = physical_max_dmg
        self.magical_min_dmg = magical_min_dmg
        self.magical_max_dmg = magical_max_dmg
        self.move = (int, str)
        self.valid_moves = [
            (0, "Physical Attack"),
            (1, "Magical Attack"),
            (2, "Block Attack"),
            (3, "Consume Health Potion"),
            (4, "Consume Magic Potion"),
            (5, "Skip Turn")
        ]

    def physical_attack(self, enemy):
        """Reduces the enemy's health by applying damage in range of
        [physical_min_dmg, physical_max_dmg] to health points.

        Parameters
        ----------
        enemy : Enemy(Player) or Player
            Instantiated Enemy or Player class

        Returns
        -------
        damage, True : tuple
            Physical damage dealt to enemy and information to
            determine successful or failed attack.
        """
        damage = random.randint(self.physical_min_dmg,
                                self.physical_max_dmg)
        # crit = random.random()
        # if (crit < 0.05):
        #     damage *= 1.5
        if enemy.move[0] == enemy.valid_moves[2][0]:
            return enemy.block_attack(damage)
        enemy.hp -= damage
        return damage, True

    def magical_attack(self, enemy):
        """Reduces the enemy's health by applying damage in range of
        [magical_min_dmg, magical_max_dmg] to health points.

        Parameters
        ----------
        enemy : Enemy(Player) or Player
            Instantiated Enemy or Player class

        Returns
        -------
        tuple(int, bool)
            Magical damage dealt to enemy and information to
            determine successful or failed attack.
        """
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
        # if (crit < 0.10):
        #     damage *= 1.5
        if enemy.move[0] == enemy.valid_moves[2][0]:
            return enemy.block_attack(damage)
        enemy.hp -= damage
        return damage, True

    def block_attack(self, damage):
        """Moves the damage from physical_attack() or magical_attack()
        to block points instead of health points given available
        block points.

        Parameters
        ----------
        damage : int
            Amount of damage from
            physical_attack() or magical_attack()

        Returns
        -------
        tuple(int, bool)
            Physical or magical damage dealt to enemy and
            information to determine successful or failed block.
            Successful block = failed attack
            Failed block = successful attack
        """
        result = self.bp - damage
        if result < 0:
            self.bp = 0
            self.hp -= abs(result)
            return abs(result), True
        self.bp -= damage
        return damage, False

    def heal_hp(self, heal = 20):
        """Recover health to health points given available amount of
        heal_pot.

        Parameters
        ----------
        heal : int
            Amount of health recovered by player

        Returns
        -------
        tuple(int, bool)
            Amount of health recovery to player and information to
            determine successful or failed recovery.
        """
        if self.heal_pot > 0:
            result = self.hp + heal
            if result > self.max_hp:
                # ensures that hp only reaches at most max_hp
                heal -= result - self.max_hp
                self.hp += heal
            else:
                self.hp = result
            self.heal_pot -= 1 # decrement
            return heal, True
        return 0, False

    def heal_mp(self, heal = 25):
        """Recover magic to magic points given available amount of
        magic_pot.

        Parameters
        ----------
        heal : int
            Amount of magic recovered by player

        Returns
        -------
        tuple(int, bool)
            Amount of magic recovery dealt to player and
            information to determine successful or failed recovery.
        """
        if self.magic_pot > 0:
            result = self.mp + heal
            if result > self.max_mp:
                # ensures that mp only reaches at most max_mp
                heal -= result - self.max_mp
                self.mp += heal
            else:
                self.mp = result
            self.magic_pot -= 1 # decrement
            return heal, True
        return 0, False
    
    def perfom_move(self, enemy):
        """Call methods in Player class given self.move.

        Parameters
        ----------
        enemy : Enemy(Player) or Player
            Instantiated Enemy or Player class

        Returns
        -------
        tuple(int, bool)
            Returned value from called function.
        """
        if self.move[0] == 0:
            return self.physical_attack(enemy)
        elif self.move[0] == 1:
            return self.magical_attack(enemy)
        elif self.move[0] == 3:
            return self.heal_hp()
        elif self.move[0] == 4:
            return self.heal_mp()
        else:
            return int, bool

class Enemy(Player):
    """Inherited Player class to represent enemy.

    Attributes
    ----------
    move_chance : list(list(float, float))
        List of distribution range of moves

    Methods
    -------
    __init__()
        Construct additional attributes from inherited attributes
    enemy_choice()
        Randomly select moves based on distribution range
    update_behavior(behavior=None)
        Change distribution range of moves

    """
    def __init__(self, name):
        """Construct variables for use by Enemy class methods inherited
        from Player.__init__.

        Parameters
        ----------
        name : str
            Name of Enemy
        move_chance : list(list(float, float))
            Distribution range of each move
        """
        Player.__init__(self, name)
        self.move_chance = self.update_behavior()

    def enemy_choice(self):
        """Selects move based on weights move_chance.

        Parameters
        ----------
        None : None

        Returns
        -------
        self.valid_moves[a] : tuple(int, bool)
            Valid move from list of valid_moves
        """
        return random.choices(self.valid_moves,
            weights = self.move_chance)
    
    def update_behavior(self, behavior = None):
        """Change weights move_chance depending on behavior.

        Parameters
        ----------
        enemy : Enemy(Player)
            Instantiated enemy class

        Returns
        -------
        chance : list(float)
            List of weights of each move
        """
        chance = []
        if behavior == "aggressive":
            chance = [
                0.45, # physical attack, 45%
                0.45, # magical attack, 45%
                0.10, # block attack, 10%
                0.00, # consume health potion, 0%
                0.00, # consume magic potion, 0%
                0.00  # skip turn, 0%
            ]
        elif behavior == "defensive":
            chance = [
                0.15, # physical attack, 15%
                0.15, # magical attack, 15%
                0.30, # block attack, 30%
                0.20, # consume health potion, 20%
                0.20, # consume magic potion, 20%
                0.00, # skip turn, 0%
            ]
        elif behavior == "blocky":
            chance = [
                0.00, # physical attack, 0%
                0.00, # magical attack, 0%
                1.00, # block attack, 100%
                0.00, # consume health potion, 0%
                0.00, # consume magic potion, 0%
                0.00  # skip turn, 0%
            ]
        else:
            # default behavior
            chance = [
                0.30, # physical attack, 30%
                0.30, # magical attack, 30%
                0.20, # block attack, 20%
                0.10, # consume health potion, 10%
                0.10, # consume magic potion, 10%
                0.00  # skip turn, 0%
            ]
        if self.mp == 0:
            chance[1] = 0.0 # no longer use magic
        if self.bp == 0:
            chance[2] = 0.0 # no longer use shield
        if self.heal_pot == 0:
            chance[3] = 0.0 # no longer use healing potion
        if self.magic_pot == 0:
            chance[4] = 0.0 # no longer consume magic potion
        return chance

def animated_loading(*texts, end = " ", position = 0, duration = 3):
    """Prints an animated loading string.

    Parameters
    ----------
    *texts : str
        Variable-length input strings
    end : str
        Default string if no arguments passed
    position : int
        Position of animated input string
    duration : int
        Duration of animation

    Returns
    -------
    None : None

    Examples
    --------
    >>> animated_loading("Hello", "world", "!")
    ***** world !
    >>> animated_loading("Hello", "world", "!", position = -1)
    Hello world *
    >>> animated_loading("Hello", "world", "!", position = 1)
    Hello **** !

    Notes
    -----
    In Examples, ``*`` means specified string is affected,
        in actual use all strings will be printed.
    To print numbers, the parameter must be converted to string first
        when calling the function.
    """

    # positive index only
    if position < 0:
        position %= len(texts)

    # merge non-animated strings
    left = ' '.join(
        [texts[i] for i in range(0, position)]
    )
    right = ' '.join(
        [texts[i] for i in range(position + 1, len(texts))]
    )

    # start animation
    symbols = ["\\", "|", "/", "-"]
    for i in range(duration):
        for j in symbols:
            if texts:
                if left and right:
                    print(f"\r{left} {j * len(texts[position])} "
                          + f"{right}", end = "", flush = True)
                elif right:
                    print(f"\r{j * len(texts[position])} {right}",
                          end = "", flush = True)
                elif left:
                    print(f"\r{left} {j * len(texts[position])}",
                          end = "", flush = True)
                else:
                    print(f"\r{j * len(texts[position])}",
                          end = "", flush = True)
            else:
                print(f"\r{j * len(end)}", end="", flush = True)
            time.sleep(0.1)

    # print all strings and newline
    if texts:
        if left and right:
            print(f"\r{left} {texts[position]} {right}")
        elif right:
            print(f"\r{texts[position]} {right}")
        elif left:
            print(f"\r{left} {texts[position]}")
        else:
            print(f"\r{texts[position]}")
    else:
        print(f"\r{end}")

def status_check(player):
    """Prints current status of player.

    Parameters
    ----------
    player : Enemy(Player) or Player
        Instantiated Enemy or Player class

    Returns
    -------
    None : None
    """

    print()
    print(f"Current status of {player.name}")
    animated_loading(f"{'-' * len(f'Current status of {player.name}')}")
    print(f"Health points: {player.hp} / {player.max_hp}")
    print(f"Magic points: {player.mp} / {player.max_mp}")
    print(f"Block points: {player.bp} / {player.max_bp}")
    print(f"Healing potions remaining: {player.heal_pot}")
    print(f"Magic potions remaining: {player.magic_pot}")
    print()
    time.sleep(1)

def result_move(player, enemy, player_is_success, enemy_is_success):
    """Prints the result of selected moves by player and enemy.

    Parameters
    ----------
    player : Enemy(Player) or Player
        Instantiated Enemy or Player class
    enemy : Enemy(Player) or Player
        Instantiated Enemy or Player class
    player_is_success : tuple(int, bool)
        Amount of damage or recovery and info to determine if move by
        player is successful
    enemy_is_success : tuple(int, bool)
        Amount of damage or recovery and info to determine if move
        enemy is successful

    Returns
    -------
    None : None
    """
    # physical attack
    print()
    if player.move[0] == 0:
        if player_is_success[1] == True:
            # failed block
            if enemy.move[0] == 2:
                animated_loading(f"{player.name} breaks through "
                                + f"{enemy.name}\'s block for",
                                f"{str(player_is_success[0])}",
                                "damage!", position = 1)
            else:
                animated_loading(f"{player.name} strikes "
                                + f"{enemy.name} for",
                                f"{str(player_is_success[0])}",
                                "damage!", position = 1)
        # blocked physical attack
        else:
            animated_loading(f"{enemy.name} blocks {player.name}\'s "
                             + "strike for",
                             f"{str(player_is_success[0])}",
                             "damage!", position = 1)
    # magical attack
    elif player.move[0] == 1:
        if player_is_success[1] == True:
            # failed block
            if enemy.move[0] == 2:
                animated_loading(f"{player.name} bursts through "
                                + f"{enemy.name}\'s block for",
                                f"{str(player_is_success[0])}",
                                "damage!", position = 1)
            else:
                animated_loading(f"{player.name} blasts "
                                + f"{enemy.name} for",
                                f"{str(player_is_success[0])}",
                                "damage!", position = 1)
        elif player.mp == 0:
                print(f"{player.name} has no magic left, failing",
                      f"to land an magic blast to {enemy.name}!")
                time.sleep(0.3)
        # blocked magical attack
        else:
            animated_loading(f"{enemy.name} blocks {player.name}\'s "
                             + "magic blast for",
                             f"{str(player_is_success[0])}",
                             "damage!", position = 1)
    # block attack
    elif player.move[0] == 2:
        animated_loading(f"{player.name} braces for impact...")
    # consume health potion
    elif player.move[0] == 3:
        if player_is_success[1] == True and player_is_success[0] != 0:
            animated_loading(f"{player.name} used a health potion, "
                             + "recovering health for",
                             str(player_is_success[0]),
                             "health points!", position = 1)
        elif player_is_success[0] == 0:
            animated_loading(f"{player.name} wasted a health potion, "
                             + "recovering",
                             str(player_is_success[0]),
                             "health points!", position = 1)
        else:
            print(f"{player.name} has no health potions left,",
                  "failing to heal this turn!")
            time.sleep(0.3)
    # consume magic potion
    elif player.move[0] == 4:
        if player_is_success[1] == True and player_is_success[0] != 0:
            animated_loading(f"{player.name} used a magic potion, "
                             + "recovering magic for",
                             str(player_is_success[0]),
                             "magic points!", position = 1)
        elif player_is_success[0] == 0:
            animated_loading(f"{player.name} wasted a magic potion, "
                             + "recovering",
                             str(player_is_success[0]),
                             "magic points!", position = 1)
        else:
            print(f"{player.name} has no magic potions left,",
                  "failing to heal this turn!")
            time.sleep(0.3)
    # skip turn
    else:
        animated_loading(f"{player.name} is...",
                         "doing nothing?", position = -1)

enemy_name = ["Batman", "Gandalf", "Magikarp"]

player1 = Player(input("Input Player Name: ")) # Ask for player name
player2 = Enemy(random.choice(enemy_name)) # Randomly select enemy name

print()
animated_loading(f"Welcome to the arena, {player1.name}!")
print("The crowd is cheering for the battle between "
      + f"{player1.name} and {player2.name}!")
time.sleep(1)
print("Who's gonna win?")
time.sleep(1)
print("Who's gonna lose?")
time.sleep(1)
print("The winner takes all!")
time.sleep(1)
animated_loading(f"{player1.name}",
                 "steps into the arena...")
animated_loading(f"{player2.name}",
                 "also steps in the arena...")
print("The announcer shouts...")
time.sleep(1)
print("'THE BATTLE BEGINS!'")
time.sleep(2)
print()

### Start game
turn = 0
is_running = True
while is_running:
    turn += 1 # increment turn
    print("Turn", turn) # display turn
    print("Choices:") # display choices
    for i, j in player1.valid_moves:
        print("[" + str(i) + "] " + j)
    print()

    # Player chooses move
    while True:
        choice = int(input("Choice: "))
        is_found = [item for item in player1.valid_moves
                    if item[0] == choice]
        if is_found: # list is not empty
            player1.move = is_found[0]
            animated_loading("Valid move. Well chosen!")
            break
        animated_loading("Invalid move. Try again!")
        print()

    # Enemy chooses move
    player2.move = player2.enemy_choice()

    # Randomly select who goes first
    first_turn = random.getrandbits(1) # 0 = Enemy, 1 = Player

    # Variables to hold for successful or failed move
    player1_is_success = (int, bool)
    player2_is_success = (int, bool)

    # Perform chosen moves
    if first_turn:
        print(f"{player1.name} moves first!")
        print()
        time.sleep(1)
        animated_loading(
            f"{player1.name} selects", 
            f"{player1.move[1]}!",
            position = 1
        )
        animated_loading(
            f"{player2.name} selects",
            f"{player2.move[1]}!",
            position = 1
        )
        player1_is_success = player1.perfom_move(player2)
        player2_is_success = player2.perfom_move(player1)
        result_move(player1, player2,
                    player1_is_success, player2_is_success)
        result_move(player2, player1,
                    player2_is_success, player1_is_success)
    else:
        print(f"{player2.name} moves first!")
        animated_loading(
            f"{player2.name} selects",
            f"{player2.move[1]}!",
            position = 1
        )
        animated_loading(
            f"{player1.name} selects",
            f"{player1.move[1]}!",
            position = 1
        )
        player2_is_success = player2.perfom_move(player1)
        player1_is_success = player1.perfom_move(player2)
        result_move(player2, player1,
                    player2_is_success, player1_is_success)
        result_move(player1, player2,
                    player1_is_success, player2_is_success)

    # Decide to update behavior based on enemy or player health
    if (random.getrandbits(1)): # 0 = enemy, 1 = player
        # Change behavior based on player health
        if 75 <= player1.hp <= 100:
            player2.move_chance = player2.update_behavior()
        elif 50 <= player1.hp < 75:
            player2.move_chance = player2.update_behavior("defensive")
            animated_loading(f"{player2.name} is being careful!")
            time.sleep(1)
        elif 0 <= player1.hp < 50:
            player2.move_chance = player2.update_behavior("aggressive")
            animated_loading(f"{player2.name} is no longer hesitant!")
            time.sleep(1)
    else:
        # Change enemy behavior based on enemy health
        if 75 <= player2.hp <= 100:
            player2.move_chance = player2.update_behavior()
        elif 50 <= player2.hp < 75:
            player2.move_chance = player2.update_behavior("aggressive")
            animated_loading(f"{player2.name} is enraged!")
            time.sleep(1)
        elif 0 <= player2.hp < 50:
            player2.move_chance = player2.update_behavior("defensive")
            animated_loading(f"{player2.name} is standing ground!")
            time.sleep(1)

    # Check status of each player
    status_check(player1)
    status_check(player2)

    ### End game
    # Draw
    if player1.hp <= 0 and player2.hp <= 0:
        print()
        animated_loading(f"Both {player1.name} and {player2.name} lay "
                         + "dead on the ground. What a draw!")
        print("The crowd is shocked by the result!")
        animated_loading(
            f"{'-' * len('The crowd is shocked by the result!')}",
            duration = 6
        )
        print("The battle has ended...")
        time.sleep(1)
        print("Everyone has left...")
        time.sleep(1)
        animated_loading(f"Except the corpses of {player1.name} and "
            + f"{player2.name}."
        )
        time.sleep(1)
        print("This is just one of the fights in the arena.")
        time.sleep(1)
        print("There are more battles to come...")
        time.sleep(1)
        print("Better prepare for the next.")
        animated_loading(f"{'-' * len('Better prepare for the next.')}")
        time.sleep(1)
        is_running = False
    # Player 1 wins
    elif player2.hp <= 0:
        print()
        animated_loading(f"Congratulations {player1.name}",
                         "for overpowering", f"{player2.name},",
                         "whose prowess was outmatched up until now!",
                         position = 2)
        print(f"The crowd cheers for the victory of {player1.name}!")
        animated_loading(
            f"{'-' * (37 + len(player1.name))}",
            duration = 6
        )
        print("The battle has ended...")
        time.sleep(1)
        print("Everyone has left...")
        time.sleep(1)
        animated_loading(f"Except {player1.name} and"
            + f"the corpse of {player2.name}."
        )
        time.sleep(1)
        print(f"As {player1.name} contemplates, a realization hits:",
              "this is just one of the fights in the arena.")
        time.sleep(1)
        print("There are more battles to come...")
        time.sleep(1)
        print("Better prepare for the next.")
        animated_loading(f"{'-' * len('Better prepare for the next.')}")
        time.sleep(1)
        is_running = False
    # Player 2 wins
    elif player1.hp <= 0:
        print()
        animated_loading(f"{player2} has won the battle!")
        print(f"The crowd cheers as the corpse of {player1.name}",
            "falls to the ground!")
        animated_loading(
            f"{'-' * (54 + len(player1.name))}",
            duration = 6
        )
        print("The battle has ended...")
        time.sleep(1)
        print("Everyone has left...")
        time.sleep(1)
        animated_loading(f"Except {player2.name} and"
            + f"the corpse of {player1.name}.")
        time.sleep(1)
        print(f"As {player2.name} contemplates, a realization hits:",
              "this is just one of the fights in the arena.")
        time.sleep(1)
        print("There are more battles to come...")
        time.sleep(1)
        print("Better prepare for the next.")
        animated_loading(f"{'-' * len('Better prepare for the next.')}")
        time.sleep(1)
        is_running = False