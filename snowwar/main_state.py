import stage_state
import start_state
import game_framework
import game_data
import shop
import math

from pico2d import *

SHOP_BUTTON, START_BUTTON = range(2)

name = "MainState"
Data = None
Shop = None
stage_num = 4
IsShopOpened = False
map = None
stage = None
shop_button_image = None
stage_button_image = None
arrow_image = None
font = None
small_font = None
button_on = None

def enter():
    global Shop
    global Data, map, stage, shop_button_image, font,small_font, arrow_image,stage_button_image
    map = load_image('image\\ui\\map.png')
    stage = load_image('image\\ui\\stage.png')
    shop_button_image = load_image('image\\ui\\shop_button.png')
    stage_button_image = load_image('image\\ui\\stage_button.png')
    arrow_image = load_image('image\\ui\\arrow.png')
    font = load_font('font\\neodgm.ttf',60)
    small_font = load_font('font\\neodgm.ttf', 40)
    Data = game_data.Data()
    Shop = shop.Shop()

def exit():
    pass

def pause():
    pass


def resume():
    pass


def handle_events():
    global IsShopOpened, button_on
    global Shop
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if button_on == SHOP_BUTTON:
                if IsShopOpened:
                    IsShopOpened = False
                else:
                    IsShopOpened = True
            elif button_on == START_BUTTON:
                game_framework.push_state(stage_state)
                IsShopOpened = False

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 900 - event.y - 1
            if math.sqrt((mouse_x - 70)**2 + (mouse_y - 70)**2) <= 100:
                button_on = SHOP_BUTTON
            elif math.sqrt((mouse_x - 1530)**2 + (mouse_y - 70)**2) <= 100:
                button_on = START_BUTTON
            else:
                button_on = None


        if IsShopOpened:
            Shop.handle_event(event)



def update():
    pass


def draw():
    global Shop, map, stage, shop_button_image, font, stage_num, small_font, arrow_image, button_on, stage_button_image
    clear_canvas()
    map.draw(800,450, 1600, 900)

    for i in range(4):
        for j in range(6):
            x, y = 200 + 240*j, 750 - 180*i

            if stage_num > (i*6 + j +1):
                stage.clip_draw(50, 0, 50, 50, 200 + 240 * j, 750 - 180 * i, 120, 120)
                small_font.draw(x - 50, y, 'clear', (255, 255, 255))
            else:

                stage.clip_draw(0, 0, 50, 50, 200 + 240*j, 750 - 180*i, 120, 120)
                if (i*6 + j +1)/10<1:
                    font.draw(x - 40, y, '%2d' % (i * 6 + j + 1), (255, 255, 255))
                else:
                    font.draw(x - 30, y, '%2d'% (i*6 + j +1), (255, 255, 255))
                if stage_num == (i * 6 + j + 1):
                    arrow_image.draw(x, y + 80 , 60, 100)
    if button_on == SHOP_BUTTON:
        shop_button_image.clip_draw(150,0,150,150,70,70,200,200)
    else:
        shop_button_image.clip_draw(0, 0, 150, 150, 70, 70, 200, 200)

    if button_on == START_BUTTON:
        stage_button_image.clip_draw(150,0,150,150,1530,70,200,200)
    else:
        stage_button_image.clip_draw(0, 0, 150, 150,1530, 70, 200, 200)

    if IsShopOpened:
        Shop.draw()
    update_canvas()






