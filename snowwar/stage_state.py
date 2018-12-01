import random
import json
import os

from pico2d import *

import game_framework
import game_world
import main_character
import back_ground
import main_state
import object_creator
import interface
import ally

name = "StageState"

PIXEL_PER_METER = 40

player = None
background = None
font = None
ui = None
base_x = 0
end_point = 0
start_image = None
obj_creator = None

def enter():
    global player
    global background
    global ui
    global base_x, obj_creator, end_point
    base_x = 0
    player = main_character.Character()
    background = back_ground.Back_Ground()
    background.set_player(player)
    game_world.add_object(player, game_world.player_layer)
    game_world.add_object(background, game_world.back_ground_layer)
    ui = interface.UI()
    obj_creator = object_creator.ObjectCreator()
    obj_creator.create_ally()
    end_point = obj_creator.stage_start(main_state.stage_num) * PIXEL_PER_METER
    ui.game_start()


def exit():
    global player, background, ui
    game_world.clear()



def pause():
    pass


def resume():
    pass


def handle_events():
    global player
    global background
    global ui
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.pop_state()
        else:
            if not(event.type == SDL_MOUSEBUTTONDOWN and 900 - event.y - 1 < 200):
                player.handle_event(event)

            ui.handle_event(event)
            background.handle_event(event)



def update():
    global ui, obj_creator
    for game_object in game_world.all_objects():
        game_object.update()
    obj_creator.update()
    ui.update()


def draw():
    global ui
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    if ui.game_state == interface.FAIL:
        player.draw()
    update_canvas()