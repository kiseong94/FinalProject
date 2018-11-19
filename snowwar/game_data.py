
HP, THROW_POWER, RELOAD_SPEED, SHOVEL_POWER, WALL_LEVEL = range(5)

class Data:
    def __init__(self):
        self.main_inform = [1, 1, 1, 1, 1]
        # main_inform = {'hp': 5, 'throw_power': 1, 'shovel_power': 0, 'reload_speed': 1}
        self.available_weapon = [True, False, False, False]
        self.available_ally = [True, False, False, False]
        self.weapon_inform = [[], [], [], []]


    def get_player_inform(self,option):
        if option == HP:
            return 5 + self.main_inform[0]*3
        elif option == THROW_POWER:
            return 280 + self.main_inform[1] * 10
        elif option == RELOAD_SPEED:
            return 50 - self.main_inform[2] * 5
        elif option == SHOVEL_POWER:
            return self.main_inform[3]
        elif option == WALL_LEVEL:
            return self.main_inform[4]