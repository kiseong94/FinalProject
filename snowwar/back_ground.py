from pico2d import *

A_DOWN, A_UP, S_DOWN, S_UP, W_DOWN, W_UP, D_DOWN, D_UP, R_DOWN, LEFT_BUTTON_DOWN, LEFT_BUTTON_UP = range(11)


key_event_table = {
    (SDL_KEYDOWN, SDLK_a): A_DOWN, (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_s): S_DOWN, (SDL_KEYUP, SDLK_s): S_UP,
    (SDL_KEYDOWN, SDLK_w): W_DOWN, (SDL_KEYUP, SDLK_w): W_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN, (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_r): R_DOWN
}
mouse_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LEFT_BUTTON_DOWN,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): LEFT_BUTTON_UP,
}

class MoveState:
    @staticmethod
    def do(background):
        background.move_ground()
        background.move_forest()
        background.move_mountain()

class IdleState:
    @staticmethod
    def do(background):
        pass


next_state_table = {
    IdleState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: IdleState, S_UP: IdleState, W_DOWN: IdleState,
                W_UP: IdleState, R_DOWN: IdleState, LEFT_BUTTON_DOWN: IdleState, LEFT_BUTTON_UP: IdleState},
    MoveState: {A_DOWN: MoveState, D_DOWN: MoveState, A_UP: IdleState, D_UP: IdleState, S_DOWN: IdleState, S_UP: MoveState, W_DOWN: IdleState,
           W_UP: MoveState, R_DOWN: IdleState, LEFT_BUTTON_DOWN: IdleState, LEFT_BUTTON_UP: MoveState}
}

class Back_Ground:
    def __init__(self):
        self.event_que = []
        self.ground_image = load_image('image\\background\\ground.png')
        self.mountain_image = load_image('image\\background\\mountain.png')
        self.forest_image = load_image('image\\background\\forest.png')
        self.tree_image = load_image('image\\background\\trees.png')
        self.sky_image = load_image('image\\background\\sky.png')
        self.mountain_x = 0
        self.forest_x = 0
        self.ground_x = 0
        self.velocity = 0
        self.cur_state = IdleState


    def draw(self):
        self.sky_image.draw(800, 550, 1600, 700)
        self.mountain_image.draw(800 - self.mountain_x, 200 + self.mountain_image.h, 1600, 400)
        self.mountain_image.draw(1600 + 800 - self.mountain_x, 200 + self.mountain_image.h, 1600, 400)
        self.forest_image.draw(800 - self.forest_x, 340, 1600, 160)
        self.forest_image.draw(1600 + 800 - self.forest_x, 340, 1600, 160)
        self.tree_image.draw(800 - self.ground_x, 340 + self.tree_image.h//2, 1600, 320)
        self.tree_image.draw(1600 + 800 - self.ground_x, 340 + self.tree_image.h // 2, 1600, 320)
        self.ground_image.draw(800 - self.ground_x, 230)
        self.ground_image.draw(1600 + 800 - self.ground_x, 230)



    def move_ground(self):
        self.ground_x = (self.ground_x + self.velocity) % 1600

    def move_forest(self):
        self.forest_x = (self.forest_x + self.velocity/(3/2)) % 1600

    def move_mountain(self):
        self.mountain_x = (self.mountain_x + self.velocity/3) % 1600


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state = next_state_table[self.cur_state][event]


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == D_DOWN:
                self.velocity += 3
            elif key_event == D_UP:
                self.velocity -= 3
            elif key_event == A_DOWN:
                self.velocity -= 2
            elif key_event == A_UP:
                self.velocity += 2
            self.add_event(key_event)
        elif (event.type, event.button) in mouse_event_table:
            key_event = mouse_event_table[(event.type, event.button)]
            self.add_event(key_event)
