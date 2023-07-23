import random

from modules.snowflake import Snowflake
from modules.constants import *

class Layer:
    def __init__(self, distance, mass, snowflakes_count, wind, color_scale):
        """
        Initialize a Layer object with snowflakes.

        Args:
            distance (int): The distance of the layer from the viewer (higher layers are closer).
            mass (int): The mass of the layer, which affects wind influence.
            snowflakes_count (int): The number of snowflakes in the layer.
            wind (Wind): The wind object affecting the layer.
            color_scale (float): The color scale for snowflakes in this layer (0 to 1).
        """
        self.distance = distance
        self.mass = mass
        self.snowflakes_count = snowflakes_count
        self.wind = wind

        self.snowflakes = []
        for i in range(snowflakes_count):
            # Create snowflakes with different colors based on color_scale
            color = get_snowflake_color(scale=color_scale**3, mode='scale')
            new_snowflake = Snowflake(distance=distance, mass=mass, color=color)
            self.snowflakes.append(new_snowflake)

    def apply_wind(self, wind):
        """
        Apply wind influence to each snowflake in the layer.

        Args:
            wind (Wind): The wind object affecting the layer.
        """
        for snowflake in self.snowflakes:
            snowflake.apply_wind_snowflake(wind)

    def update(self):
        """
        Update the positions of all snowflakes in the layer.
        """
        for snowflake in self.snowflakes:
            snowflake.update_position_snowflake()

    def draw(self, screen):
        """
        Draw all snowflakes in the layer on the screen.

        Args:
            screen (pygame.Surface): The screen surface to draw the snowflakes on.
        """
        for snowflake in self.snowflakes:
            if random.random() > 0.999:
                color = snowflake.shiny_color
            else:
                color = snowflake.color
            draw_snowflake(surface=screen,
                           shape=SNOWFLAKE_SHAPE,
                           position=snowflake.position,
                           size=snowflake.size,
                           color=color,
                           alpha=1)
            if RENDER_TAIL:
                snowflake.render_tail(screen)
