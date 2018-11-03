from pico2d import *
import main_state
import game_world
import snow



class UI:
    def __init__(self):
        self.image = load_image('image\\ui\\inform.png')
        self.weapon_image = load_image('image\\ui\\weapon.png')
        self.select_image = load_image('image\\ui\\select.png')
        self.x, self.y = 800, 100


    def draw(self):
        self.image.draw(self.x, self.y)

        self.weapon_image.clip_draw(0 * 120, 0, 120, 180, 300, 95)
        self.weapon_image.clip_draw(1 * 120, 0, 120, 180, 300 + 150, 95)
        self.weapon_image.clip_draw(2 * 120, 0, 120, 180, 300 + 300, 95)
        if main_state.player


    def update(self):
        pass
