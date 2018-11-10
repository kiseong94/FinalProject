import stage_state
import start_state
import game_framework
import shop

from pico2d import *



name = "MainState"

main_inform = {'hp': 5, 'throw_power': 1, 'shovel_power': 0, 'reload_speed': 1}
available_weapon = [True, False, False, False]

Shop = None
IsShopOpened = False

def enter():
    global Shop
    Shop = shop.Shop()

def exit():
    pass

def pause():
    pass


def resume():
    pass


def handle_events():
    global IsShopOpened
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(start_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.push_state(stage_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            if IsShopOpened:
                IsShopOpened = False
            else:
                IsShopOpened = True



def update():
    pass


def draw():
    global Shop
    clear_canvas()
    if IsShopOpened:
        Shop.draw()
    update_canvas()






