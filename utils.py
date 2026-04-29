def get_color(value, normal_range):
    if value < normal_range[0] or value > normal_range[1]:
        return "red"
    elif abs(value - normal_range[1]) < 5:
        return "yellow"
    return "green"
