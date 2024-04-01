def map_temperature_to_color(temperature, lb=18, up=25):
    if temperature <= lb:
        return (0, 0, 255)
    elif temperature >= up:
        return (255, 0, 0)
    else:
        t = (temperature - lb) / (up - lb)
        r = int(max(0, min(255, 255 * t)))
        b = int(max(0, min(255, 255 * (1 - t))))
        g = 0
        return (r, g, b)

def is_wall_vertical(wall):
    return wall.width < wall.height

def check_wall_click(event, objects, tmp_objects):
    for obj in objects:
        if obj.collidepoint(event.pos):
            if obj not in tmp_objects:
                tmp_objects.append(obj)
            else:
                tmp_objects.remove(obj)
            break
        
def add_unique_elements(initial_list, new_elements):
    for element in new_elements:
        if element not in initial_list:
            initial_list.append(element)
    return initial_list
