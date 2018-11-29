from pico2d import *
import main_state
import stage_state
import random
import snow
import game_world
import snow_wall
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

IDLE, MOVE, AIM, THROW, HIT, DEAD1, DEAD2, DEAD3, SIT, MAKE_WALL, RELOAD, ATTACK = range(12)
LEFT,RIGHT = range(2)

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
            damage = snow.damage
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

####################################################################################################################################
####################################################################################################################################

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
        self.targeted = False

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

####################################################################################################################################
####################################################################################################################################

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
        self.targeted = False

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
            if snow_wall.x >= self.x - self.range and not snow_wall.dir:
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

####################################################################################################################################
####################################################################################################################################

class EnemyType3(Enemy):
    image = None

    def __init__(self, level):
        if EnemyType3.image == None:
            EnemyType3.image = load_image('image\\enemy\\type1\\enemy2_image.png')
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
        self.max_wall_hp = 10
        self.shovel_power = 2
        self.shoveling_time = 30
        self.wall_pos = random.randint(900, 1450)
        self.is_wall_built = False
        self.my_wall = None
        self.money = 70 + level * 70
        self.targeted = False

    def check_wall_build_position(self):
        if not self.is_wall_built and self.x - stage_state.base_x <= self.wall_pos:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def check_duplicated_wall(self):
        if not self.wall_duplication_check():
            self.is_wall_built = True
            return BehaviorTree.SUCCESS
        else:
            if self.x >= 900:
                self.wall_pos -= 200
            else:
                self.is_wall_built = True
        return BehaviorTree.FAIL

    def build_wall(self):
        if self.cur_state != MAKE_WALL:
            self.change_state(MAKE_WALL)
            return BehaviorTree.RUNNING
        else:
            if self.timer >= self.shoveling_time:
                self.timer = 0
                self.create_and_strengthen_wall()
                if self.my_wall.hp >= self.my_wall.max_hp:
                    return BehaviorTree.FAIL
            else:
                self.timer += 1
            return BehaviorTree.RUNNING


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
            if snow_wall.x >= self.x - self.range and not snow_wall.dir:
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

        check_position_node = LeafNode('Check Position', self.check_wall_build_position)
        check_duplication_node = LeafNode('Check Duplication', self.check_duplicated_wall)
        build_wall_node = LeafNode('Build Wall', self.build_wall)

        move_node = LeafNode('Move', self.move)

        attack_node = SequenceNode('Attack')
        attack_node.add_children(set_target_node,attack_target_node)

        make_wall_node = SequenceNode('Make Wall')
        make_wall_node.add_children(check_position_node, check_duplication_node, build_wall_node)

        start_node = SelectorNode('Start Node')
        start_node.add_children(attack_node, make_wall_node, move_node)

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


    def wall_duplication_check(self):
        for w in game_world.layer_objects(game_world.snow_wall_layer):
            if w.dir and self.wall_pos - 60 < w.x - stage_state.base_x + 60 and self.wall_pos + 60 > w.x - stage_state.base_x - 60:
                return True
        return False

    def create_and_strengthen_wall(self):
        if self.my_wall == None:
            self.my_wall = snow_wall.SnowWall(self.x, True, 1, self.shovel_power)
            game_world.add_object(self.my_wall, game_world.snow_wall_layer)
        else:
            self.my_wall.strengthen_wall(self.shovel_power)

####################################################################################################################################
####################################################################################################################################

class EnemyType4(Enemy):
    image = None

    def __init__(self, level):
        if EnemyType4.image == None:
            EnemyType4.image = load_image('image\\enemy\\basic\\enemy_image.png')
        if Enemy.hp_bar == None:
            Enemy.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Enemy.hp_gauge == None:
            Enemy.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        self.hp = level
        self.max_hp = level
        self.armor = 0
        self.velocity = 2
        self.dir = LEFT
        self.cur_state = MOVE
        self.x, self.y = 1800 + stage_state.base_x, 30 + 260
        self.frame = 0
        self.reload_time = 80
        self.aim_time = 30
        self.range = 1200 + (level * 50)
        self.timer = 0
        self.target_position = random.randint(900, 1200) + stage_state.base_x
        self.is_target_position_set = True
        self.snow_stack = 0
        self.build_behavior_tree()
        self.target = None
        self.cover = False
        self.money = 50 + level * 50
        self.targeted = False

    def find_cover(self):
        if not self.cover:
            for wall in game_world.layer_objects(game_world.snow_wall_layer):
                if self.x - 150 <= wall.x <= min(self.x + 150, self.target.x + self.range):
                    self.target_position = wall.x + 50 + random.randint(-10, 30)
                    return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_to_cover(self):
        if self.cur_state == MOVE:
            if self.x >= self.target_position:
                self.dir = LEFT
                self.x -= self.velocity
                if self.x < self.target_position:
                    self.cover = True
                    return BehaviorTree.SUCCESS
            else:
                self.dir = RIGHT
                self.x += self.velocity
                if self.x > self.target_position:
                    self.dir = LEFT
                    self.cover = True
                    return BehaviorTree.SUCCESS
        else:
            self.cur_state = self.change_state(MOVE)
        return BehaviorTree.RUNNING


    def check_range(self):
        for target in game_world.layer_objects(game_world.player_layer):
            if target.x > self.x - self.range:
                self.target = target
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
            self.x -= self.velocity
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_range_node = LeafNode('Check Range', self.check_range)

        find_cover_node = LeafNode('Find Cover', self.find_cover)
        move_to_cover = LeafNode('Move To Cover', self.move_to_cover)

        reload_node = LeafNode('Reload', self.reload)
        set_target_node = LeafNode('Set Target', self.set_target)
        aim_node = LeafNode('Aim', self.aim)
        throw_node = LeafNode('Throw', self.throw)

        set_target_position_node = LeafNode('Set Target Position', self.set_target_position)
        move_to_position_node = LeafNode('Move To Position', self.move_to_position)

        cover_node = SequenceNode('Cover_node')
        attack_node = SequenceNode('Attack_node')
        move_node = SequenceNode('Move_node')

        cover_node.add_children(check_range_node, find_cover_node, move_to_cover)
        attack_node.add_children(check_range_node, reload_node, set_target_node, aim_node, throw_node)
        move_node.add_children(set_target_position_node, move_to_position_node)

        start_node = SelectorNode('Start Node')
        start_node.add_children(cover_node, attack_node, move_node)

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
            if self.dir == LEFT:
                self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
            else:
                self.image.clip_composite_draw(60 * (self.frame // 2), 60 * 0, 60, 60, 0, 'h',self.x - stage_state.base_x, self.y, 60, 60)
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

        def throw_snow(self):
            distance = self.x - self.target.x + random.randint(-200, 100)
            vx = random.randint(15, 20)
            t = distance / vx
            # vy = (28*math.sqrt(t**2 + 100) + 40*t)/50
            vy = t / 5 - (40 / t)
            game_world.add_object(snow.SmallSnow(self.x, self.y + 10, -vx, vy, self.snow_stack), game_world.snow_layer)
            self.snow_stack -= 1