from pico2d import *
import stage_state
import game_world
import ally
import enemy
import random
import game_data

RELOAD_MAN, THROW_MAN, SHOVEL_MAN, STORAGE = range(4)

import main_state

class ObjectCreator:
    def __init__(self):
        self.time = 0

    def update(self):

        if self.time == 0:
            if random.randint(0, 1) == 1:
                game_world.add_object(enemy.EnemyType4(1), game_world.enemy_layer)
            else:
                game_world.add_object(enemy.EnemyType3(1), game_world.enemy_layer)

            self.time = 50
        else:
            self.time -= 1

    def create_ally(self):
        for i in range(main_state.Data.num_ally[RELOAD_MAN]):
            game_world.add_object(ally.ReloadMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[THROW_MAN]):
            game_world.add_object(ally.ThrowMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[SHOVEL_MAN]):
            game_world.add_object(ally.ShovelMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[STORAGE]):
            game_world.add_object(ally.Storage(), game_world.player_layer)


    def stage_start(self,stage_num):


