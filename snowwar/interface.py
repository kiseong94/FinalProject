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
        self.x, self.y = 800, 100


    def draw(self):
        self.image.draw(self.x, self.y)

       


    def update(self):
        pass
