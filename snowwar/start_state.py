import random
import json
import os

START, EXIT, NONE = range(3)

from pico2d import *
import game_framework
import main_state

main_image = None
start_button = None
exit_button = None

button = None

def enter():
    global main_image, start_button, exit_button

    main_image = load_image('image\\ui\\start.png')
    start_button = load_image('image\\ui\\start_button.png')
    exit_button = load_image('image\\ui\\exit_button.png')

def exit():
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global button
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, 900 - event.y -1

            if 800 - 200 <= mouse_x <= 800 + 200 and 300 - 50 <= mouse_y <= 300 + 50:
                button = START
            elif 800 - 200 <= mouse_x <= 800 + 200 and 180 - 50 <= mouse_y <= 180 + 50:
                button = EXIT
            else:
                button = NONE
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if button == START:
                game_framework.change_state(main_state)
            elif button == EXIT:
                game_framework.quit()

def update():
    pass


def draw():
    global main_image, start_button, exit_button, button
    clear_canvas()

    main_image.draw(800, 450, 1600, 900)
    if button == START:
        start_button.clip_draw(220 * 1, 56 * 0, 220, 56, 800, 300, 400, 100)
    else:
        start_button.clip_draw(220 * 0, 56 * 0, 220, 56, 800, 300, 400, 100)
    if button == EXIT:
        exit_button.clip_draw(220 * 1, 56 * 0, 220, 56, 800, 180, 400, 100)
    else:
        exit_button.clip_draw(220 * 0, 56 * 0, 220, 56, 800, 180, 400, 100)

    update_canvas()






