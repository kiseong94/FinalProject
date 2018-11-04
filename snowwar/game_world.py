
back_ground_layer, character_layer, snow_layer, snow_wall_layer = range(4)

objects = [[], [], [], []]

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
    for o in objects[character_layer]:
        objects[character_layer].remove(o)
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






