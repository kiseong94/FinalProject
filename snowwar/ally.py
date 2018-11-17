from pico2d import *
import main_state
import stage_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import snow
import game_world

IDLE, MOVE, AIM, THROW, HIT, DEAD1, DEAD2, DEAD3, SIT, MAKE_WALL, RELOAD, ATTACK = range(12)


# initialization code
class ReloadMan:
    image = None
    giving_snow_queue = []
    def __init__(self):
        if ReloadMan.image == None:
            ReloadMan.image = load_image('image\\ally\\reload_man\\temp.png')
        self.velocity = 2
        self.cur_state = IDLE
        self.event_que = []
        self.x, self.y = 0, 30 + 260
        self.frame = 0
        self.reload_time = 140
        self.timer = 0
        self.move_target_point = 0
        self.Is_move_point_set = False
        self.snow_stack = 0
        self.build_behavior_tree()

    def check_player_distance(self):
        if stage_state.player.x - self.x > 280 or self.Is_move_point_set:
            self.cur_state = MOVE

            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def follow_player(self):
        if self.Is_move_point_set:
            self.x += self.velocity

            if self.x > self.move_target_point:
                self.Is_move_point_set = False
                return BehaviorTree.FAIL

        else:
            self.Is_move_point_set = True
            self. move_target_point = stage_state.player.x - random.randint(230, 260)


    def reload(self):
        if self.snow_stack == 0:
            if self.cur_state == RELOAD:
                if self.timer >= self.reload_time:
                    self.snow_stack += 1
                    ReloadMan.giving_snow_queue.insert(0, self)
                    self.timer = 0
                    self.cur_state = IDLE
                    self.frame = 0
                else:
                    self.timer += 1
            else:
                self.timer = 0
                self.cur_state = RELOAD
            return BehaviorTree.SUCCESS
        else:
            self.timer = 0
            return BehaviorTree.FAIL


    def wait(self):
        self.cur_state = IDLE

    def build_behavior_tree(self):
        check_position_node = LeafNode("Check Player Position", self.check_player_distance)
        follow_player_node = LeafNode("Follow Player", self.follow_player)
        reload_node = LeafNode("Reload", self.reload)
        wait_node = LeafNode("Wait", self.wait)

        move_node = SequenceNode("Move")
        move_node.add_children(check_position_node, follow_player_node)

        reload_or_wait_node = SelectorNode("Reload Or Wait")
        reload_or_wait_node.add_children(reload_node, wait_node)

        start_node = SelectorNode("Start Action")
        start_node.add_children(move_node, reload_or_wait_node)
        self.bt = BehaviorTree(start_node)

    def update(self):
        self.bt.run()

        self.frame = (self.frame + 1) % 16


    def draw(self):
        if self.cur_state == IDLE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MOVE:
            self.image.clip_draw(60 * (self.frame//2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == RELOAD:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)


class ThrowMan:
    image = None
    def __init__(self):
        if ThrowMan.image == None:
            ThrowMan.image = load_image('image\\ally\\reload_man\\temp.png')
        self.velocity = 2
        self.cur_state = IDLE
        self.event_que = []
        self.x, self.y = 0, 30 + 260
        self.frame = 0
        self.reload_time = 140
        self.aim_time = 40
        self.timer = 0
        self.move_target_point = 0
        self.target_x = 0
        self.is_move_point_set = False
        self.is_target_set = False
        self.is_aim_done = False
        self.snow_stack = 0
        self.build_behavior_tree()

    def check_player_distance(self):
        if stage_state.player.x - self.x > 280 or self.is_move_point_set:
            self.cur_state = MOVE
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def follow_player(self):
        if self.is_move_point_set:
            self.x += self.velocity

            if self.x > self.move_target_point:
                self.is_move_point_set = False
                return BehaviorTree.FAIL

        else:
            self.is_move_point_set = True
            self. move_target_point = stage_state.player.x - random.randint(230, 260)


    def reload(self):
        if self.snow_stack == 0:
            if self.cur_state == RELOAD:
                if self.timer >= self.reload_time:
                    self.snow_stack += 1
                    self.timer = 0
                else:
                    self.timer += 1
            else:
                self.timer = 0
                self.cur_state = RELOAD
                self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            self.timer = 0
            return BehaviorTree.FAIL

    def aim(self):
        if self.is_target_set:
            if self.cur_state == AIM:
                if self.timer > self.aim_time:
                    self.is_aim_done = True
                    self.timer = 0
                else:
                    self.timer += 1
            else:
                self.cur_state = AIM
                self.timer = 0
                self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def throw(self):
        if self.is_aim_done:
            if self.cur_state == THROW:
                if self.timer > 20:
                    self.throw_snow()
                    self.is_target_set = False
                    self.is_aim_done = False
                    self.timer = 0
                else:
                    self.timer += 1
            else:
                self.cur_state = THROW
                self.timer = 0
                self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def set_target(self):
        for enemy in game_world.layer_objects(game_world.enemy_layer):
            if enemy.cur_state != DEAD1 and enemy.cur_state != DEAD2 and enemy.cur_state != DEAD3:
                self.target_x = enemy.x
                self.is_target_set = True
                return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def wait(self):
        self.cur_state = IDLE

    def build_behavior_tree(self):
        throw_node = LeafNode("Throw", self.throw)
        aim_node = LeafNode("Aim", self.aim)
        check_position_node = LeafNode("Check Player Position", self.check_player_distance)
        follow_player_node = LeafNode("Follow Player", self.follow_player)
        set_target_node = LeafNode("Set Target", self.set_target)
        reload_node = LeafNode("Reload", self.reload)
        wait_node = LeafNode("Wait", self.wait)

        aim_or_throw_node = SelectorNode("Aim Or Throw")
        aim_or_throw_node.add_children(throw_node, aim_node)

        move_node = SequenceNode("Move")
        move_node.add_children(check_position_node, follow_player_node)


        start_node = SelectorNode("Start Action")
        start_node.add_children(aim_or_throw_node, move_node, reload_node, set_target_node, wait_node)
        self.bt = BehaviorTree(start_node)

    def update(self):
        self.bt.run()

        self.frame = (self.frame + 1) % 16


    def draw(self):
        if self.cur_state == IDLE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MOVE:
            self.image.clip_draw(60 * (self.frame//2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == RELOAD:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == AIM:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 6, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == THROW:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 7, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)


    def throw_snow(self):
        distance = self.target_x - self.x  #random.randint(-150, 100)
        vx = random.randint(20, 25)
        t = distance / vx
        vy = t / 5 - (40 / t)
        game_world.add_object(snow.SmallSnow(self.x, self.y + 10, vx, vy, 0), game_world.snow_layer)

        self.snow_stack = 0