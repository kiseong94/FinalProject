
back_ground_layer, player_layer, enemy_layer, snow_layer, snow_wall_layer = range(5)

objects = [[], [], [], [], []]

def add_object(o, layer):
    objects[layer].append(o)

def remove_object(o, layer):
    if o in objects[layer]:
        objects[layer].remove(o)
        del o

def clear():

    for i in range(len(objects[back_ground_layer])):
        o = objects[back_ground_layer].pop()
        del o
    for i in range(len(objects[player_layer])):
        o = objects[player_layer].pop()
        del o
    for i in range(len(objects[enemy_layer])):
        o = objects[enemy_layer].pop()
        del o
    for i in range(len(objects[snow_layer])):
        o = objects[snow_layer].pop()
        del o
    for i in range(len(objects[snow_wall_layer])):
        o = objects[snow_wall_layer].pop()
        del o


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def layer_objects(layer):
    for o in objects[layer]:
        yield o






