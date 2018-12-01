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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_state()
            game_framework.pop_state()
            game_framework.change_state(start_state)


def update():
    pass


def draw():
    global big_font, small_font
    clear_canvas()
    stage_state.ui.draw()
    stage_state.player.draw()
    big_font.draw(700, 500, '패배', (255, 0, 0))
    small_font.draw(600, 400, 'space 키를 눌러 메인화면으로 이동', (255, 255, 255))
    update_canvas()








