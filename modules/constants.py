import random
import pygame

# Display
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 20)
LIGHT_BLUE = (0, 0, 40)

# {layer index: count}
dict_layer_to_amount = {1: 200, 2: 130, 3: 100, 4: 20, 5: 10}

layers_count = len(dict_layer_to_amount)

# Speed related constants
WIND_CHANGES_INCREMENTS = 0.05
MAX_WIND = 1.5
MIN_WIND = -MAX_WIND
MAX_DROP_SPEED = 2.5
MIN_DROP_SPEED = MAX_DROP_SPEED * 0.5

ERROR_PERCENTAGE = 10


def get_new_error():
    """
    Generate a random error percentage for wind speed variation.

    Returns:
        float: A random error percentage within the range [-ERROR_PERCENTAGE, ERROR_PERCENTAGE].
    """
    return random.randint(-ERROR_PERCENTAGE, ERROR_PERCENTAGE) / 100


def constraint(value, min_value, max_value):
    """
    Constraint a value within a specified range.

    Args:
        value (float): The value to be constrained.
        min_value (float): The minimum allowed value.
        max_value (float): The maximum allowed value.

    Returns:
        float: The constrained value within the specified range.
    """
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value

    return value


def get_snowflake_color(scale=1, mode='random'):
    """
    Get the color for a snowflake based on its scale and color mode.

    Args:
        scale (float): The scale of the snowflake (0 to 1).
        mode (str): The color mode ('random' or 'scale').

    Returns:
        tuple: The RGB color value for the snowflake.
    """
    min_brightness = 75
    max_brightness = 255

    if mode == 'random':
        v = random.randint(min_brightness, max_brightness)

    elif mode == 'scale':
        gap = max_brightness - min_brightness
        to_add = gap * scale
        v = min_brightness + to_add
    else:
        raise ValueError(f'Unknown model {mode}')

    return v, v, constraint(round(v * 1.1), 0, 255)


def create_gradient_surface(width, height, start_color, end_color):
    """
    Create a gradient surface from start_color to end_color.

    Args:
        width (int): Width of the gradient surface.
        height (int): Height of the gradient surface.
        start_color (tuple): RGB color value at the top.
        end_color (tuple): RGB color value at the bottom.

    Returns:
        pygame.Surface: The gradient surface.
    """
    gradient_surface = pygame.Surface((width, height))
    for y in range(height):
        progress = y / float(height - 1)
        r = start_color[0] + int((end_color[0] - start_color[0]) * progress)
        g = start_color[1] + int((end_color[1] - start_color[1]) * progress)
        b = start_color[2] + int((end_color[2] - start_color[2]) * progress)
        line_color = (r, g, b)
        pygame.draw.line(gradient_surface, line_color, (0, y), (width - 1, y))
    return gradient_surface
