from pico2d import *
import main_state
import stage_state
import random
import snow
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

IDLE, MOVE, AIM, THROW, HIT, DEAD1, DEAD2, DEAD3, SIT, MAKE_WALL, RELOAD, ATTACK = range(12)


# initialization code
class Enemy:
    hp_gauge = None
    hp_bar = None

    def change_state(self, state):
        self.cur_state = state
        self.timer = 0
        self.frame = 0

    def throw_snow(self):
        distance = self.x - self.target.x + random.randint(-150, 100)
        vx = random.randint(20, 25)
        t = distance/vx
        #vy = (28*math.sqrt(t**2 + 100) + 40*t)/50
        vy = t/5-(40/t)
        game_world.add_object(snow.SmallSnow(self.x, self.y + 10, -vx, vy, self.snow_stack), game_world.snow_layer)
        self.snow_stack -= 1

    def out_of_sight(self):
        if stage_state.base_x > self.x or self.x > stage_state.base_x + 1600:
            return True

    def delete(self):
        game_world.remove_object(self, game_world.enemy_layer)

    def snow_collision_check(self):
        for snow in game_world.layer_objects(game_world.snow_layer):
            if snow.vx > 0:
                if snow.collision_object(*self.get_hit_box()):
                    self.hit_by_snow(snow)


    def get_hit_box(self):
        if self.cur_state == RELOAD:
            return self.x - 10, self.y + 5, self.x + 10, self.y - 25
        else:
            return self.x - 10, self.y + 20, self.x + 10, self.y - 25

    def hit_by_snow(self, snow):

        if snow.type == 1:
            if snow.critical_chance >= random.randint(0, 100):
                damage = snow.damage * 2
            else:
                damage = snow.damage
        elif snow.type == 2:
            self.armor = min(snow.destroy_armor - self.armor, 0)

        else:
            damage = snow.damage

        self.hp -= min(snow.armor_piercing_point - self.armor, 0) + damage

        if self.hp <= 0:
            if snow.type == 0 or snow.type == 3:
                self.change_state(DEAD1)
            elif snow.type == 1:
                self.change_state(DEAD2)
            elif snow.type == 2:
                self.change_state(DEAD3)
            main_state.Data.cur_money += self.money
            main_state.Data.total_money += self.money



    def draw_hp_gauge(self):
        t = 30 * self.hp // self.max_hp // 2

        self.hp_bar.draw(self.x - stage_state.base_x, self.y - 50)
        if self.hp > 0:
            self.hp_gauge.draw(self.x - stage_state.base_x - 15 + t, self.y - 50, t * 2, 5)

