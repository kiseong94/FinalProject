from pico2d import *
import stage_state
import main_character
import main_state
import game_world
import ally
import game_framework
import game_data

SNOW, STONE_SNOW, ICICLE, START, RUNNING, END = range(6)


class UI:
    def __init__(self):
        self.image = load_image('image\\ui\\inform.png')
        self.weapon_image = load_image('image\\ui\\weapon.png')
        self.weapon_locked_image = load_image('image\\ui\\weapon_locked.png')
        self.select_image = load_image('image\\ui\\select.png')
        self.progress_pointer = load_image('image\\ui\\progress_pointer.png')
        self.stage_progress_bar = load_image('image\\ui\\stage_progress_bar.png')
        self.stage_progress_gauge = load_image('image\\ui\\stage_progress_gauge.png')
        self.ally_button_locked_image = load_image('image\\ui\\ally_button_locked.png')
        self.ally_button_image = load_image('image\\ui\\ally_button.png')
        self.coin_image = load_image('image\\ui\\coin.png')
        self.start_image = load_image('image\\ui\\stage_start_image.png')
        self.font = load_font('font\\neodgm.ttf', 30)
        self.big_font = load_font('font\\neodgm.ttf', 60)
        self.player_inform = load_font('font\\neodgm.ttf', 20)
        self.biggest_font = load_font('font\\neodgm.ttf', 120)
        self.x, self.y = 800, 100

        self.game_state = 0
        self.timer = 0

        self.ally_button_pos = [(1050, 140, '눈 뭉치기 용병 고용'), (1130, 140, '눈 투척 용병 고용'), (1210, 140, '눈 벽 수리 용병'), (1290, 140, '이동식 눈 저장소')]
        self.ally_inform_num = None
        self.mouse_x, self.mouse_y = 0, 0

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
            else:
                self.weapon_locked_image.draw(300+150*i, 95)



        for i in range(4):
            x, y, = self.ally_button_pos[i][0], self.ally_button_pos[i][1]
            if main_state.Data.available_ally[i]:
                self.ally_button_image.clip_draw(i*70, 0, 70, 70, x, y)
            else:
                self.ally_button_locked_image.draw(x, y)


        self.font.draw(300 + 20, 80, '+%d' % stage_state.player.snow_stack, (255, 255, 0))


        if stage_state.player.weapon_type == main_character.SNOW:
            self.select_image.draw(300, 95)
        elif stage_state.player.weapon_type == main_character.STONE_SNOW:
            self.select_image.draw(300 + 150, 95)
        elif stage_state.player.weapon_type == main_character.ICICLE:
            self.select_image.draw(300 + 300, 95)
        elif stage_state.player.weapon_type == main_character.BUCKET:
            self.select_image.draw(300 + 450, 95)

        if self.ally_inform_num != None:
            self.font.draw(self.mouse_x + 20, self.mouse_y, self.ally_button_pos[self.ally_inform_num][2], (0, 0, 0))

        self.draw_stage_progress_bar()

        self.coin_image.draw(1280, 855)
        self.big_font.draw(1350, 850, '%6d' % main_state.Data.cur_money, (0, 0, 0))

        if self.game_state == START:
            self.start_image.draw(800, 450, 1600, 900)
            if self.timer >= 100:
                self.game_state = RUNNING
            elif self.timer >= 50:
                opacity = 1 - (self.timer - 50)/50
                self.start_image.opacify(opacity)
            else:
                self.big_font.draw(650, 450, 'stage 1', (255, 255, 255))
        elif self.game_state == END:
            if self.timer >= 100:
                game_framework.pop_state()
                self.start_image.draw(800, 450, 1600, 900)
            elif self.timer >= 50:
                opacity = (self.timer - 50) / 50
                self.start_image.opacify(opacity)
                self.start_image.draw(800, 450, 1600, 900)
            else:
                self.biggest_font.draw(630, 450, '승리!', (0, 0, 0))




    def update(self):
        self.timer += 1
        if self.game_state == RUNNING and stage_state.base_x >= stage_state.end_point:
            self.game_end()

    def game_start(self):
        self.timer = 0
        self.game_state = START

    def game_end(self):
        self.timer = 0
        self.game_state = END

    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            for i in range(4):
                if main_state.Data.available_ally[i]:
                    mouse_x, mouse_y = event.x, 900 - event.y - 1
                    x, y, = self.ally_button_pos[i][0], self.ally_button_pos[i][1]
                    if x - 35 <= mouse_x <= x + 35 and y - 35 <= mouse_y <= y + 35:
                        self.hire_ally(i)

        elif event.type == SDL_MOUSEMOTION:
            for i in range(4):
                if main_state.Data.available_ally[i]:
                    mouse_x, mouse_y = event.x, 900 - event.y - 1
                    x, y, = self.ally_button_pos[i][0], self.ally_button_pos[i][1]
                    if x - 35 <= mouse_x <= x + 35 and y - 35 <= mouse_y <= y + 35:
                        self.ally_inform_num = i
                        self.mouse_x = mouse_x
                        self.mouse_y = mouse_y
                        break
                    else:
                        self.ally_inform_num = None


    def hire_ally(self, type):
        if type == 0:
            game_world.add_object(ally.ReloadMan(), game_world.player_layer)
        if type == 1:
            game_world.add_object(ally.ThrowMan(), game_world.player_layer)
        if type == 2:
            game_world.add_object(ally.ShovelMan(), game_world.player_layer)
        if type == 3:
            game_world.add_object(ally.Storage(), game_world.player_layer)
        main_state.Data.num_ally[type] += 1

    def draw_stage_progress_bar(self):
        t = 550 * stage_state.base_x // stage_state.end_point // 2
        cur_distance = stage_state.base_x//stage_state.PIXEL_PER_METER
        self.stage_progress_bar.draw(800, 870)
        self.stage_progress_gauge.draw(800 - 550/2 + t, 870-2, t * 2, 6)
        self.progress_pointer.draw(800 - 550/2 + t*2, 870 - 20)
        self.font.draw(800 - 550/2 + t*2 - 10, 870 - 50, '%dm' % cur_distance, (0, 0, 0))


