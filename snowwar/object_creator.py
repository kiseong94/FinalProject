from pico2d import *
import stage_state
import game_world
import ally
import enemy
import random
import json

RELOAD_MAN, THROW_MAN, SHOVEL_MAN, STORAGE = range(4)

import main_state

class ObjectCreator:
    def __init__(self):
        self.time = 0
        self.enemy_queue = [(0, 0, 5000)]

    def update(self):
        while stage_state.base_x > self.enemy_queue[0][2]:
            enemy_type, level = self.enemy_queue[0][0], self.enemy_queue[0][1]
            if enemy_type == 0:
                game_world.add_object(enemy.EnemyType1(level), game_world.enemy_layer)
            elif enemy_type == 1:
                game_world.add_object(enemy.EnemyType2(level), game_world.enemy_layer)
            elif enemy_type == 2:
                game_world.add_object(enemy.EnemyType3(level), game_world.enemy_layer)
            elif enemy_type == 3:
                game_world.add_object(enemy.EnemyType4(level), game_world.enemy_layer)
            self.enemy_queue.pop(0)

    def create_ally(self):
        for i in range(main_state.Data.num_ally[RELOAD_MAN]):
            game_world.add_object(ally.ReloadMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[THROW_MAN]):
            game_world.add_object(ally.ThrowMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[SHOVEL_MAN]):
            game_world.add_object(ally.ShovelMan(), game_world.player_layer)
        for i in range(main_state.Data.num_ally[STORAGE]):
            game_world.add_object(ally.Storage(), game_world.player_layer)


    def stage_start(self, stage_num):
        file = open('data.txt', 'r')
        #data_str = file.read()
        enemy_data = json.load(file)
        file.close()
        print(enemy_data)
        stage_distance = enemy_data[stage_num - 1][0]

        for i in range(1, 12):
            enemy_type, level, num = enemy_data[stage_num - 1][i][0], enemy_data[stage_num - 1][i][1], enemy_data[stage_num - 1][i][2]

            for j in range(num):
                distance = random.randint(0, (stage_distance - 10)*stage_state.PIXEL_PER_METER)
                if len(self.enemy_queue) == 0:
                    self.enemy_queue.insert(0, (enemy_type, level, distance))
                else:
                    for k in range(len(self.enemy_queue)):
                        if distance <= self.enemy_queue[k][2]:
                            self.enemy_queue.insert(k, (enemy_type, level, distance))
                            break
        print(self.enemy_queue)

        return stage_distance


