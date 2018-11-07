
back_ground_layer, player_layer, enemy_layer, snow_layer, snow_wall_layer = range(5)

objects = [[], [], [], [], []]

def add_object(o, layer):
    objects[layer].append(o)

def remove_object(o, layer):
    if o in objects[layer]:
        objects[layer].remove(o)
        del o

def clear():
    for o in objects[back_ground_layer]:
        objects[back_ground_layer].remove(o)
        del o
    for o in objects[player_layer]:
        objects[player_layer].remove(o)
        del o
    for o in objects[enemy_layer]:
        objects[enemy_layer].remove(o)
        del o
    for o in objects[snow_layer]:
        objects[snow_layer].remove(o)
        del o
    for o in objects[snow_wall_layer]:
        objects[snow_wall_layer].remove(o)
        del o






def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def layer_objects(layer):
    for o in objects[layer]:
        yield o






