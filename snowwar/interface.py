from pico2d import *
import stage_state
import main_character
import main_state
import game_world
import ally
import game_data

SNOW, STONE_SNOW, ICICLE = range(3)


class UI:
    def __init__(self):
        self.image = load_image('image\\ui\\inform.png')
        self.weapon_image = load_image('image\\ui\\weapon.png')
        self.select_image = load_image('image\\ui\\select.png')
        self.ally_button_image = load_image('image\\ui\\ally_button.png')
        self.font = load_font('font\\neodgm.ttf', 30)
        self.player_inform = load_font('font\\neodgm.ttf', 20)
        self.x, self.y = 800, 100

        self.ally_button_pos = [(1050, 140, '눈 뭉치기 용병 고용'), (1130, 140, '눈 투척 용병 고용'), (1210, 140, '눈 벽 수리 용병'), (1290, 140, '이동식 눈 저장소')]

    def draw(self):
        self.image.draw(self.x, self.y)

        self.player_inform.draw(30, 160, '체 력 LV.%d' % main_state.Data.main_inform[0], (0, 0, 0))
        self.player_inform.draw(30, 130, '장전 속도 LV.%d'% main_state.Data.main_inform[1], (0, 0, 0))
        self.player_inform.draw(30, 100, '던지는 힘 LV.%d'% main_state.Data.main_inform[2], (0, 0, 0))
        self.player_inform.draw(30, 70, '눈벽 보수 LV.%d'% main_state.Data.main_inform[3], (0, 0, 0))
        self.player_inform.draw(30, 40, '눈벽 레벨 LV.%d' % main_state.Data.main_inform[4], (0, 0, 0))

        for i in range(4):
            if main_state.Data.available_weapon[i]:
                if i == 2:
                    self.weapon_image.clip_draw(i * 120, 0, 120, 180, 300 + 300, 95)
                    self.font.draw(300 + 150*i - 10, 30, '%d' % stage_state.player.num_ammo[i], (0, 0, 0))
                else:
                    self.weapon_image.clip_draw(i * 120, 0, 120, 180, 300 + 150*i, 95)
                    self.font.draw(300 - 35 + i*150, 30, '%d / 1' % stage_state.player.num_ammo[i], (0, 0, 0))

        for i in range(4):
            x, y, = self.ally_button_pos[i][0], self.ally_button_pos[i][1]
            self.ally_button_image.draw(x, y)


        self.font.draw(300 + 20, 80, '+%d' % stage_state.player.snow_stack, (255, 255, 0))

        if stage_state.player.weapon_type == main_character.SNOW:
            self.select_image.draw(300, 95)
        elif stage_state.player.weapon_type == main_character.STONE_SNOW:
            self.select_image.draw(300 + 150, 95)
        elif stage_state.player.weapon_type == main_character.ICICLE:
            self.select_image.draw(300 + 300, 95)
        elif stage_state.player.weapon_type == main_character.BUCKET:
            self.select_image.draw(300 + 450, 95)


    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            for i in range(4):
                if main_state.Data.available_ally[i]:
                    mouse_x, mouse_y = event.x, 900 - event.y - 1
                    x, y, = self.ally_button_pos[i][0], self.ally_button_pos[i][1]
                    if x - 35 <= mouse_x <= x + 35 and y - 35 <= mouse_y <= y + 35:
                        self.hire_ally(i)


    def hire_ally(self, type):
        if type == 0:
            game_world.add_object(ally.ReloadMan(), game_world.player_layer)
        if type == 1:
            game_world.add_object(ally.ThrowMan(), game_world.player_layer)
        if type == 2:
            game_world.add_object(ally.ShovelMan(), game_world.player_layer)