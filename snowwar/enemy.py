from pico2d import *
import main_state
import random
import snow
import game_world

IDLE, MOVE, AIM, THROW, HIT, DEAD, SIT, MAKE_WALL, RELOAD = range(9)


# initialization code
class Enemy:

    def enter_IDLE(self):
        pass

    def exit_IDLE(self):
        pass

    def do_IDLE(self):
        pass

    def draw_IDLE(self):
        pass



    def enter_MOVE(self):
        self.frame = 0

    def exit_MOVE(self):
        pass

    def do_MOVE(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.velocity


    def draw_MOVE(self):
        self.image.clip_draw(60 * self.frame, 60 * 0, 60, 60, self.x - main_state.base_x, self.y, 60, 60)




    def enter_RELOAD(self):
        self.frame = 0
        self.timer = 0

    def exit_RELOAD(self):
        pass

    def do_RELOAD(self):

        self.frame = (self.frame + 1) % 16
        if self.timer == self.reload_time:
            self.snow_stack += 1
            self.change_state(AIM)
        else:
            self.timer += 1



    def draw_RELOAD(self):
        self.image.clip_draw(60 * (self.frame//2), 60 * 2, 60, 60, self.x - main_state.base_x, self.y, 60, 60)



    def enter_SIT(self):
        pass

    def exit_SIT(self):
        pass

    def do_SIT(self):
        pass

    def draw_SIT(self):
        pass


    def enter_MAKE_WALL(self):
        pass

    def exit_MAKE_WALL(self):
        pass

    def do_MAKE_WALL(self):
        pass

    def draw_MAKE_WALL(self):
        pass


    def enter_AIM(self):
        self.timer = 0
        self.frame = 0


    def exit_AIM(self):
        pass

    def do_AIM(self):
        if self.frame < 16:
            self.frame += self.frame
        if self.timer == 40:
            self.snow_stack += 1
            self.change_state(THROW)
        else:
            self.timer += 1

    def draw_AIM(self):
        self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - main_state.base_x, self.y, 60, 60)


    def enter_THROW(self):
        self.frame = 0


    def exit_THROW(self):
        self.snow_stack = 0
        self.throw_snow()
        self.target_distance -= random.randint(0, 50)


    def do_THROW(self):
        if self.frame == 8:
            self.change_state(IDLE)
        else:
            self.frame += 1

    def draw_THROW(self):
        self.image.clip_draw(60 * (self.frame // 2), 60 * 4, 60, 60, self.x - main_state.base_x, self.y, 60, 60)


    def enter_HIT(self):
        pass

    def exit_HIT(self):
        pass

    def do_HIT(self):
        pass

    def draw_HIT(self):
        pass


    def enter_DEAD(self):
        self.frame = 0

    def exit_DEAD(self):
        pass

    def do_DEAD(self):
        if self.frame < 15:
            self.frame += 1

    def draw_DEAD(self):
        self.image.clip_draw(60 * (self.frame//2), 60 * 1, 60, 60, self.x - main_state.base_x, self.y, 60, 60)

    enter_state = {IDLE: enter_IDLE, MOVE: enter_MOVE, DEAD: enter_DEAD, RELOAD: enter_RELOAD, AIM: enter_AIM, THROW: enter_THROW}
    exit_state = {IDLE: exit_IDLE, MOVE: exit_MOVE, DEAD: exit_DEAD, RELOAD: exit_RELOAD, AIM: exit_AIM, THROW: exit_THROW}
    do_state = {IDLE: do_IDLE, MOVE: do_MOVE, DEAD: do_DEAD, RELOAD: do_RELOAD, AIM: do_AIM, THROW: do_THROW}
    draw_state = {IDLE: draw_IDLE, MOVE: draw_MOVE, DEAD: draw_DEAD, RELOAD: draw_RELOAD, AIM: draw_AIM, THROW: draw_THROW}


    def add_event(self, event):
        self.event_que.insert(0, event)


    def change_state(self, state):
        if self.cur_state != state:
            self.exit_state[self.cur_state](self)
            self.enter_state[state](self)
            self.cur_state = state

    def update(self):
        self.do_state[self.cur_state](self)
        if self.cur_state == IDLE or self.cur_state != DEAD:
            self.select_state()

        if self.cur_state != DEAD:
            for s in game_world.layer_objects(game_world.snow_layer):
                if s.collision_object(self.x - 10, self.y + 25, self.x + 10, self.y - 25):
                    self.change_state(DEAD)

    def draw(self):
        self.draw_state[self.cur_state](self)
        #draw_rectangle(self.x - 10 - main_state.base_x, self.y + 25, self.x + 10 - main_state.base_x, self.y - 25)

    def throw_snow(self):
        distance = self.x - main_state.base_x - 200 + random.randint(-150, 100)
        vx = random.randint(20, 25)
        t = distance/vx
        #vy = (28*math.sqrt(t**2 + 100) + 40*t)/50
        vy = t/5-(40/t)
        game_world.add_object(snow.Snow(self.x, self.y + 10, -vx, vy), game_world.snow_layer)







class Enemy_Basic(Enemy):
    def __init__(self):
        self.image = load_image('enemy_image.png')
        self.velocity = -2
        self.cur_state = MOVE
        self.event_que = []
        self.x, self.y = 1800 + main_state.base_x, 30 + 260
        self.frame = 0
        self.reload_time = 80
        self.throw_power = 0
        self.timer = 0
        self.throw_degree = 0
        self.target_distance = random.randint(800, 1200)
        self.snow_stack = 0


    def select_state(self):
         # 일정 거리에 도달하면 공격상태에 들어감

        if self.x - main_state.base_x <= self.target_distance:
            # 눈덩이가 없다면 눈을 뭉침
            if self.snow_stack == 0:
                self.change_state(RELOAD)
        else:
            self.change_state(MOVE)

