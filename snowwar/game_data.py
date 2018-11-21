
SNOW, STONE_SNOW, ICICLE, BUCKET, HP, THROW_POWER, RELOAD_SPEED, SHOVEL_POWER, WALL_LEVEL, MAX_SNOW_STACK, SPLASH_DAMAGE, SPLASH_RANGE = range(12)


class Data:
    def __init__(self):
        self.main_inform = [1, 1, 1, 1, 1]
        # main_inform = {'hp': 5, 'throw_power': 1, 'shovel_power': 0, 'reload_speed': 1}
        self.available_weapon = [True, False, False, False]
        self.available_ally = [True, False, False, False]
        self.weapon_inform = [[], [], [], []]
        self.weapon_level = [1, 0, 0, 0, 0]
        self.ally_level = [1, 0, 0, 0, 0]


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

    def get_player_snow_inform(self, option):
        if option == MAX_SNOW_STACK:
            if self.weapon_level[SNOW] >= 4:
                return 4
            elif self.weapon_level[SNOW] >= 2:
                return 3
            elif self.weapon_level[SNOW] >= 1:
                return 2
        elif option == SPLASH_DAMAGE:
            if self.weapon_level[SNOW] >= 3:
                return 2
        elif option == SPLASH_RANGE:
            if self.weapon_level[SNOW] == 5:
                return True
            else:
                return False


    def get_player_stone_snow_inform(self, option):
        pass