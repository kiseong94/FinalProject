from pico2d import *
import stage_state
import game_world
import snow

LEVEL1, LEVEL2, LEVEL3 = range(3)

class SnowWall:
    image = None
    def __init__(self, x, dir, max_hp_level, shovel_power):
        if SnowWall.image == None:
            SnowWall.image = load_image('image\\snows\\snow_wall.png')
        self.y = 260 + 25
        if dir:
            self.x = x - 20
        else:
            self.x = x + 20
        self.cur_state = LEVEL1
        self.hp = shovel_power
        self.max_hp = 5 + max_hp_level*5
        self.shovel_tick = shovel_power
        self.dir = dir
        self.occupied = False


    def draw(self):
        if self.dir:
            self.image.clip_composite_draw(self.cur_state * 40, 0, 40, 50, 0, 'h', self.x - stage_state.base_x, self.y, 40, 50)
        else:
            self.image.clip_composite_draw(self.cur_state * 40, 0, 40, 50, 0, 'n', self.x - stage_state.base_x, self.y, 40, 50)

        #draw_rectangle(*self.get_hit_box())

    def update(self):
        self.collision_snow()

    def strengthen_wall(self, shovel_power):
        self.hp += shovel_power
        if self.max_hp < self.hp:
            self.hp = self.max_hp

        if 3 <= self.hp <= 5:
            self.cur_state = LEVEL2
        elif self.hp > 5:
            self.cur_state = LEVEL3

    def check_existence(self, x1, x2):
        if x1 <= self.x <= x2:
            return True
        else:
            return False

    def collision_snow(self):
        for snow in game_world.layer_objects(game_world.snow_layer):
            if snow.type != 2:
                if snow.collision_object(*self.get_hit_box()):
                    self.hit_by_snow(snow)


    def get_hit_box(self):
        if self.cur_state == LEVEL1:
            return self.x - 15, self.y, self.x + 15, self.y - 25
        elif self.cur_state == LEVEL2:
            return self.x - 15, self.y + 15, self.x + 15, self.y - 25
        elif self.cur_state == LEVEL3:
            return self.x - 15, self.y + 25, self.x + 15, self.y - 25

    def hit_by_snow(self, snow):
        self.hp -= snow.damage
        if self.hp < 1:
            game_world.remove_object(self, game_world.snow_wall_layer)
        elif 1 <= self.hp < 3:
            self.cur_state = LEVEL1
        elif 3 <= self.hp < 6:
            self.cur_state = LEVEL2
        elif self.hp >= 6:
            self.cur_state = LEVEL3

    def hit_by_melee(self, damage):
        self.hp -= damage
        if self.hp < 1:
            game_world.remove_object(self, game_world.snow_wall_layer)
        elif 1 <= self.hp < 3:
            self.cur_state = LEVEL1
        elif 3 <= self.hp < 6:
            self.cur_state = LEVEL2
        elif self.hp >= 6:
            self.cur_state = LEVEL3