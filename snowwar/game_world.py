
back_ground_layer, character_layer, snow_layer, snow_wall_layer = 0, 1, 2, 3

objects = [[], [], [], []]

def add_object(o, layer):
    objects[layer].append(o)

def remove_object(o, layer):
    if o in objects[layer]:
        objects[layer].remove(o)
        del o

def clear():
    for o in all_objects():
        del o
    objects.clear()

def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

def layer_objects(layer):
    for o in objects[layer]:
        yield o






