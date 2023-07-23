import random
import pygame

# Display
WIDTH, HEIGHT = 1000, 600
WHITE = (240, 240, 230)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 20)
LIGHT_BLUE = (0, 0, 40)
YELLOW = (255, 255, 0)

# {layer index: count}
dict_layer_to_amount = {1: 200, 2: 160, 3: 120, 4: 20, 5: 10, 6: 3}

layers_count = len(dict_layer_to_amount)

# Speed related constants
WIND_CHANGES_INCREMENTS = 0.05
MAX_WIND = 1.5
MIN_WIND = -MAX_WIND
MAX_DROP_SPEED = 2.5
MIN_DROP_SPEED = MAX_DROP_SPEED * 0.5

ERROR_PERCENTAGE = 10

SNOWFLAKE_SHAPE = 'snowflake'

# Tail
TAIL_LENGTH = 50
TAIL_SHAPE = 'snowflake'
RENDER_TAIL = False


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
    min_brightness = 100
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


def draw_snowflake(surface, shape, position, size, color, alpha):
    """
    Draw the snowflake on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw the snowflake on.
        shape (str, optional): The shape of the snowflake ('circle' or 'snowflake'). Defaults to 'circle'.
        position (pygame.Vector2): The position of the center of the snowflake on the surface.
        size (int): The size of the snowflake (radius for circle, half-length of lines for snowflake).
        color (tuple): A tuple representing the color of the snowflake in the format (r, g, b),
                       with values in the range of 0 to 255 for each component.
        alpha (float): A value between 0 and 1 representing the transparency of the snowflake.
                       0 = fully transparent (invisible), 1 = fully opaque.

    Raises:
        ValueError: If an unknown shape is provided for snowflake drawing.
    """

    # Create a temporary surface with an alpha channel
    snowflake_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

    # Draw the snowflake shape on the temporary surface
    if shape == 'circle':
        pygame.draw.circle(snowflake_surface, color + (int(alpha * 255),), (size, size), size)
    elif shape == 'snowflake':
        s = size
        pygame.draw.line(snowflake_surface, color + (int(alpha * 255),), (size, size - s), (size, size + s))
        pygame.draw.line(snowflake_surface, color + (int(alpha * 255),), (size - s, size), (size + s, size))
        pygame.draw.line(snowflake_surface, color + (int(alpha * 255),), (size - s / 1.4, size - s / 1.4), (size + s / 1.4, size + s / 1.4))
        pygame.draw.line(snowflake_surface, color + (int(alpha * 255),), (size + s / 1.4, size - s / 1.4), (size - s / 1.4, size + s / 1.4))
    else:
        raise ValueError(f'Unknown shape for a snowflake drawing: {shape}')

    # Blit the temporary surface onto the main surface with transparency
    surface.blit(snowflake_surface, (position.x - size, position.y - size))



