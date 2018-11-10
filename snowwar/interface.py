from pico2d import *
import stage_state
import main_character
import main_state
import game_world
import snow

SNOW, STONE_SNOW, ICICLE = range(3)


class UI:
    def __init__(self):
        self.image = load_image('image\\ui\\inform.png')
        self.weapon_image = load_image('image\\ui\\weapon.png')
        self.select_image = load_image('image\\ui\\select.png')
        self.font = load_font('font\\neodgm.ttf', 30)
        self.player_inform = load_font('font\\neodgm.ttf', 20)
        self.x, self.y = 800, 100


    def draw(self):
        self.image.draw(self.x, self.y)

        self.player_inform.draw(30, 150, '체력 LV.1', (0, 0, 0))
        self.player_inform.draw(30, 120, '장전속도 LV.1', (0, 0, 0))
        self.player_inform.draw(30, 90, '던지는힘 LV.1', (0, 0, 0))
        self.player_inform.draw(30, 60, '눈벽보수 LV.1', (0, 0, 0))

        for i in range(4):
            if main_state.available_weapon[i]:
                if i == 2:
                    self.weapon_image.clip_draw(i * 120, 0, 120, 180, 300 + 300, 95)
                    self.font.draw(300 + 150*i - 10, 30, '%d' % stage_state.player.ammo[i], (0, 0, 0))
                else:
                    self.weapon_image.clip_draw(i * 120, 0, 120, 180, 300 + 150*i, 95)
                    self.font.draw(300 - 35 + i*150, 30, '%d / 1' % stage_state.player.ammo[i], (0, 0, 0))


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
