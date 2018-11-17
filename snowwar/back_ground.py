from pico2d import *

A_DOWN, A_UP, D_DOWN, D_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_a): A_DOWN, (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN, (SDL_KEYUP, SDLK_d): D_UP,
}




class Back_Ground:
    def __init__(self):
        self.ground_image = load_image('image\\background\\ground.png')
        self.mountain_image = load_image('image\\background\\mountain.png')
        self.forest_image = load_image('image\\background\\forest.png')
        self.tree_image = load_image('image\\background\\trees.png')
        self.sky_image = load_image('image\\background\\sky.png')
        self.mountain_x = 0
        self.forest_x = 0
        self.ground_x = 0
        self.velocity = 0


    def draw(self):
        self.sky_image.draw(800, 550, 1600, 700)
        self.mountain_image.draw(800 - self.mountain_x, 200 + self.mountain_image.h, 1600, 400)
        self.mountain_image.draw(1600 + 800 - self.mountain_x, 200 + self.mountain_image.h, 1600, 400)
        self.forest_image.draw(800 - self.forest_x, 340, 1600, 160)
        self.forest_image.draw(1600 + 800 - self.forest_x, 340, 1600, 160)
        self.tree_image.draw(800 - self.ground_x, 340 + self.tree_image.h//2, 1600, 320)
        self.tree_image.draw(1600 + 800 - self.ground_x, 340 + self.tree_image.h // 2, 1600, 320)
        self.ground_image.draw(800 - self.ground_x,230)
        self.ground_image.draw(1600 + 800 - self.ground_x, 230)



    def move_ground(self, distance):
        self.ground_x = (self.ground_x + distance) % 1600

    def move_forest(self, distance):
        self.forest_x = (self.forest_x + distance/(3/2)) % 1600

    def move_mountain(self, distance):
        self.mountain_x = (self.mountain_x + distance/3) % 1600

    def update(self):
        self.move_ground(self.velocity)
        self.move_forest(self.velocity)
        self.move_mountain(self.velocity)

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

