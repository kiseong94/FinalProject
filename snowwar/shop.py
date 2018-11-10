Character, Weapon, Ally = range(3)

from pico2d import *




class Shop:
    def __init__(self):
        self.font = load_font('font\\neodgm.ttf')
        self.frame_image = load_image('image\\shop\\frame.png')
        self.upgrade_button_image = load_image('image\\shop\\upgrade_button.png')
        self.frame1_select_image = load_image('image\\shop\\frame1_select_image.png')
        self.frame_state = Character
        self.frame1_button_pos = [(650, 500), (1250, 500), (650, 350), (1250, 350), (650, 200)]
        self.frame1_image_pos = [(350, 500, '체 력'), (950, 500, '던지는 힘'), (350, 350, '장전 속도'), (950, 350, '눈벽 보수'), (350, 200, '눈벽 강화')]




    def draw(self):
        self.frame_image.draw(800, 450, 1200, 600)
        for x, y in self.frame1_button_pos:
            self.upgrade_button_image.draw(x, y, 150, 50)

        for i in range(5):
            x, y, option_name = self.frame1_image_pos[i]
            self.frame1_select_image.clip_draw(120*i,0,120,120,x,y)
            self.font.draw(x + 75, y, option_name + '%d' ,(0,0,0))




