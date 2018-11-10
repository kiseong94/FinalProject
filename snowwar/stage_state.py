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
import start_state

name = "StageState"

player = None
background = None
font = None
ui = None
base_x = 0
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


def exit():
    global player, background, ui
    game_world.clear()



def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.pop_state()
        else:
            player.handle_event(event)



def update():
    global cnt

    if cnt == 0:
        if random.randint(0, 1) == 1:
            game_world.add_object(enemy.EnemyBasic(), game_world.enemy_layer)
        else:
            game_world.add_object(enemy.EnemyType1(), game_world.enemy_layer)

        cnt = 50
    else:
        cnt -= 1

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    global ui
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    ui.draw()
    update_canvas()






