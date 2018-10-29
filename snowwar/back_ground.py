from pico2d import *



class Back_Ground:
    def __init__(self):
        self.ground_image = load_image('ground.png')
        self.mountain_image = load_image('mountain.png')
        self.forest_image = load_image('forest.png')
        self.tree_image = load_image('trees.png')
        self.mountain_x = 0
        self.forest_x = 0
        self.ground_x = 0


    def draw(self):
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
        pass
