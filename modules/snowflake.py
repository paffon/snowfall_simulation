from modules.constants import *
from modules.vector import Vector
import random
import pygame


class Snowflake:
    def __init__(self, distance, mass, size=None, speed=None, position=None, color=WHITE):
        """
        Initialize a Snowflake object.

        Args:
            distance (int): The distance of the snowflake layer from the viewer (higher layers are closer).
            mass (int): The mass of the snowflake, affecting its size and drop speed.
            size (int, optional): The size of the snowflake. Defaults to None.
            speed (Vector, optional): The speed vector of the snowflake. Defaults to None.
            position (Vector, optional): The initial position of the snowflake. Defaults to None.
            color (tuple, optional): The RGB color value of the snowflake. Defaults to WHITE.
        """
        self.error_factor = get_new_error()

        self.distance_factor = (1 / distance) ** 0.5

        self.mass = mass
        self.size = round(mass if size is None else size)

        drop_speed = constraint(self.error_factor * MAX_DROP_SPEED, MIN_DROP_SPEED, MAX_DROP_SPEED)

        self.speed = Vector(0, drop_speed) if speed is None else speed
        self.perceived_speed = self.speed.scale(self.distance_factor)
        self.position = self.init_snowflake_position() if position is None else position

        self.color = color

    def calc_and_return_perceived_speed(self):
        """
        Calculate and return the perceived speed of the snowflake based on its distance.

        Returns:
            Vector: The perceived speed vector of the snowflake.
        """
        return self.speed.scale(self.distance_factor)

    @staticmethod
    def init_snowflake_position(x=None, y=None):
        """
        Initialize the position of the snowflake.

        Args:
            x (int, optional): The initial x-coordinate of the snowflake. Defaults to None.
            y (int, optional): The initial y-coordinate of the snowflake. Defaults to None.

        Returns:
            Vector: The initial position vector of the snowflake.
        """
        x = random.randint(0, WIDTH) if x is None else x
        y = random.randint(0, HEIGHT) if y is None else y

        return Vector(x, y)

    def apply_wind_snowflake(self, wind):
        """
        Apply wind influence to the snowflake's speed.

        Args:
            wind (Vector): The wind vector affecting the snowflake.
        """
        self.speed = Vector(self.error_factor * wind.x, self.speed.y)

        self.perceived_speed = self.speed.scale(self.distance_factor)

    def update_position_snowflake(self):
        """
        Update the position of the snowflake based on its speed and screen bounds.

        If the snowflake goes completely below the bottom of the screen, it reappears at the top with a new error factor.
        """
        self.position = self.position.add(self.perceived_speed)
        if self.position.y > HEIGHT + self.size:  # Completely below the bottom of the screen
            self.position = self.init_snowflake_position(y=-self.size)
            self.error_factor = get_new_error()

    def draw_snowflake(self, surface, shape='circle'):
        """
        Draw the snowflake on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the snowflake on.
            shape (str, optional): The shape of the snowflake ('circle' or 'snowflake'). Defaults to 'circle'.

        Raises:
            ValueError: If an unknown shape is provided for snowflake drawing.
        """
        if shape == 'circle':
            pygame.draw.circle(surface, self.color, (self.position.x, self.position.y), self.size)
        elif shape == 'snowflake':
            x, y = self.position.x, self.position.y
            s = self.size
            pygame.draw.line(surface, self.color, (x, y - s), (x, y + s))
            pygame.draw.line(surface, self.color, (x - s, y), (x + s, y))
            pygame.draw.line(surface, self.color, (x - s / 1.4, y - s / 1.4), (x + s / 1.4, y + s / 1.4))
            pygame.draw.line(surface, self.color, (x + s / 1.4, y - s / 1.4), (x - s / 1.4, y + s / 1.4))
        else:
            raise ValueError(f'Unknown shape for a snowflake drawing: {shape}')
