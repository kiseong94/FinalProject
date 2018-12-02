from pico2d import *
import main_state
import stage_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import snow
import game_world

IDLE, MOVE, AIM, THROW, HIT, DEAD1, DEAD2, DEAD3, SIT, MAKE_WALL, RELOAD, ATTACK = range(12)
RELOAD_MAN, THROW_MAN, SHOVEL_MAN, STORAGE = range(4)
LEFT, RIGHT = range(2)

class Ally:
    hp_bar = None
    hp_gauge = None
    hit_sound = None
    throw_sound = None
    reload_sound = None
    make_wall_sound = None
    melee_attack_sound = None

    def load_sound(self):
        if Ally.hit_sound == None:
            Ally.hit_sound = load_wav('sound\\hit.ogg')
        if Ally.throw_sound == None:
            Ally.throw_sound = load_wav('sound\\throw.ogg')
        if Ally.reload_sound == None:
            Ally.reload_sound = load_wav('sound\\reload.ogg')
            Ally.reload_sound.set_volume(20)
        if Ally.make_wall_sound == None:
            Ally.make_wall_sound = load_wav('sound\\makewall.ogg')
            Ally.make_wall_sound.set_volume(30)


    def hit_by_snow(self, snow):
        self.hit_sound.play()
        if self.hp > 0:
            self.hp -= snow.damage

        if self.hp <= 0:
            self.die()


    def hit_by_melee(self, damage):
        self.hit_sound.play()
        if self.hp > 0:
            self.hp -= damage

        if self.hp <= 0:
            self.die()

    def draw_hp_gauge(self):
        t = 30 * self.hp // self.max_hp // 2

        self.hp_bar.draw(self.x - stage_state.base_x, self.y - 50)
        if self.hp > 0:
            self.hp_gauge.draw(self.x - stage_state.base_x - 15 + t, self.y - 50, t * 2, 5)

    def snow_collision_check(self):
        for snow in game_world.layer_objects(game_world.snow_layer):
            if snow.vx < 0:
                if snow.collision_object(*self.get_hit_box()):
                    self.hit_by_snow(snow)

    def out_of_sight(self):
        if stage_state.base_x > self.x or self.x > stage_state.base_x + 1600:
            return True

    def delete(self):
        game_world.remove_object(self, game_world.player_layer)

    def get_hit_box(self):
        if self.cur_state == RELOAD:
            return self.x - 10, self.y + 5, self.x + 10, self.y - 25
        else:
            return self.x - 10, self.y + 20, self.x + 10, self.y - 25

    def change_state(self, state):
        self.cur_state = state
        self.timer = 0
        self.frame = 0

    def die(self):
        self.change_state(DEAD1)

        if isinstance(self, ReloadMan):
            main_state.Data.num_ally[RELOAD_MAN] -= 1
        elif isinstance(self, ThrowMan):
            main_state.Data.num_ally[THROW_MAN] -= 1
        elif isinstance(self, ShovelMan):
            main_state.Data.num_ally[SHOVEL_MAN] -= 1
        elif isinstance(self, Storage):
            main_state.Data.num_ally[STORAGE] -= 1




