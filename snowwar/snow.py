from pico2d import *
import main_state
import game_world

FLY, HIT, DESTROY = range(3)


class Snow:

    def draw(self):
        pass

    def update(self):
        if self.cur_state == FLY:
            self.prev_x, self.prev_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.vy = self.vy - 0.4 - 0.1 * self.size
            self.collision_ground()
            self.out_of_sight()
        elif self.cur_state == HIT:
            if self.frame == 16:
                self.delete()
            else:
                self.frame = self.frame + 1

    def collision_ground(self):
        if self.y < 260:
            self.vx, self.vy = 0, 0
            self.cur_state = HIT
            self.frame = 0

    def out_of_sight(self):
        if main_state.base_x > self.x or self.x > main_state.base_x + 1600:
            self.delete()

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if self.y < top and self.prev_x < left < self.x and self.vx > 0:
                self.x = left
                self.cur_state = HIT
                self.frame = 0
                return True
            elif self.y < top and self.x < right < self.prev_x and self.vx < 0:
                self.x = right
                self.cur_state = HIT
                self.frame = 0
                return True

    def delete(self):
        game_world.remove_object(self, game_world.snow_layer)

class SmallSnow(Snow):
    def __init__(self, x, y, vx, vy, size):
        self.image = load_image('snow.png')
        self.destroy_image = load_image('snow_destroy.png')
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.size = size

    def draw(self):
        if self.cur_state == FLY:
            self.image.draw(self.x - main_state.base_x, self.y, 10+(self.size + 1)*2,10+(self.size + 1)*2)
        elif self.cur_state == HIT:
            self.destroy_image.clip_draw((self.frame//2)*30, 0, 30, 30, self.x-main_state.base_x, self.y, 30 + (self.size + 1)*6, 30 + (self.size + 1)*6)



class BigSnow(Snow):
    def __init__(self, x, y, vx, vy, size):
        self.image = load_image('big_snow.png')
        self.destroy_image = load_image('big_snow_destroy.png')
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.size = size

    def draw(self):
        if self.cur_state == FLY:
            self.image.draw(self.x - main_state.base_x, self.y)
        elif self.cur_state == HIT:
            self.destroy_image.clip_draw((self.frame//3)*80, 0, 80, 80, self.x-main_state.base_x, self.y, 80, 80)

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if self.y < top and self.prev_x < left < self.x and self.vx > 0:
                self.x = left
                self.cur_state = HIT
                self.frame = 0

                return True
            elif self.y < top and self.x < right < self.prev_x and self.vx < 0:
                self.x = right
                self.cur_state = HIT
                self.frame = 0
                return True

    def update(self):
        if self.cur_state == FLY:
            self.prev_x, self.prev_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.vy = self.vy - 0.4 - 0.1 * self.size
            self.collision_ground()
            self.out_of_sight()
        elif self.cur_state == HIT:
            if self.frame == 30:
                self.delete()
            else:
                self.frame = self.frame + 1