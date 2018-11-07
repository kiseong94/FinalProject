from pico2d import *
import main_state
import snow
import snow_wall
import math
import game_world

SNOW, STONE_SNOW, ICICLE, BUCKET, A_DOWN, A_UP, S_DOWN, S_UP, W_DOWN, W_UP, D_DOWN, D_UP, R_DOWN, LEFT_BUTTON_DOWN, LEFT_BUTTON_UP, TIME_UP = range(16)


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
        character.image.clip_draw(60 * (character.frame // 2), 60 * 0, 60, 60, 200, character.y, 60, 60)


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
        main_state.base_x += character.velocity
        character.x += character.velocity
        main_state.background.move_ground(character.velocity)
        main_state.background.move_forest(character.velocity)
        main_state.background.move_mountain(character.velocity)

    @staticmethod
    def draw(character):
        if character.velocity > 0:
            character.image.clip_draw(60 * (character.frame//2), 60 * 1, 60, 60, 200, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame//2), 60 * 2, 60, 60, 200, character.y, 60, 60)


class ReloadState:

    @staticmethod
    def enter(character):
        character.frame = 0
        character.timer = 0
        if (character.weapon_type == SNOW and character.snow_stack == 4) or (character.weapon_type == STONE_SNOW and character.ammo[1] == 1) or character.weapon_type == ICICLE :
            character.add_event(TIME_UP)

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 16
        if character.weapon_type == BUCKET:
            if character.timer == character.reload_time*2:
                character.ammo[character.weapon_type] += 1
                character.add_event(TIME_UP)
            else:
                character.timer += 1
        else:
            if character.timer == character.reload_time:
                if character.weapon_type == SNOW:
                    if character.ammo[0] == 0:
                        character.ammo[0] += 1
                    character.snow_stack += 1
                else:
                    character.ammo[character.weapon_type] += 1
                character.add_event(TIME_UP)
            else:
                character.timer += 1




    @staticmethod
    def draw(character):
        if character.weapon_type == BUCKET:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 8, 60, 60, 200, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 3, 60, 60, 200, character.y, 60, 60)


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
        character.image.clip_draw(60 * (character.frame // 2), 60 * 4, 60, 60, 200, character.y, 60, 60)


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
                    sw.strengthen_wall()
                    find_wall = True

            if find_wall == False:
                game_world.add_object(snow_wall.SnowWall(character.x + 20), game_world.snow_wall_layer)

            character.frame = 0
        else:
            character.frame += 1

    @staticmethod
    def draw(character):
        character.image.clip_draw(60 * (character.frame // 2), 60 * 5, 60, 60, 200, character.y, 60, 60)


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
            character.image.clip_draw(60 * (character.frame // 2), 60 * 9, 60, 60, 200, character.y, 60, 60)
        else:
            character.throw_image.clip_composite_draw(40 * 1, 0, 40, 45, clamp(-1.2, character.throw_degree, 0), 'n', 200, character.y + 10, 40, 45)
            character.image.clip_draw(60 * 0, 60 * 6, 60, 60, 200, character.y, 60, 60)
            character.throw_image.clip_composite_draw(40 * 0, 0, 40, 45, clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5, character.y + 10, 40, 45)
            character.throw_image.clip_composite_draw(40 * 2, 0, 40, 45, clamp(-2, character.throw_degree, -0.6) - 30, 'n', 200 - 1, character.y + 15, 40, 45)
            character.arrow_image.rotate_draw(character.throw_degree, 200, 350, 10 + character.throw_power / 12, 30 + character.throw_power / 2)
            if character.weapon_type == SNOW:
                if character.snow_stack == 1:
                    character.throw_objects.clip_composite_draw(40 * 0, 0, 40, 45,
                                                              clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
                                                              character.y + 10, 40, 45)
                elif character.snow_stack == 2:
                    character.throw_objects.clip_composite_draw(40 * 1, 0, 40, 45,
                                                                clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
                                                                character.y + 10, 40, 45)
                elif character.snow_stack == 3:
                    character.throw_objects.clip_composite_draw(40 * 2, 0, 40, 45,
                                                                clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
                                                                character.y + 10, 40, 45)
                elif character.snow_stack == 4:
                    character.throw_objects.clip_composite_draw(40 * 3, 0, 40, 45,
                                                                clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
                                                                character.y + 10, 40, 45)
            elif character.weapon_type == STONE_SNOW:
                character.throw_objects.clip_composite_draw(40 * 4, 0, 40, 45,
                                                            clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
                                                            character.y + 10, 40, 45)
            elif character.weapon_type == ICICLE:
                character.throw_objects.clip_composite_draw(40 * 5, 0, 40, 45,
                                                            clamp(-2, character.throw_degree, -0.2), 'n', 200 - 5,
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
            character.image.clip_draw(60 * (character.frame // 2), 60 * 9, 60, 60, 200, character.y, 60, 60)
        else:
            character.image.clip_draw(60 * (character.frame // 2), 60 * 7, 60, 60, 200, character.y, 60, 60)



class HitState:

    @staticmethod
    def enter(character):
        pass

    @staticmethod
    def exit(character):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        pass


next_state_table = {
    IdleState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: SitState, S_UP: IdleState, W_DOWN: MakeWallState,
                W_UP: IdleState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: IdleState, TIME_UP: IdleState},
    MoveState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: SitState, S_UP: MoveState, W_DOWN: MakeWallState,
           W_UP: MoveState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: MoveState, TIME_UP: IdleState},
    ReloadState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: ReloadState, D_UP: ReloadState, S_DOWN: SitState, S_UP: ReloadState, W_DOWN: MakeWallState,
             W_UP: ReloadState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: ReloadState, TIME_UP: IdleState},
    SitState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: SitState, D_UP: SitState, S_DOWN: SitState, S_UP: IdleState, W_DOWN: MakeWallState,
          W_UP: SitState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: SitState, TIME_UP: IdleState},
    MakeWallState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: MakeWallState, D_UP: MakeWallState, S_DOWN: SitState, S_UP: MakeWallState,
                W_DOWN: MakeWallState, W_UP: IdleState, R_DOWN: ReloadState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: MakeWallState, },
    AimState: {A_DOWN: AimState, D_DOWN: AimState, A_UP: AimState, D_UP: AimState, S_DOWN: AimState, S_UP: AimState, TIME_UP: IdleState,
          W_DOWN: AimState, W_UP: AimState, R_DOWN: AimState, LEFT_BUTTON_DOWN: AimState, LEFT_BUTTON_UP: ThrowState, TIME_UP: IdleState},
    ThrowState: {A_DOWN: ThrowState, D_DOWN: ThrowState, A_UP: ThrowState, D_UP: ThrowState, S_DOWN: ThrowState, S_UP: ThrowState,
            W_DOWN: ThrowState, W_UP: ThrowState, R_DOWN: ThrowState, LEFT_BUTTON_DOWN: ThrowState, LEFT_BUTTON_UP: ThrowState, TIME_UP: IdleState},
    HitState: {},

}


class Character:

    def __init__(self):
        self.event_que = []
        self.image = load_image('image\\main_character\\main.png')
        self.arrow_image = load_image('image\\main_character\\arrow.png')
        self.throw_image = load_image('image\\main_character\\throw_parts.png')
        self.throw_objects = load_image('image\\main_character\\throw_objects.png')
        self.x, self.y = 200, 30 + 260
        self.cur_state = IdleState
        self.frame = 0
        self.velocity = 0
        self.reload_time = 30
        self.throw_power = 0
        self.max_throw_power = 280
        self.aim_base_x, self.aim_base_y = 0, 0
        self.aim_draw_x, self.aim_draw_y = 0, 0
        self.timer = 0
        self.throw_degree = 0
        self.snow_stack = 0
        self.weapon_type = SNOW
        self.ammo = [0, 0, 30, 1]


    def add_event(self, event):
        self.event_que.insert(0, event)


    def change_state(self, state):
        if self.cur_state != state:
            self.cur_state.exit(self)
            self.cur_state = state
            self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.change_state(next_state_table[self.cur_state][event])

    def draw(self):
        self.cur_state.draw(self)

    def throw(self):
        bias_x = (self.aim_base_x - self.aim_draw_x) / (self.aim_base_x - self.aim_draw_x + self.aim_base_y - self.aim_draw_y)
        bias_y = (self.aim_base_y - self.aim_draw_y) / (self.aim_base_x - self.aim_draw_x + self.aim_base_y - self.aim_draw_y)
        if self.weapon_type == SNOW:
            if self.snow_stack < 3:
                game_world.add_object(snow.SmallSnow(200 + main_state.base_x, self.y + 15,
                                            self.throw_power * bias_x / 10 + 6 - self.snow_stack * 2,
                                            self.throw_power * bias_y / 10 - self.snow_stack * 2, self.snow_stack-1),
                                game_world.snow_layer)
            else:
                game_world.add_object(snow.BigSnow(200 + main_state.base_x, self.y + 15,
                                                 self.throw_power * bias_x / 10 + 6 - self.snow_stack * 2,
                                                 self.throw_power * bias_y / 10 - self.snow_stack * 2,
                                                 self.snow_stack - 1),
                                  game_world.snow_layer)
        elif self.weapon_type == STONE_SNOW:
            game_world.add_object(snow.StoneSnow(200 + main_state.base_x, self.y + 15,
                                                 self.throw_power * bias_x / 10 + 6,
                                                 self.throw_power * bias_y / 10),
                                  game_world.snow_layer)
        elif self.weapon_type == ICICLE:
            game_world.add_object(snow.Icicle(200 + main_state.base_x, self.y + 15,
                                                 self.throw_power * bias_x / 10 / 2 + 6,
                                                 self.throw_power * bias_y / 10 / 2),
                                  game_world.snow_layer)
        elif self.weapon_type == BUCKET:
            game_world.add_object(snow.SpreadSnow(200 + 80 + main_state.base_x, self.y), game_world.snow_layer)

        self.ammo[self.weapon_type] -= 1
        if self.weapon_type == SNOW:
            self.snow_stack = 0

    def hit(self):
        pass

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
            if key_event != self.weapon_type and self.cur_state == ReloadState:
                self.add_event(TIME_UP)
                self.weapon_type = key_event
            else:
                self.weapon_type = key_event

        elif (event.type, event.button) in mouse_event_table:
            key_event = mouse_event_table[(event.type, event.button)]
            if key_event == LEFT_BUTTON_DOWN:
                if self.ammo[self.weapon_type] == 0:
                    key_event = R_DOWN
                else:
                    self.aim_base_x, self.aim_base_y = event.x, 900 - event.y - 1
            self.add_event(key_event)

        elif event.type == SDL_MOUSEMOTION and self.cur_state == AimState:
            self.aim_draw_x, self.aim_draw_y = event.x, 900 - event.y - 1




