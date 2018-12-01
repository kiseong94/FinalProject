import random
import json
import os

from pico2d import *

import game_framework
import stage_state
import start_state
import game_world

big_font = None
small_font = None


def enter():
    global big_font, small_font
    big_font = load_font('font\\neodgm.ttf', 60)
    small_font = load_font('font\\neodgm.ttf', 20)

def exit():
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.pop_state()
            game_framework.change_state(start_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_state()


def update():
    pass

def draw():
    global big_font, small_font
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    stage_state.ui.draw()
    big_font.draw(680, 700, '일시정지', (0, 0, 0))
    small_font.draw(690, 600, 'Q 키를 누르면 게임종료', (255, 0, 0))
    update_canvas()








