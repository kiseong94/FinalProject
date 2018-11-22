import random
import json
import os

from pico2d import *

import game_framework
import game_world
import main_character
import back_ground
import enemy
import interface
import ally


name = "StageState"

PIXEL_PER_METER = 40

player = None
background = None
font = None
ui = None
base_x = 0
end_point = 30 * PIXEL_PER_METER
cnt = 10
start_image = None

def enter():
    global player
    global background
    global ui
    global base_x
    base_x = 0
    player = main_character.Character()
    background = back_ground.Back_Ground()
    ui = interface.UI()
    game_world.objects = [[], [], [], [], []]
    game_world.add_object(player, game_world.player_layer)
    game_world.add_object(background, game_world.back_ground_layer)
    game_world.add_object(ally.ReloadMan(), game_world.player_layer)
    for i in range(5):
        game_world.add_object(ally.ThrowMan(), game_world.player_layer)
    game_world.add_object(ally.ShovelMan(), game_world.player_layer)

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
    global cnt
    global ui

    if cnt == 0:
        if random.randint(0, 1) == 1:
            game_world.add_object(enemy.EnemyType1(2), game_world.enemy_layer)
        else:
            game_world.add_object(enemy.EnemyType2(1), game_world.enemy_layer)

        cnt = 50
    else:
        cnt -= 1

    for game_object in game_world.all_objects():
        game_object.update()
    ui.update()


def draw():
    global ui
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    ui.draw()
    update_canvas()






