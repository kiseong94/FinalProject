

class Data:
    def __init__(self):
        self.main_inform = [1, 1, 1, 1, 1]
        # main_inform = {'hp': 5, 'throw_power': 1, 'shovel_power': 0, 'reload_speed': 1}
        self.available_weapon = [True, False, False, False]
        self.weapon_inform = [[], [], [], []]


    def get_player_inform(self,option):
        if option == 'hp':
            return self.main_inform[0]
        elif option == 'throw_power':
            return self.main_inform[1] * 10
        elif option == 'reload_speed':
            return 45 - self.main_inform[2] * 2
        elif option == 'shovel_power':
            return self.main_inform[3]
        elif option == 'wall_level':
            return self.main_inform[4]