
SNOW, STONE_SNOW, ICICLE, BUCKET, HP, THROW_POWER, RELOAD_SPEED, SHOVEL_POWER, WALL_LEVEL, MAX_SNOW_STACK,\
SPLASH_DAMAGE, SPLASH_RANGE, PIERCING_NUM, DAMAGE, CRITICAL_CHANCE, PIERCING_ARMOR, PIERCING_WALL, DESTROY_ARMOR,\
FAST_RELOAD, KNOW_BACK = range(20)


class Data:
    def __init__(self):
        self.main_inform = [1, 1, 1, 1, 1]
        # main_inform = {'hp': 5, 'throw_power': 1, 'shovel_power': 0, 'reload_speed': 1}
        self.available_weapon = [True, False, False, False]
        self.available_ally = [True, False, False, False]
        self.weapon_inform = [[], [], [], []]
        self.weapon_level = [1, 0, 0, 0, 0]
        self.ally_level = [1, 0, 0, 0, 0]
        self.num_ally = [0, 0, 0, 0]
        self.stage_num = 1
        self.total_money = 0
        self.cur_money = 0


    def get_player_inform(self,option):
        if option == HP:
            return 5 + self.main_inform[0]*3
        elif option == THROW_POWER:
            return 240 + self.main_inform[1] * 12
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
        if option == PIERCING_NUM:
            if self.weapon_level[STONE_SNOW] >= 4:
                return 3
            else:
                return 2
        elif option == DAMAGE:
            if self.weapon_level[STONE_SNOW] >= 2:
                return 2
            else:
                return 1
        elif option == CRITICAL_CHANCE:
            if self.weapon_level[STONE_SNOW] >= 5:
                return 30
            elif self.weapon_level[STONE_SNOW] >= 3:
                return 15
            else:
                return 0

    def get_player_icicle_inform(self, option):
        if option == PIERCING_ARMOR:
            return 1
        elif option == DAMAGE:
            if self.weapon_level[ICICLE] >= 4:
                return 3
            elif self.weapon_level[ICICLE] >= 3:
                return 2
            else:
                return 1
        elif option == PIERCING_WALL:
            if self.weapon_level[ICICLE] >= 2:
                return True
            else:
                return False
        elif option == DESTROY_ARMOR:
            if self.weapon_level[ICICLE] >= 5:
                return 1
            else:
                return 0


    def get_player_bucket_inform(self, option):
        if option == FAST_RELOAD:
            if self.weapon_level[BUCKET] >= 2:
                return True
            else:
                return False
        elif option == KNOW_BACK:
            if self.weapon_level[BUCKET] >= 3:
                return True
            else:
                return False
        elif option == DAMAGE:
            if self.weapon_level[BUCKET] >= 4:
                return 2
            else:
                return 1
        elif option == SPLASH_RANGE:
            if self.weapon_level[BUCKET] >= 5:
                return True
            else:
                return False