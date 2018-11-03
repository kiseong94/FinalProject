from pico2d import *
import main_state
import main_character
import game_world
import snow

SNOW, STONE_SNOW, ICICLE = range(3)


class UI:
    def __init__(self):
        self.image = load_image('image\\ui\\inform.png')
        self.weapon_image = load_image('image\\ui\\weapon.png')
        self.select_image = load_image('image\\ui\\select.png')
        self.font = load_font('font\\neodgm.ttf', 30)
        self.x, self.y = 800, 100


    def draw(self):
        self.image.draw(self.x, self.y)

        self.weapon_image.clip_draw(0 * 120, 0, 120, 180, 300, 95)
        self.font.draw(300 + 20, 80, '+%d' % main_state.player.snow_stack, (255, 255, 0))
        self.font.draw(300 - 35, 30, '%d / 1' % main_state.player.ammo[0], (0, 0, 0))

        self.weapon_image.clip_draw(1 * 120, 0, 120, 180, 300 + 150, 95)
        self.font.draw(300 + 150 - 35, 30, '%d / 1' % main_state.player.ammo[1], (0, 0, 0))

        self.weapon_image.clip_draw(2 * 120, 0, 120, 180, 300 + 300, 95)
        self.font.draw(300 + 300 - 10, 30, '%d' % main_state.player.ammo[2], (0, 0, 0))


        if main_state.player.weapon_type == main_character.SNOW:
            self.select_image.draw(300, 95)
        elif main_state.player.weapon_type == main_character.STONE_SNOW:
            self.select_image.draw(300 + 150, 95)
        elif main_state.player.weapon_type == main_character.ICICLE:
            self.select_image.draw(300 + 300, 95)


    def update(self):
        pass