# initialization code
class ReloadMan(Ally):
    image = None
    giving_snow_queue = []
    def __init__(self):
        if Ally.hp_bar == None:
            Ally.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Ally.hp_gauge == None:
            Ally.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        if ReloadMan.image == None:
            ReloadMan.image = load_image('image\\ally\\reloadman.png')
        self.load_sound()
        self.hp = 2
        self.max_hp = 2
        self.velocity = 2
        self.cur_state = IDLE
        self.event_que = []
        self.x, self.y = stage_state.base_x - 20, 30 + 260
        self.frame = 0
        self.reload_time = 140
        self.timer = 0
        self.move_target_point = 0
        self.Is_move_point_set = False
        self.snow_stack = 0
        self.build_behavior_tree()
        self.targeted = False

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
                    if main_state.Data.num_ally[STORAGE] != 0 and Storage.num_ammo[0] < main_state.Data.num_ally[STORAGE] * 40:
                        Storage.num_ammo[0] += 1
                    else:
                        self.snow_stack += 1
                        ReloadMan.giving_snow_queue.insert(0, self)
                    self.timer = 0
                    self.cur_state = IDLE
                    self.frame = 0
                else:
                    self.timer += 1
            else:
                self.reload_sound.play()
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
        if self.cur_state != DEAD1:
            self.bt.run()
            self.snow_collision_check()
            self.frame = (self.frame + 1) % 16
        else:
            if self.out_of_sight():
                self.delete()
            if self.frame < 15:
                self.frame += 1


    def draw(self):
        if self.cur_state == IDLE:
            if self.snow_stack == 0:
                self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
            else:
                self.image.clip_draw(60 * (self.frame // 2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MOVE:
            if self.snow_stack == 0:
                self.image.clip_draw(60 * (self.frame // 2), 60 * 2, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
            else:
                self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == RELOAD:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 4, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 5, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)

        if self.cur_state != DEAD1:
            self.draw_hp_gauge()



class ThrowMan(Ally):
    image = None
    def __init__(self):
        if Ally.hp_bar == None:
            Ally.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Ally.hp_gauge == None:
            Ally.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        if ThrowMan.image == None:
            ThrowMan.image = load_image('image\\ally\\throwman.png')
        self.load_sound()
        self.hp = 3
        self.max_hp = 3
        self.velocity = 2
        self.cur_state = IDLE
        self.event_que = []
        self.x, self.y = stage_state.base_x - 20, 30 + 260
        self.frame = 0
        self.reload_time = 140
        self.aim_time = 40
        self.timer = 0
        self.target_x = 0
        self.target = None
        self.snow_stack = 0
        self.build_behavior_tree()
        self.targeted = False

    def check_player_distance(self):
        if stage_state.player.x - self.x > 280:
            self.change_state(MOVE)
            self.target_x = stage_state.player.x - random.randint(100, 200)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def follow_player(self):
        self.x += self.velocity
        if self.x >= self.target_x:
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING


    def reload(self):
        if self.snow_stack == 0:
            if self.get_snow():
                return BehaviorTree.SUCCESS
            else:
                if self.cur_state == RELOAD:
                    if self.timer >= self.reload_time:
                        self.snow_stack += 1
                        self.timer = 0
                    else:
                        self.timer += 1
                else:
                    self.reload_sound.play()
                    self.timer = 0
                    self.cur_state = RELOAD
                    self.frame = 0
                return BehaviorTree.SUCCESS
        else:
            self.timer = 0
            return BehaviorTree.FAIL

    def aim(self):
        if self.cur_state == AIM:
            if self.timer > self.aim_time:
                self.timer = 0
                return BehaviorTree.SUCCESS
            else:
                self.timer += 1
        else:
            self.change_state(AIM)
        return BehaviorTree.RUNNING


    def throw(self):
        if self.cur_state == THROW:
            if self.timer > 16:
                self.timer = 0
                return BehaviorTree.SUCCESS
            elif self.timer == 12:
                self.throw_sound.play()
                self.throw_snow()
                self.timer += 1
            else:
                self.timer += 1
        else:
            self.change_state(THROW)
        return BehaviorTree.RUNNING


    def set_target(self):
        if random.randint(0, 1):
            nearest = None
            for enemy in game_world.layer_objects(game_world.enemy_layer):
                if enemy.cur_state != DEAD1 and enemy.cur_state != DEAD2 and enemy.cur_state != DEAD3 and\
                        stage_state.base_x + 500 < enemy.x < stage_state.base_x + 1200:
                    if nearest == None:
                        nearest = enemy
                    elif nearest.x > enemy.x:
                        nearest = enemy
            if nearest != None:
                self.target = nearest
                self.target.targeted = True
                return BehaviorTree.SUCCESS

        else:
            for enemy in game_world.layer_objects(game_world.enemy_layer):
                if enemy.cur_state != DEAD1 and enemy.cur_state != DEAD2 and enemy.cur_state != DEAD3 and \
                        stage_state.base_x + 500 < enemy.x < stage_state.base_x + 1200 and not enemy.targeted:
                    self.target = enemy
                    self.target.targeted = True
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

        aim_or_throw_node = SequenceNode("Aim Or Throw")
        aim_or_throw_node.add_children(set_target_node, aim_node, throw_node)

        move_node = SequenceNode("Move")
        move_node.add_children(check_position_node, follow_player_node)


        start_node = SelectorNode("Start Action")
        start_node.add_children(move_node, reload_node, aim_or_throw_node, wait_node)
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
        if self.cur_state == IDLE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MOVE:
            self.image.clip_draw(60 * (self.frame//2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == RELOAD:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 2, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == AIM:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == THROW:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 4, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 5, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)

        if self.cur_state != DEAD1:
            self.draw_hp_gauge()

    def throw_snow(self):
        distance = self.target.x - self.x + random.randint(0, 200)
        vx = random.randint(15, 20)
        t = distance / vx
        vy = t / 5 - (40 / t)
        game_world.add_object(snow.SmallSnow(self.x, self.y + 10, vx, vy, self.snow_stack), game_world.snow_layer)
        self.target.targeted = False
        self.snow_stack = 0

    def get_snow(self):
        if main_state.Data.num_ally[STORAGE] != 0:
            if Storage.num_ammo[0] > 0:
                Storage.num_ammo[0] -= 1
                self.snow_stack += 1
                return True

        elif len(ReloadMan.giving_snow_queue) > 0:
            giver = ReloadMan.giving_snow_queue.pop()
            giver.snow_stack -= 1
            self.snow_stack += 1
            return True

        return False




class ShovelMan(Ally):
    image = None
    def __init__(self):
        if Ally.hp_bar == None:
            Ally.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Ally.hp_gauge == None:
            Ally.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        if ShovelMan.image == None:
            ShovelMan.image = load_image('image\\ally\\shovelman.png')
        self.load_sound()
        self.hp = 6
        self.max_hp = 6
        self.velocity = 3
        self.cur_state = IDLE
        self.event_que = []
        self.x, self.y = stage_state.base_x - 20, 30 + 260
        self.frame = 0
        self.timer = 0
        self.move_target_point = 0
        self.shovel_power = 1
        self.is_move_point_set = False
        self.is_target_set = False
        self.target_wall = None
        self.build_behavior_tree()
        self.shoveling_time = 50
        self.dir = RIGHT
        self.targeted = False

    def check_player_distance(self):
        if stage_state.player.x - self.x > 280 or self.is_move_point_set:
            self.cur_state = MOVE
            self.target_wall = None
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
            self. move_target_point = stage_state.player.x - random.randint(50, 100)

    def find_target_wall(self):
        farthest = None
        for wall in game_world.layer_objects(game_world.snow_wall_layer):
            if stage_state.player.x - 250 <= wall.x <= stage_state.player.x + 50 and wall.occupied == False and wall.max_hp > wall.hp:
                if farthest == None:
                    farthest = wall
                elif farthest.x < wall.x:
                    farthest = wall
                if self.target_wall == None:
                    self.target_wall = wall

        if farthest == None:
            self.target_wall = None
            return BehaviorTree.FAIL
        else:
            self.target_wall = farthest
            return BehaviorTree.SUCCESS


    def move_to_target_wall(self):
        if self.target_wall == None:
            return BehaviorTree.FAIL
        elif self.target_wall.x - 35 <= self.x <= self.target_wall.x - 20:
            return BehaviorTree.FAIL
        else:
            self.cur_state = MOVE
            if self.x <= self.target_wall.x - 30:
                self.x += self.velocity
                self.dir = RIGHT
            else:
                self.x -= self.velocity
                self.dir = LEFT
            return BehaviorTree.SUCCESS

    def strengthen_wall(self):
        if self.target_wall == None:
            return BehaviorTree.FAIL
        else:
            if self.target_wall.max_hp > self.target_wall.hp:
                if self.cur_state != MAKE_WALL:
                    self.cur_state = MAKE_WALL
                    self.timer = 0
                else:
                    if self.shoveling_time <= self.timer:
                        self.make_wall_sound.play()
                        self.target_wall.strengthen_wall(self.shovel_power)
                        self.timer = 0
                    else:
                        self.timer += 1
                return BehaviorTree.SUCCESS
            return BehaviorTree.FAIL

    def wait(self):
        self.cur_state = IDLE

    def build_behavior_tree(self):
        find_wall_node = LeafNode("Throw", self.find_target_wall)
        move_to_wall_node = LeafNode("Aim", self.move_to_target_wall)
        check_position_node = LeafNode("Check Player Position", self.check_player_distance)
        follow_player_node = LeafNode("Follow Player", self.follow_player)
        strengthen_wall_node = LeafNode("Set Target", self.strengthen_wall)
        wait_node = LeafNode("Wait", self.wait)

        move_node = SequenceNode("Move")
        move_node.add_children(check_position_node, follow_player_node)

        find_move_wall_node = SequenceNode("Find And Move to Wall")
        find_move_wall_node.add_children(find_wall_node, move_to_wall_node)

        get_cover_node = SelectorNode("Get Cover")
        get_cover_node.add_children(find_move_wall_node, strengthen_wall_node)

        start_node = SelectorNode("Start Action")
        start_node.add_children(move_node, get_cover_node, wait_node)
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
        if self.cur_state == IDLE:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 0, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MOVE:
            if self.dir == RIGHT:
                self.image.clip_draw(60 * (self.frame//2), 60 * 1, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
            else:
                self.image.clip_composite_draw(60 * (self.frame // 2), 60 * 1, 60, 60, 0, 'h', self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == MAKE_WALL:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 2, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(60 * (self.frame // 2), 60 * 3, 60, 60, self.x - stage_state.base_x, self.y, 60, 60)

        if self.cur_state != DEAD1:
            self.draw_hp_gauge()


class Storage(Ally):
    image = None
    num_ammo = [0, 0, 0]

    def __init__(self):
        if Ally.hp_bar == None:
            Ally.hp_bar = load_image('image\\ui\\hp_bar.png')
        if Ally.hp_gauge == None:
            Ally.hp_gauge = load_image('image\\ui\\hp_gauge.png')
        if Storage.image == None:
            Storage.image = load_image('image\\ally\\storage_image.png')
        self.load_sound()
        self.hp = 10
        self.max_hp = 10
        self.velocity = 2
        self.cur_state = IDLE
        self.x, self.y = stage_state.base_x - 20, 30 + 260
        self.frame = 0
        self.timer = 0
        self.move_target_x = 0
        self.build_behavior_tree()
        self.targeted = False

    def check_player_distance(self):
        if stage_state.player.x - self.x > 280:
            self.change_state(MOVE)
            self.target_x = stage_state.player.x - random.randint(180, 260)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def follow_player(self):
        self.x += self.velocity
        if self.x >= self.target_x:
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def wait(self):
        self.cur_state = IDLE

    def build_behavior_tree(self):
        check_position_node = LeafNode("Check Player Position", self.check_player_distance)
        follow_player_node = LeafNode("Follow Player", self.follow_player)

        wait_node = LeafNode("Wait", self.wait)

        move_node = SequenceNode("Move")
        move_node.add_children(check_position_node, follow_player_node)

        start_node = SelectorNode("Start Action")
        start_node.add_children(move_node, wait_node)
        self.bt = BehaviorTree(start_node)

    def update(self):
        if self.cur_state != DEAD1 and self.cur_state != DEAD2 and self.cur_state != DEAD3:
            self.bt.run()
            self.snow_collision_check()
            self.get_snow()
            self.frame = (self.frame + 1) % 16
        else:
            if self.out_of_sight():
                self.delete()
            if self.frame < 15:
                self.frame += 1


    def draw(self):
        if self.cur_state == IDLE:
            self.image.clip_draw(80 * (self.frame // 2), 60 * 0, 80, 60, self.x - stage_state.base_x, self.y)
        elif self.cur_state == MOVE:
            self.image.clip_draw(80 * (self.frame//2), 60 * 1, 80, 60, self.x - stage_state.base_x, self.y)
        elif self.cur_state == DEAD1:
            self.image.clip_draw(80 * (self.frame // 2), 60 * 2, 80, 60, self.x - stage_state.base_x, self.y, 80, 60)

        if self.cur_state != DEAD1:
            self.draw_hp_gauge()

    def get_snow(self):
        if Storage.num_ammo[0] < main_state.Data.num_ally[STORAGE]*40:
            while len(ReloadMan.giving_snow_queue) > 0:
                giver = ReloadMan.giving_snow_queue.pop()
                giver.snow_stack -= 1
                Storage.num_ammo[0] += 1