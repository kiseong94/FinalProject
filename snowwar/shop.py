Character, Weapon, Ally = range(3)

import main_state
from pico2d import *




class Shop:
    def __init__(self):
        self.font = load_font('font\\neodgm.ttf')
        self.page_image = load_image('image\\shop\\frame.png')
        self.upgrade_button_image = load_image('image\\shop\\upgrade_button.png')

        self.page_state = Character
        self.page_select_button_pos = [(300, 630), (470, 630), (640, 630)]


        self.page1_select_image = load_image('image\\shop\\frame1_select_image.png')
        self.page1_button_pos = [(650, 500), (1250, 500), (650, 350), (1250, 350), (650, 200)]
        self.page1_image_pos = [(350, 500, '체 력'), (950, 500, '던지는 힘'), (350, 350, '장전 속도'), (950, 350, '눈벽 보수'), (350, 200, '눈벽 강화')]




    def draw(self):
        self.page_image.clip_draw(1200*self.page_state, 0, 1200, 700, 800, 450)

        if self.page_state == Character:
            
            for x, y in self.page1_button_pos:
                self.upgrade_button_image.draw(x, y, 150, 50)

            for i in range(5):
                x, y, option_name = self.page1_image_pos[i]
                #option_name = option_name + ' %d'
                self.page1_select_image.clip_draw(120*i,0,120,120,x,y)
                self.font.draw(x + 75, y, option_name + ' LV.%d' % main_state.main_inform[i], (0, 0, 0))


    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            for i in range(3):
                x, y = self.page_select_button_pos[i]
                if x - 70 <= event.x <= mouse_x + 70 and y - 30 <= mouse_y <= y + 30:
                    self.page_state = i

