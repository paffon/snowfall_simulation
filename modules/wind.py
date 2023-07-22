from modules.vector import Vector
from modules.constants import *

class Wind(Vector):
    def __init__(self, x=0., y=0.):
        """
        Initialize a Wind object with x and y components.

        Args:
            x (float): The x-component of the wind vector.
            y (float): The y-component of the wind vector.
        """
        super().__init__(x, y)
        self.direction = WIND_CHANGES_INCREMENTS

    def update(self):
        """
        Update the wind vector randomly, changing its x-component.

        The wind direction can randomly change its x-component (positive or negative)
        based on the value of WIND_CHANGES_INCREMENTS.
        """
        if random.random() > 0.5:
            self.x += WIND_CHANGES_INCREMENTS
        else:
            self.x -= WIND_CHANGES_INCREMENTS

        self.x = constraint(self.x, MIN_WIND, MAX_WIND)

    def cyclic_update(self, cycle):
        """
        Update the wind vector cyclically.

        Args:
            cycle (int): The number of cycles after which to reverse the wind direction.
        """
        if self.direction > 0 and self.x > MAX_WIND:
            self.direction = -WIND_CHANGES_INCREMENTS / cycle
        if self.direction < 0 and self.x < MIN_WIND:
            self.direction = +WIND_CHANGES_INCREMENTS / cycle

        self.x += self.direction
