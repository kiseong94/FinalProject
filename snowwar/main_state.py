import stage_state
import start_state
import game_framework
import game_data
import shop

from pico2d import *



name = "MainState"
Data = None
Shop = None
IsShopOpened = False

def enter():
    global Shop
    global Data
    Data = game_data.Data()
    Shop = shop.Shop()

def exit():
    pass

def pause():
    pass


def resume():
    pass


def handle_events():
    global IsShopOpened
    global Shop
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
        elif IsShopOpened:
            Shop.handle_event(event)



def update():
    pass


def draw():
    global Shop
    clear_canvas()
    if IsShopOpened:
        Shop.draw()
    update_canvas()






