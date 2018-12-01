from pico2d import *
import stage_state
import main_state
import game_data
import snow
import snow_wall
import math
import game_world
import ally
import game_framework
import end_state

SNOW, STONE_SNOW, ICICLE, BUCKET, A_DOWN, A_UP, S_DOWN, S_UP, W_DOWN, W_UP, D_DOWN, D_UP, R_DOWN, LEFT_BUTTON_DOWN, LEFT_BUTTON_UP, TIME_UP, DEAD = range(17)


key_event_table = {
    (SDL_KEYDOWN, SDLK_a): A_DOWN, (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_s): S_DOWN, (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYDOWN, SDLK_w): W_DOWN, (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN, (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_r): R_DOWN
}
mouse_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LEFT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): LEFT_BUTTON_UP,
}
weapon_key_table = {
    (SDL_KEYDOWN, SDLK_1): SNOW,
    (SDL_KEYDOWN, SDLK_2): STONE_SNOW,
    (SDL_KEYDOWN, SDLK_3): ICICLE,
    (SDL_KEYDOWN, SDLK_4): BUCKET
}


class IdleState:

    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 16

    @staticmethod
    def draw(character):
        character.image.clip_draw(60 * (character.frame // 2), 60 * 0, 60, 60, 300, character.y, 60, 60)


class MoveState:

    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 16
        stage_state.base_x += character.velocity
        character.x += character.velocity


    @staticmethod
    def draw(character):
        if character.velocity > 0:
            character.image.clip_draw(60 * (character.frame//2), 60 * 1, 60, 60, 300, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame//2), 60 * 2, 60, 60, 300, character.y, 60, 60)


class ReloadState:

    @staticmethod
    def enter(character):
        character.frame = 0
        character.timer = 0
        if (character.weapon_type == SNOW and character.snow_stack == character.max_snow_stack) or (character.weapon_type == STONE_SNOW and character.num_ammo[1] == 1) or character.weapon_type == ICICLE :
            character.add_event(TIME_UP)

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 16
        if character.weapon_type == BUCKET:
            if character.timer == character.reload_time*2:
                character.num_ammo[character.weapon_type] += 1
                character.add_event(TIME_UP)
            else:
                character.timer += 1
        else:
            if character.timer == character.reload_time:
                if character.weapon_type == SNOW:
                    if character.num_ammo[0] == 0:
                        character.num_ammo[0] += 1
                    character.snow_stack += 1
                else:
                    character.num_ammo[character.weapon_type] += 1
                character.add_event(TIME_UP)
            else:
                character.timer += 1


    @staticmethod
    def draw(character):
        if character.weapon_type == BUCKET:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 8, 60, 60, 300, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 3, 60, 60, 300, character.y, 60, 60)
        character.draw_reloading_gauge()


class SitState:

    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 16

    @staticmethod
    def draw(character):
        character.image.clip_draw(60 * (character.frame // 2), 60 * 4, 60, 60, 300, character.y, 60, 60)


class MakeWallState:

    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):

        if character.frame == 15:
            find_wall = False

            for sw in game_world.layer_objects(game_world.snow_wall_layer):
                if sw.check_existence(character.x, character.x + 60):
                    sw.strengthen_wall(character.shovel_power)
                    find_wall = True

            if find_wall == False:
                game_world.add_object(snow_wall.SnowWall(character.x, False, character.snow_wall_level, character.shovel_power), game_world.snow_wall_layer)

            character.frame = 0
        else:
            character.frame += 1

    @staticmethod
    def draw(character):
        character.image.clip_draw(60 * (character.frame // 2), 60 * 5, 60, 60, 300, character.y, 60, 60)


class AimState:

    @staticmethod
    def enter(character):
        if character.weapon_type == BUCKET:
            character.add_event(LEFT_BUTTON_UP)
        else:
            character.aim_draw_x, character.aim_draw_y = character.aim_base_x, character.aim_base_y
            character.frame = 0
            character.throw_power = 0


    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        if character.aim_base_y <= character.aim_draw_y:
            character.aim_draw_y = character.aim_base_y - 1
        if character.aim_base_x <= character.aim_draw_x:
            character.aim_draw_x = character.aim_base_x - 1
        character.throw_power = clamp(0, math.sqrt((character.aim_draw_x - character.aim_base_x)**2+(character.aim_base_y - character.aim_draw_y)**2), character.max_throw_power)
        character.throw_degree = math.atan((character.aim_draw_x - character.aim_base_x)/(character.aim_base_y - character.aim_draw_y))

    @staticmethod
    def draw(character):
        if character.weapon_type == BUCKET:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 9, 60, 60, 300, character.y, 60, 60)
        else:
            character.throw_image.clip_composite_draw(40 * 1, 0, 40, 45, clamp(-1.2, character.throw_degree, 0), 'n', 300, character.y + 10, 40, 45)
            character.image.clip_draw(60 * 0, 60 * 6, 60, 60, 300, character.y, 60, 60)
            character.throw_image.clip_composite_draw(40 * 0, 0, 40, 45, clamp(-2, character.throw_degree, -0.2), 'n', 300 - 5, character.y + 10, 40, 45)
            character.throw_image.clip_composite_draw(40 * 2, 0, 40, 45, clamp(-2, character.throw_degree, -0.6) - 30, 'n', 300 - 1, character.y + 15, 40, 45)
            character.arrow_image.rotate_draw(character.throw_degree, 300, 350, 10 + character.throw_power / 12, 30 + character.throw_power / 2)
            if character.weapon_type == SNOW:
                character.throw_objects.clip_composite_draw(40 * (character.snow_stack -1), 0, 40, 45,
                                                            clamp(-2, character.throw_degree, -0.2), 'n', 300 - 5,
                                                            character.y + 10, 40, 45)
            else:
                character.throw_objects.clip_composite_draw(40 * (character.weapon_type+3), 0, 40, 45,
                                                            clamp(-2, character.throw_degree, -0.2), 'n', 300 - 5,
                                                            character.y + 10, 40, 45)


class ThrowState:

    @staticmethod
    def enter(character):
        character.frame = 0
        if character.weapon_type == BUCKET:
            character.timer = 16
        else:
            character.timer = 8

    @staticmethod
    def exit(character):
        character.throw()



    @staticmethod
    def do(character):
        character.timer -= 1
        character.frame += 1
        if character.timer <= 0:
            character.add_event(TIME_UP)

    @staticmethod
    def draw(character):
        if character.weapon_type == BUCKET:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 9, 60, 60, 300, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 7, 60, 60, 300, character.y, 60, 60)



class DeadState:

    @staticmethod
    def enter(character):
        character.frame = 0

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        if character.frame < 127:
            character.frame += 1
        else:
            game_framework.push_state(end_state)


    @staticmethod
    def draw(character):
        character.image.clip_draw(60 * (character.frame // 16), 60 * 10, 60, 60, 300, character.y, 60, 60)


next_state_table = {
    IdleState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: SitState, S_UP: IdleState, W_DOWN: MakeWallState,
                W_UP: IdleState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: IdleState, TIME_UP: IdleState, DEAD:DeadState},
    MoveState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: SitState, S_UP: MoveState, W_DOWN: MakeWallState,
           W_UP: MoveState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: MoveState, TIME_UP: IdleState, DEAD:DeadState},
    ReloadState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: ReloadState, D_UP: ReloadState, S_DOWN: SitState, S_UP: ReloadState, W_DOWN: MakeWallState,
             W_UP: ReloadState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: ReloadState, TIME_UP: IdleState, DEAD:DeadState},
    SitState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: SitState, D_UP: SitState, S_DOWN: SitState, S_UP: IdleState, W_DOWN: MakeWallState,
          W_UP: SitState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: SitState, TIME_UP: IdleState, DEAD:DeadState},
    MakeWallState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: MakeWallState, D_UP: MakeWallState, S_DOWN: SitState, S_UP: MakeWallState,
                W_DOWN: MakeWallState, W_UP: IdleState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: MakeWallState, TIME_UP: IdleState, DEAD:DeadState},
    AimState: {A_DOWN: AimState, D_DOWN: AimState, A_UP: AimState, D_UP: AimState, S_DOWN: AimState, S_UP: AimState, TIME_UP: IdleState,
          W_DOWN: AimState, W_UP: AimState, R_DOWN: AimState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: ThrowState, DEAD:DeadState},
    ThrowState: {A_DOWN: ThrowState, D_DOWN: ThrowState, A_UP: ThrowState, D_UP: ThrowState, S_DOWN: ThrowState, S_UP: ThrowState,
            W_DOWN: ThrowState, W_UP: ThrowState, R_DOWN: ThrowState, LEFT_BUTTON_DOWN: ThrowState, LEFT_BUTTON_UP: ThrowState, TIME_UP: IdleState, DEAD:DeadState},
    DeadState: {A_DOWN: DeadState, D_DOWN: DeadState, A_UP: DeadState, D_UP: DeadState, S_DOWN: DeadState, S_UP: DeadState,
            W_DOWN: DeadState, W_UP: DeadState, R_DOWN: DeadState, LEFT_BUTTON_DOWN: DeadState, LEFT_BUTTON_UP: DeadState, TIME_UP: DeadState, DEAD:DeadState}

}


class Character:

    def __init__(self):
        self.event_que = []
        self.image = load_image('image\\main_character\\main.png')
        self.arrow_image = load_image('image\\main_character\\arrow.png')
        self.throw_image = load_image('image\\main_character\\throw_parts.png')
        self.throw_objects = load_image('image\\main_character\\throw_objects.png')
        self.gauge_bar = load_image('image\\main_character\\gauge_bar.png')
        self.reloading_gauge = load_image('image\\main_character\\reloading_gauge.png')
        self.hp_gauge = load_image('image\\main_character\\hp_gauge.png')
        self.font = load_font('font\\neodgm.ttf')
        self.x, self.y = 300, 30 + 260
        self.cur_state = IdleState
        self.frame = 0
        self.velocity = 0
        self.hp = main_state.Data.get_player_inform(game_data.HP)
        self.max_hp = main_state.Data.get_player_inform(game_data.HP)
        self.reload_time = main_state.Data.get_player_inform(game_data.RELOAD_SPEED)
        self.max_throw_power = main_state.Data.get_player_inform(game_data.THROW_POWER)
        self.snow_wall_level = main_state.Data.get_player_inform(game_data.WALL_LEVEL)
        self.shovel_power = main_state.Data.get_player_inform(game_data.SHOVEL_POWER)
        self.throw_power = 0
        self.aim_base_x, self.aim_base_y = 0, 0
        self.aim_draw_x, self.aim_draw_y = 0, 0
        self.timer = 0
        self.throw_degree = 0
        self.snow_stack = 0
        self.max_snow_stack = main_state.Data.get_player_snow_inform(game_data.MAX_SNOW_STACK)
        self.weapon_type = SNOW
        self.num_ammo = [0, 0, 30, 1]
        self.targeted = False


    def add_event(self, event):
        self.event_que.insert(0, event)




    def change_state(self, state):
        if self.cur_state != state:
            self.cur_state.exit(self)
            self.cur_state = state
            self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)
        self.get_snow()
        self.snow_collision_check()
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(next_state_table[self.cur_state][event])

    def draw(self):
        self.draw_hp_gauge()
        self.cur_state.draw(self)

    def throw(self):
        bias_x = (self.aim_base_x - self.aim_draw_x) / (self.aim_base_x - self.aim_draw_x + self.aim_base_y - self.aim_draw_y)
        bias_y = (self.aim_base_y - self.aim_draw_y) / (self.aim_base_x - self.aim_draw_x + self.aim_base_y - self.aim_draw_y)
        if self.weapon_type == SNOW:
            if self.snow_stack < 3:
                game_world.add_object(snow.SmallSnow(self.x, self.y + 15,
                                            max(self.throw_power * bias_x / 10 + 6 - self.snow_stack * 2, 1),
                                            self.throw_power * bias_y / 10 - self.snow_stack * 2, self.snow_stack),
                                game_world.snow_layer)
            else:
                game_world.add_object(snow.BigSnow(self.x, self.y + 15,
                                                 max(self.throw_power * bias_x / 10 + 6 - self.snow_stack * 2, 1),
                                                 self.throw_power * bias_y / 10 - self.snow_stack * 2,
                                                 self.snow_stack),
                                  game_world.snow_layer)
        elif self.weapon_type == STONE_SNOW:
            game_world.add_object(snow.StoneSnow(self.x, self.y + 15,
                                                 self.throw_power * bias_x / 10 + 6,
                                                 self.throw_power * bias_y / 10),
                                  game_world.snow_layer)
        elif self.weapon_type == ICICLE:
            game_world.add_object(snow.Icicle(self.x, self.y + 15,
                                                 self.throw_power * bias_x / 10 / 2 + 6,
                                                 self.throw_power * bias_y / 10 / 2),
                                  game_world.snow_layer)
        elif self.weapon_type == BUCKET:
            game_world.add_object(snow.SpreadSnow(self.x + 80, self.y), game_world.snow_layer)

        self.num_ammo[self.weapon_type] -= 1
        if self.weapon_type == SNOW:
            self.snow_stack = 0

    def hit_by_snow(self, snow):
        if self.cur_state != DeadState:
            self.hp -= snow.damage
            if self.hp <= 0:
                self.event_que.insert(0, DEAD)
                stage_state.ui.game_fail()

    def hit_by_melee(self, damage):
        if self.cur_state != DeadState:
            self.hp -= damage
            if self.hp <= 0:
                self.event_que.insert(0, DEAD)
                stage_state.ui.game_fail()


    def get_snow(self):
        if self.snow_stack == 0 and self.num_ammo[SNOW] == 0:
            if len(ally.ReloadMan.giving_snow_queue) > 0:
                self.snow_stack += 1
                self.num_ammo[SNOW] += 1
                giver = ally.ReloadMan.giving_snow_queue.pop()
                giver.snow_stack = 0

    def draw_reloading_gauge(self):
        t = 50 * self.timer // self.reload_time//2


        self.reloading_gauge.clip_draw(0, 0, 4, 10, self.x - stage_state.base_x - 27, self.y + 20)
        if self.timer > 0:
            self.reloading_gauge.clip_draw(4, 0, 4, 10, self.x - stage_state.base_x - 25 + t, self.y + 20, t*2, 10)
        self.reloading_gauge.clip_draw(54, 0, 4, 10, self.x - stage_state.base_x - 23 + t*2, self.y + 20)
        self.gauge_bar.draw(self.x - stage_state.base_x, self.y + 20)

    def draw_hp_gauge(self):
        t = 50 * self.hp // self.max_hp // 2

        if self.hp > 0:
            self.hp_gauge.clip_draw(0, 0, 4, 10, self.x - stage_state.base_x - 27, self.y - 50)
            self.hp_gauge.clip_draw(4, 0, 4, 10, self.x - stage_state.base_x - 25 + t, self.y - 50, t * 2, 10)
            self.hp_gauge.clip_draw(54, 0, 4, 10, self.x - stage_state.base_x - 23 + t * 2, self.y - 50)
        self.gauge_bar.draw(self.x - stage_state.base_x, self.y - 50)

    def snow_collision_check(self):
        for snow in game_world.layer_objects(game_world.snow_layer):
            if snow.vx < 0:
                if snow.collision_object(*self.get_hit_box()):
                    self.hit_by_snow(snow)

    def get_hit_box(self):
        if self.cur_state == SitState or self.cur_state == ReloadState:
            return self.x - 10, self.y + 5, self.x + 10, self.y - 25
        else:
            return self.x - 10, self.y + 20, self.x + 10, self.y - 25


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == D_DOWN:
                self.velocity += 3
            elif key_event == D_UP:
                self.velocity -= 3
            elif key_event == A_DOWN:
                self.velocity -= 2
            elif key_event == A_UP:
                self.velocity += 2
            self.add_event(key_event)
        elif (event.type, event.key) in weapon_key_table:
            key_event = weapon_key_table[(event.type, event.key)]
            if main_state.Data.available_weapon[key_event]:
                if key_event != self.weapon_type and (self.cur_state == ReloadState or self.cur_state == AimState):
                    self.add_event(TIME_UP)
                    self.weapon_type = key_event
                else:
                    self.weapon_type = key_event

        elif (event.type, event.button) in mouse_event_table:
            key_event = mouse_event_table[(event.type, event.button)]
            if key_event == LEFT_BUTTON_DOWN:
                if self.num_ammo[self.weapon_type] == 0:
                    key_event = R_DOWN
                else:
                    self.aim_base_x, self.aim_base_y = event.x, 900 - event.y - 1
            self.add_event(key_event)

        elif event.type == SDL_MOUSEMOTION and self.cur_state == AimState:
            self.aim_draw_x, self.aim_draw_y = event.x, 900 - event.y - 1

        return self.velocity


