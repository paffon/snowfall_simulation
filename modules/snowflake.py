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
        self.perceived_speed = self.calc_and_return_perceived_speed()
        self.position = self.init_snowflake_position() if position is None else position

        self.color = color
        r, g, b = color
        self.shiny_color = ((r + 255) / 2, (g + 255) / 2, (b + 255) / 2)

        self.tail = []

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

        self.perceived_speed = self.calc_and_return_perceived_speed()

    def update_position_snowflake(self):
        """
        Update the position of the snowflake based on its speed and screen bounds.

        If the snowflake goes completely below the bottom of the screen, it reappears at the top with a new error factor.
        """
        self.update_tail()
        self.position = self.position.add(self.perceived_speed)
        if self.position.y > HEIGHT + self.size:  # Completely below the bottom of the screen
            self.position = self.init_snowflake_position(y=-self.size)
            self.error_factor = get_new_error()

    def update_tail(self):
        self.tail.insert(0, self.position.copy())
        if len(self.tail) > TAIL_LENGTH:
            self.tail.pop()

    def render_tail(self, surface):
        r, g, b = self.color
        r_steps = r / TAIL_LENGTH
        g_steps = g / TAIL_LENGTH
        b_steps = b / TAIL_LENGTH

        for i, element_position in enumerate(self.tail):
            steps = i + 1
            alpha = (1 - steps / TAIL_LENGTH) ** 5

            draw_snowflake(
                surface=surface,
                shape=TAIL_SHAPE,
                position=element_position,
                size=self.size,
                color=self.color,
                alpha=alpha)
