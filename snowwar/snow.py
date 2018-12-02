from pico2d import *
import stage_state
import game_world
import game_data
import main_state

FLY, HIT, DESTROY = range(3)

pi = 3.14

class Snow:
    snow_hit = None


    def load_sound(self):
        if Snow.snow_hit == None:
            Snow.snow_hit = load_wav('sound\\snow_hit2.wav')

    def draw(self):
        pass

    def update(self):
        if self.cur_state == FLY:
            self.prev_x, self.prev_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.vy = self.vy - 0.4
            self.collision_ground()
            self.out_of_sight()
        elif self.cur_state == HIT:
            if self.frame == 16:
                self.delete()
            else:
                self.frame = self.frame + 1

    def collision_ground(self):
        if self.y < 260:
            self.y = 260
            self.vx, self.vy = 0, 0
            self.cur_state = HIT
            self.frame = 0
            self.snow_hit.play()

    def out_of_sight(self):
        if stage_state.base_x > self.x or self.x > stage_state.base_x + 1600:
            self.delete()

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if bottom <= self.y <= top and left <= self.x <= right:
                if self.vx > 0:
                    self.x = left
                else:
                    self.x = right
                self.cur_state = HIT
                self.frame = 0
                return True
            elif self.y < top and self.prev_x < left < self.x and self.vx > 0:
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
    image = None
    destroy_image = None
    def __init__(self, x, y, vx, vy, size):
        if SmallSnow.image == None:
            SmallSnow.image = load_image('image\\snows\\snow.png')
        if SmallSnow.destroy_image == None:
            SmallSnow.destroy_image = load_image('image\\snows\\snow_destroy.png')
        self.load_sound()
        self.damage = size
        self.armor_piercing_point = 0
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.size = size
        self.type = 0

    def draw(self):
        if self.cur_state == FLY:
            self.image.draw(self.x - stage_state.base_x, self.y, 10+(self.size - 1)*4,10+(self.size - 1)*4)
        elif self.cur_state == HIT:
            self.destroy_image.clip_draw((self.frame//2)*30, 0, 30, 30, self.x-stage_state.base_x, self.y, 30 + (self.size - 1)*12, 30 + (self.size - 1)*12)



class BigSnow(Snow):
    image = None
    destroy_image = None
    def __init__(self, x, y, vx, vy, size):
        if BigSnow.image == None:
            BigSnow.image = load_image('image\\snows\\big_snow.png')
        if BigSnow.destroy_image == None:
            BigSnow.destroy_image = load_image('image\\snows\\big_snow_destroy.png')
        self.load_sound()
        self.damage = size
        self.armor_piercing_point = 0
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.size = size
        self.type = 0

        self.splash_damage = main_state.Data.get_player_snow_inform(game_data.SPLASH_DAMAGE)
        self.wide_splash_range = main_state.Data.get_player_snow_inform(game_data.SPLASH_RANGE)

    def draw(self):
        if self.cur_state == FLY:
            self.image.draw(self.x - stage_state.base_x, self.y, 10 + (self.size - 1)*6, 10 + (self.size - 1)*6)
        elif self.cur_state == HIT:
            if self.wide_splash_range:
                self.destroy_image.clip_draw((self.frame // 3) * 80, 0, 80, 80, self.x - stage_state.base_x, self.y,
                                             100 + (self.size - 1) * 6, 100 + (self.size - 1) * 6)
            else:
                self.destroy_image.clip_draw((self.frame//3)*80, 0, 80, 80, self.x-stage_state.base_x, self.y, 80 + (self.size - 1)*6, 80 + (self.size - 1)*6)

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if bottom <= self.y <= top and left <= self.x <= right:
                if self.vx > 0:
                    self.x = left
                else:
                    self.x = right
                self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True
            elif self.y < top and self.prev_x < left < self.x and self.vx > 0:
                self.x = left
                self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True
            elif self.y < top and self.x < right < self.prev_x and self.vx < 0:
                self.x = right
                self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True
        elif self.cur_state == HIT and self.frame == 15:
            self.damage = self.splash_damage
            snow_left, snow_top, snow_right, snow_bottom = self.get_hit_box()
            if snow_left <= right and snow_right >= left and snow_bottom <= top and snow_top >= bottom:
                return True

    def update(self):
        if self.cur_state == FLY:
            self.prev_x, self.prev_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.vy = self.vy - 0.4
            self.collision_ground()
            self.out_of_sight()
        elif self.cur_state == HIT:
            if self.frame == 30:
                self.delete()
            else:
                self.frame = self.frame + 1

    def get_hit_box(self):
        if self.wide_splash_range:
            return self.x - 30, self.y + 30, self.x + 60, self.y - 40
        else:
            return self.x - 20, self.y + 10, self.x + 40, self.y - 40

class StoneSnow(Snow):
    image = None
    destroy_image = None
    def __init__(self, x, y, vx, vy):
        if StoneSnow.image == None:
            StoneSnow.image = load_image('image\\snows\\stone_snow.png')
        if StoneSnow.destroy_image == None:
            StoneSnow.destroy_image = load_image('image\\snows\\snow_destroy.png')
        self.load_sound()
        self.damage = main_state.Data.get_player_stone_snow_inform(game_data.DAMAGE)
        self.critical_chance = main_state.Data.get_player_stone_snow_inform(game_data.CRITICAL_CHANCE)
        self.piercing_num = main_state.Data.get_player_stone_snow_inform(game_data.PIERCING_NUM)
        self.armor_piercing_point = 0
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.type = 1

    def draw(self):
        if self.cur_state == FLY:
            self.image.draw(self.x - stage_state.base_x, self.y)
        elif self.cur_state == HIT:
            self.destroy_image.clip_draw((self.frame//3)*30, 0, 30, 30, self.x-stage_state.base_x, self.y)

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if bottom <= self.y <= top and left <= self.x <= right:
                if self.vx > 0:
                    self.x = left
                else:
                    self.x = right
                self.piercing_num -= 1
                if self.piercing_num == 0:
                    self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True
            elif self.y < top and self.prev_x < left < self.x and self.vx > 0:
                self.x = left
                self.piercing_num -= 1
                if self.piercing_num == 0:
                    self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True
            elif self.y < top and self.x < right < self.prev_x and self.vx < 0:
                self.x = right
                self.piercing_num -= 1
                if self.piercing_num == 0:
                    self.cur_state = HIT
                self.snow_hit.play()
                self.frame = 0
                return True

class Icicle(Snow):
    image = None
    destroy_image = None
    def __init__(self, x, y, vx, vy):
        if Icicle.image == None:
            Icicle.image = load_image('image\\snows\\icicle.png')
        if Icicle.destroy_image == None:
            Icicle.destroy_image = load_image('image\\snows\\snow_destroy.png')
        self.load_sound()
        self.damage = main_state.Data.get_player_icicle_inform(game_data.DAMAGE)
        self.armor_piercing_point = main_state.Data.get_player_icicle_inform(game_data.PIERCING_ARMOR)
        self.destroy_armor = main_state.Data.get_player_icicle_inform(game_data.DESTROY_ARMOR)
        self.piercing_wall = main_state.Data.get_player_icicle_inform(game_data.PIERCING_WALL)
        self.x, self.y = x, y
        self.prev_x, self.prev_y = x, y
        self.vx, self.vy = vx, vy
        self.cur_state = FLY
        self.frame = 0
        self.degree = 0
        self.type = 2

    def draw(self):
        if self.cur_state == FLY:
            self.image.rotate_draw(self.degree, self.x - stage_state.base_x, self.y)
        elif self.cur_state == HIT:
            self.destroy_image.clip_draw((self.frame//3)*30, 0, 30, 30, self.x-stage_state.base_x, self.y)

    def update(self):
        if self.cur_state == FLY:
            self.prev_x, self.prev_y = self.x, self.y
            self.x += self.vx
            self.y += self.vy
            self.vy = self.vy - 0.4
            self.degree += (2 * pi) / 10
            self.collision_ground()
            self.out_of_sight()
        elif self.cur_state == HIT:
            self.delete()

    def collision_object(self, left, top, right, bottom):
        if self.cur_state == FLY:
            if self.y < top and self.prev_x < left < self.x and self.vx > 0:
                self.snow_hit.play()
                self.delete()
                return True
            elif self.y < top and self.x < right < self.prev_x and self.vx < 0:
                self.snow_hit.play()
                self.delete()
                return True


class SpreadSnow(Snow):
    destroy_image = None
    def __init__(self, x, y):
        if SpreadSnow.destroy_image == None:
            SpreadSnow.destroy_image = load_image('image\\snows\\spread_snow.png')
        self.load_sound()
        self.x, self.y = x, y
        self.damage = main_state.Data.get_player_bucket_inform(game_data.DAMAGE)
        self.armor_piercing_point = 0
        self.vx = 1
        self.cur_state = HIT
        self.frame = 0
        self.type = 3
        self.wide_splash = main_state.Data.get_player_bucket_inform(game_data.SPLASH_RANGE)

    def draw(self):
        if self.wide_splash:
            self.destroy_image.clip_draw((self.frame // 3) * 120, 0, 120, 60, self.x - stage_state.base_x + 15, self.y + 5, 150, 70)
        else:
            self.destroy_image.clip_draw((self.frame//3)*120, 0, 120, 60, self.x-stage_state.base_x, self.y)
        #draw_rectangle(*self.get_hit_box())

    def collision_object(self, left, top, right, bottom):
        snow_left, snow_top, snow_right, snow_bottom = self.get_hit_box()
        if snow_left <= right and snow_right >= left and snow_bottom <= top and snow_top >= bottom:
            return True

    def update(self):
        if self.frame == 30:
            self.delete()
        else:
            self.frame = self.frame + 1

    def get_hit_box(self):
        if self.wide_splash:
            if 0 == self.frame:
                return self.x - 50, self.y + 30, self.x - 10, self.y - 30
            elif 10 == self.frame:
                return self.x - 10, self.y + 30, self.x + 30, self.y - 30
            elif 20 == self.frame:
                return self.x + 30, self.y + 30, self.x + 70, self.y - 30
            else:
                return 0, 0, 0, 0
        else:
            if 0 == self.frame:
                return self.x - 60, self.y + 30, self.x - 20, self.y - 30
            elif 10 == self.frame:
                return self.x - 20, self.y + 30, self.x + 20, self.y - 30
            elif 20 == self.frame:
                return self.x + 20, self.y + 30, self.x + 60, self.y - 30
            else:
                return 0, 0, 0, 0
