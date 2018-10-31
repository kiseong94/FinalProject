from pico2d import *
import main_state
import game_world
import snow

LEVEL1, LEVEL2, LEVEL3 = range(3)

class SnowWall:
    def __init__(self, x):
        self.image = load_image('snow_wall.png')
        self.x, self.y = x, 260 + 25
        self.cur_state = LEVEL1
        self.hp = 1


    def draw(self):
        if self.cur_state == LEVEL1:
            self.image.clip_draw(0 * 40, 0, 40, 50, self.x - main_state.base_x, self.y)
        elif self.cur_state == LEVEL2:
            self.image.clip_draw(1 * 40, 0, 40, 50, self.x - main_state.base_x, self.y)
        elif self.cur_state == LEVEL3:
            self.image.clip_draw(2 * 40, 0, 40, 50, self.x - main_state.base_x, self.y)

        #draw_rectangle(*self.get_hit_box())

    def update(self):
        self.collision_snow()

    def strengthen_wall(self):
        self.hp += 1

        if self.cur_state == LEVEL1 and self.hp >= 3:
            self.cur_state = LEVEL2
        elif self.cur_state == LEVEL2 and self.hp >= 5:
            self.cur_state = LEVEL3

    def check_existence(self, x1, x2):
        if x1 <= self.x <= x2:
            return True
        else:
            return False

    def collision_snow(self):
        for snow in game_world.layer_objects(game_world.snow_layer):
            if snow.collision_object(*self.get_hit_box()):
                pass

    def get_hit_box(self):
        if self.cur_state == LEVEL1:
            return self.x - 15, self.y, self.x + 15, self.y - 25
        elif self.cur_state == LEVEL2:
            return self.x - 15, self.y + 15, self.x + 15, self.y - 25
        elif self.cur_state == LEVEL3:
            return self.x - 15, self.y + 25, self.x + 15, self.y - 25