class EnemyType1(Enemy):
    image = None

    def __init__(self, level):
        if EnemyType1.image == None:
            EnemyType1.image = load_image('image\\enemy\\basic\\enemy_image.png')
        if Enemy.hp_bar == None:
            Enemy.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Enemy.hp_gauge == None:
            Enemy.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        self.hp = level
        self.max_hp = level
        self.armor = 0
        self.velocity = -2
        self.cur_state = MOVE
        self.x, self.y = 1800 + stage_state.base_x, 30 + 260
        self.frame = 0
        self.reload_time = 80
        self.aim_time = 30
        self.range = 800 + (level * 50)
        self.timer = 0
        self.target_position = random.randint(800 + level*100, 1200 + level * 100) + stage_state.base_x
        self.is_target_position_set = True
        self.snow_stack = 0
        self.build_behavior_tree()
        self.target = None
        self.money = 50 + level * 50

    def check_range(self):
        for target in game_world.layer_objects(game_world.player_layer):
            if target.x > self.x - self.range:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def reload(self):
        if self.snow_stack == 1:
            return BehaviorTree.SUCCESS
        else:
            if self.cur_state != RELOAD:
                self.change_state(RELOAD)
            else:
                if self.timer >= self.reload_time:
                    self.snow_stack = 1
                else:
                    self.timer += 1
            return BehaviorTree.RUNNING

    def set_target(self):
        for target in game_world.layer_objects(game_world.player_layer):
            if target.cur_state != DEAD1 and target.cur_state != DEAD2 and target.cur_state != DEAD3:
                if target.x > self.x - self.range:
                    self.target = target
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def aim(self):
        if self.cur_state != AIM:
            self.change_state(AIM)
            return BehaviorTree.RUNNING
        else:
            if self.timer >= self.aim_time:
                return BehaviorTree.SUCCESS
            else:
                self.timer += 1
                return BehaviorTree.RUNNING

    def throw(self):
        if self.cur_state != THROW:
            self.change_state(THROW)
            return BehaviorTree.RUNNING
        else:
            if self.frame >= 7:
                self.throw_snow()
                return BehaviorTree.SUCCESS
            else:
                self.timer += 1
                return BehaviorTree.RUNNING


    def set_target_position(self):
        if self.is_target_position_set == False:
            self.target_position = self.x - random.randint(0, 50)
            self.is_target_position_set = True

        return BehaviorTree.SUCCESS

    def move_to_position(self):
        if self.x >= self.target_position:
            self.x += self.velocity
            return BehaviorTree.RUNNING
        else:
            self.is_target_position_set = False
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_range_node = LeafNode('Check Range', self.check_range)
        reload_node = LeafNode('Reload', self.reload)
        set_target_node = LeafNode('Set Target', self.set_target)
        aim_node = LeafNode('Aim', self.aim)
        throw_node = LeafNode('Throw', self.throw)

        set_target_position_node = LeafNode('Set Target Position', self.set_target_position)
        move_to_position_node = LeafNode('Move To Position', self.move_to_position)

        attack_node = SequenceNode('Attack_node')
        move_node = SequenceNode('Move_node')

        attack_node.add_children(check_range_node, reload_node, set_target_node, aim_node, throw_node)
        move_node.add_children(set_target_position_node, move_to_position_node)

        start_node = SelectorNode('Start Node')
        start_node.add_children(attack_node, move_node)

        self.bt = BehaviorTree(start_node)

    def update(self):
        if self.cur_state != DEAD1 and self.cur_state != DEAD2 and self.cur_state != DEAD3:
            self.bt.run()
            self.snow_collision_check()
            self.frame = (self.frame + 1) % 16
        else:
            if self.out_of_sight():
                self.delete()
            if self.frame < 15:
                self.frame += 1

    def draw(self):
        if self.cur_state == MOVE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == RELOAD:
            self.image.clip_draw(60 * (self.frame//2), 60 * 2, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == AIM:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == THROW:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 4, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD2:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 5, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD3:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 6, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        if self.cur_state != DEAD1 and self.cur_state != DEAD2 and self.cur_state != DEAD3:
            self.draw_hp_gauge()

class EnemyType2(Enemy):
    image = None

    def __init__(self, level):
        if EnemyType2.image == None:
            EnemyType2.image = load_image('image\\enemy\\type1\\enemy2_image.png')
        if Enemy.hp_bar == None:
            Enemy.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Enemy.hp_gauge == None:
            Enemy.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        self.hp = 1 + level
        self.max_hp = 1 + level
        self.armor = 0
        self.velocity = -2
        self.cur_state = MOVE
        self.x, self.y = 1800 + stage_state.base_x, 30 + 260
        self.range = 60
        self.frame = 0
        self.timer = 0
        self.build_behavior_tree()
        self.target = None
        self.money = 70 + level*70

    def move(self):
        if self.cur_state != MOVE:
            self.change_state(MOVE)
        else:
            self.x += self.velocity

        return BehaviorTree.SUCCESS

    def set_target(self):
        for target in game_world.layer_objects(game_world.player_layer):
            if target.x >= self.x - self.range:
                self.target = target
                return BehaviorTree.SUCCESS
        for snow_wall in game_world.layer_objects(game_world.snow_wall_layer):
            if snow_wall.x >= self.x - self.range:
                self.target = snow_wall
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def attack_target(self):
        if self.cur_state != ATTACK:
            self.cur_state = ATTACK
            return BehaviorTree.RUNNING
        else:
            if self.timer >= 16:
                self.target.hit_by_melee(1)
                self.timer = 0
                return BehaviorTree.SUCCESS
            else:
                self.timer += 1
                return BehaviorTree.RUNNING


    def build_behavior_tree(self):

        set_target_node = LeafNode('Set Target', self.set_target)
        attack_target_node = LeafNode('Attack', self.attack_target)

        move_node = LeafNode('Move', self.move)

        attack_node = SequenceNode('Attack')
        attack_node.add_children(set_target_node,attack_target_node)

        start_node = SelectorNode('Start Node')
        start_node.add_children(attack_node, move_node)

        self.bt = BehaviorTree(start_node)

    def update(self):
        if self.cur_state != DEAD1 and self.cur_state != DEAD2 and self.cur_state != DEAD3:
            self.bt.run()
            self.snow_collision_check()
            self.frame = (self.frame + 1) % 16
        else:
            if self.out_of_sight():
                self.delete()
            if self.frame < 15:
                self.frame += 1

    def draw(self):
        if self.cur_state == MOVE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == ATTACK:
            self.image.clip_draw(60 * (self.frame//2), 60 * 2, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD2:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 5, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD3:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 6, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        if self.cur_state != DEAD1 and self.cur_state != DEAD2 and self.cur_state != DEAD3:
            self.draw_hp_gauge()