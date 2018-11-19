Character, Weapon, Ally = range(3)

import main_state
from pico2d import *




class Shop:
    def __init__(self):
        self.font = load_font('font\\neodgm.ttf')
        self.big_font = load_font('font\\neodgm.ttf', 30)
        self.sheet_image = load_image('image\\shop\\frame.png')
        self.upgrade_button_image = load_image('image\\shop\\upgrade_button.png')
        self.buy_button_image = load_image('image\\shop\\buy_button.png')
        self.mouse_on_button = None
        self.page_number = 0
        self.page_left_button, self.page_right_button = (275, 350), (1325, 350)

        self.sheet_state = Character
        self.sheet_select_button_pos = [(300, 630), (470, 630), (640, 630)]


        self.sheet1_select_image = load_image('image\\shop\\frame1_select_image.png')
        self.sheet1_button_pos = [(650, 500), (1250, 500), (650, 350), (1250, 350), (650, 200)]
        self.sheet1_image_pos = [(350, 500, '체 력'), (950, 500, '던지는 힘'), (350, 350, '장전 속도'), (950, 350, '눈벽 보수'), (350, 200, '눈벽 강화')]

        self.sheet2_select_image = load_image('image\\shop\\frame2_select_image.png')
        self.sheet2_button_pos = [(1200, 475), (1200, 250)]
        self.sheet2_image_pos = [[(400, 475, '눈덩이'), (400, 250, '돌을 넣은 눈덩이')],
                                [(400, 475, '고드름'), (400, 250, '눈 양동이')]]

        self.sheet3_select_image = None
        self.sheet3_button_pos = [(1200, 475), (1200, 250)]
        self.sheet3_image_pos = [[(400, 475, '눈 뭉치기 용병', '눈을 뭉쳐 줍니다'), (400, 250, '눈 던지기 용병', '눈을 던져 적을 공격합니다')],
                                 [(400, 475, '눈벽 보수 용병', '눈벽을 보수해줍니다'), (400, 250, '이동식 저장소', '눈을 저장합니다')]]


    def draw(self):
        self.sheet_image.clip_draw(1200*self.sheet_state, 0, 1200, 700, 800, 450)

        if self.sheet_state == Character:

            for i in range(5):
                x, y = self.sheet1_button_pos[i]
                if i == self.mouse_on_button:
                    self.upgrade_button_image.clip_draw(150, 0, 150, 50, x, y)
                else:
                    self.upgrade_button_image.clip_draw(0, 0, 150, 50, x, y)

            for i in range(5):
                x, y, option_name = self.sheet1_image_pos[i]
                #option_name = option_name + ' %d'
                self.sheet1_select_image.clip_draw(120 * i, 0, 120, 120, x, y)
                self.font.draw(x + 75, y, option_name + ' LV.%d' % main_state.Data.main_inform[i], (0, 0, 0))

        elif self.sheet_state == Weapon:
            for i in range(2):
                x, y = self.sheet2_button_pos[i]
                if main_state.Data.available_weapon[self.page_number * 2 + i]:
                    if i == self.mouse_on_button:
                        self.upgrade_button_image.clip_draw(150, 0, 150, 50, x, y)
                    else:
                        self.upgrade_button_image.clip_draw(0, 0, 150, 50, x, y)
                else:
                    if i == self.mouse_on_button:
                        self.buy_button_image.clip_draw(150, 0, 150, 50, x, y)
                    else:
                        self.buy_button_image.clip_draw(0, 0, 150, 50, x, y)

            for i in range(2):
                x, y, option_name = self.sheet2_image_pos[self.page_number][i]
                # option_name = option_name + ' %d'
                self.sheet2_select_image.clip_draw(150 * (self.page_number * 2 + i), 0, 150, 150, x, y)
                self.font.draw(x + 100, y + 50, option_name, (0, 0, 0))

            if self.page_number == 0:
                draw_rectangle(self.page_right_button[0] - 25, self.page_right_button[1] - 100,
                               self.page_right_button[0] + 25, self.page_right_button[1] + 100)
            elif self.page_number == 1:
                draw_rectangle(self.page_left_button[0] - 25, self.page_left_button[1] - 100,
                               self.page_left_button[0] + 25, self.page_left_button[1] + 100)

        elif self.sheet_state == Ally:
            for i in range(2):
                x, y = self.sheet3_button_pos[i]
                if main_state.Data.available_weapon[self.page_number * 2 + i]:
                    if i == self.mouse_on_button:
                        self.upgrade_button_image.clip_draw(150, 0, 150, 50, x, y)
                    else:
                        self.upgrade_button_image.clip_draw(0, 0, 150, 50, x, y)
                else:
                    if i == self.mouse_on_button:
                        self.buy_button_image.clip_draw(150, 0, 150, 50, x, y)
                    else:
                        self.buy_button_image.clip_draw(0, 0, 150, 50, x, y)

            for i in range(2):
                x, y, option_name, inform = self.sheet3_image_pos[self.page_number][i]
                # option_name = option_name + ' %d'
                self.sheet2_select_image.clip_draw(150 * (self.page_number * 2 + i), 0, 150, 150, x, y)
                self.font.draw(x + 100, y + 50, option_name, (0, 0, 0))

            if self.page_number == 0:
                draw_rectangle(self.page_right_button[0] - 25, self.page_right_button[1] - 100,
                               self.page_right_button[0] + 25, self.page_right_button[1] + 100)
            elif self.page_number == 1:
                draw_rectangle(self.page_left_button[0] - 25, self.page_left_button[1] - 100,
                               self.page_left_button[0] + 25, self.page_left_button[1] + 100)



        x, y = self.sheet_select_button_pos[0]
        self.big_font.draw(x - 45, y, '능력치', (0, 0, 0))
        x, y = self.sheet_select_button_pos[1]
        self.big_font.draw(x - 35, y, '무기', (0, 0, 0))
        x, y = self.sheet_select_button_pos[2]
        self.big_font.draw(x - 35, y, '용병', (0, 0, 0))



    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            for i in range(3):
                x, y = self.sheet_select_button_pos[i]
                if x - 70 <= mouse_x <= x + 70 and y - 30 <= mouse_y <= y + 30:
                    self.sheet_state = i

            if self.sheet_state == Character:
                for i in range(5):
                    x, y = self.sheet1_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        main_state.Data.main_inform[i] += 1
                        break
            elif self.sheet_state == Weapon:
                for i in range(2):
                    x, y = self.sheet2_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        if main_state.Data.available_weapon[self.page_number * 2 + i]:
                            pass
                        else:
                            main_state.Data.available_weapon[self.page_number * 2 + i] = True
                        break
                    if self.page_number == 0:
                        x, y = self.page_right_button
                        if x - 25 <= mouse_x <= x + 25 and y - 100 <= mouse_y <= y + 100:
                            self.page_number += 1
                    elif self.page_number == 1:
                        x, y = self.page_left_button
                        if x - 25 <= mouse_x <= x + 25 and y - 100 <= mouse_y <= y + 100:
                            self.page_number -= 1
            elif self.sheet_state == Ally:
                for i in range(2):
                    x, y = self.sheet3_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        if main_state.Data.available_weapon[self.page_number * 2 + i]:
                            pass
                        else:
                            main_state.Data.available_weapon[self.page_number * 2 + i] = True
                        break
                    if self.page_number == 0:
                        x, y = self.page_right_button
                        if x - 25 <= mouse_x <= x + 25 and y - 100 <= mouse_y <= y + 100:
                            self.page_number += 1
                    elif self.page_number == 1:
                        x, y = self.page_left_button
                        if x - 25 <= mouse_x <= x + 25 and y - 100 <= mouse_y <= y + 100:
                            self.page_number -= 1




        if event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            if self.sheet_state == Character:
                for i in range(5):
                    x, y = self.sheet1_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        self.mouse_on_button = i
                        break
                    else:
                        self.mouse_on_button = None
            elif self.sheet_state == Weapon:
                for i in range(2):
                    x, y = self.sheet2_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        self.mouse_on_button = i
                        break
                    else:
                        self.mouse_on_button = None
            elif self.sheet_state == Ally:
                for i in range(2):
                    x, y = self.sheet3_button_pos[i]
                    if x - 75 <= mouse_x <= x + 75 and y - 25 <= mouse_y <= y + 25:
                        self.mouse_on_button = i
                        break
                    else:
                        self.mouse_on_button = None



