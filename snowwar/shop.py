Character, Weapon, Ally = range(3)

import main_state
from pico2d import *




class Shop:
    def __init__(self):
        self.font = load_font('font\\neodgm.ttf')
        self.big_font = load_font('font\\neodgm.ttf', 30)
        self.page_image = load_image('image\\shop\\frame.png')
        self.upgrade_button_image = load_image('image\\shop\\upgrade_button.png')
        self.mouse_on_button = None
        self.page_number = 0

        self.page_state = Character
        self.page_select_button_pos = [(300, 630), (470, 630), (640, 630)]


        self.page1_select_image = load_image('image\\shop\\frame1_select_image.png')
        self.page1_button_pos = [(650, 500), (1250, 500), (650, 350), (1250, 350), (650, 200)]
        self.page1_image_pos = [(350, 500, '체 력'), (950, 500, '던지는 힘'), (350, 350, '장전 속도'), (950, 350, '눈벽 보수'), (350, 200, '눈벽 강화')]

        self.page2_select_image = load_image('image\\shop\\frame2_select_image.png')
        self.page2_button_pos = [(1200, 475), (1200, 250)]
        self.page2_image_pos = [[(400, 475, '눈덩이'), (400, 250, '돌을 넣은 눈덩이')],
                                [(400, 475, '고드름'), (400, 250, '눈 양동이')]]


    def draw(self):
        self.page_image.clip_draw(1200*self.page_state, 0, 1200, 700, 800, 450)

        if self.page_state == Character:

            for i in range(5):
                x, y = self.page1_button_pos[i]
                if i == self.mouse_on_button:
                    self.upgrade_button_image.clip_draw(150, 0, 150, 50, x, y)
                else:
                    self.upgrade_button_image.clip_draw(0, 0, 150, 50, x, y)

            for i in range(5):
                x, y, option_name = self.page1_image_pos[i]
                #option_name = option_name + ' %d'
                self.page1_select_image.clip_draw(120*i,0,120,120,x,y)
                self.font.draw(x + 75, y, option_name + ' LV.%d' % main_state.main_inform[i], (0, 0, 0))

        elif self.page_state == Weapon:
            for i in range(2):
                x, y = self.page2_button_pos[i]
                if i == self.mouse_on_button:
                    self.upgrade_button_image.clip_draw(150, 0, 150, 50, x, y)
                else:
                    self.upgrade_button_image.clip_draw(0, 0, 150, 50, x, y)

            if self.page_number == 0:
                for i in range(2):
                    x, y, option_name = self.page2_image_pos[self.page_number][i]
                    # option_name = option_name + ' %d'
                    self.page2_select_image.clip_draw(150 * (self.page_number * 2 + i), 0, 150, 150, x, y)
                    self.font.draw(x + 100, y + 50, option_name, (0, 0, 0))


        x, y = self.page_select_button_pos[0]
        self.big_font.draw(x - 45, y, '능력치', (0, 0, 0))
        x, y = self.page_select_button_pos[1]
        self.big_font.draw(x - 35, y, '무기', (0, 0, 0))
        x, y = self.page_select_button_pos[2]
        self.big_font.draw(x - 35, y, '용병', (0, 0, 0))



    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            for i in range(3):
                x, y = self.page_select_button_pos[i]
                if x - 70 <= mouse_x <= x + 70 and y - 30 <= mouse_y <= y + 30:
                    self.page_state = i

            if self.page_state == Character:
                for i in range(5):
                    x, y = self.page1_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        main_state.main_inform[i] += 1
                        break



        if event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            if self.page_state == Character:
                for i in range(5):
                    x, y = self.page1_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        self.mouse_on_button = i
                        break
                    else:
                        self.mouse_on_button = None


