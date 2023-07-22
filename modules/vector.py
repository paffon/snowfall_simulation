class Vector:
    def __init__(self, x=0.0, y=0.0):
        """
        Initialize a 2D vector with x and y components.

        Args:
            x (float): The x-component of the vector.
            y (float): The y-component of the vector.
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Get a string representation of the vector.

        Returns:
            str: A string representation of the vector in the format "Vector(x, y)".
        """
        return f'Vector({self.x}, {self.y})'

    def copy(self):
        """
        Create a copy of the vector.

        Returns:
            Vector: A new Vector object with the same x and y components.
        """
        new_vector = Vector(self.x, self.y)
        return new_vector

    def add(self, other, inplace=False):
        """
        Add another vector to the current vector.

        Args:
            other (Vector): The vector to be added.
            inplace (bool, optional): If True, the current vector is modified in-place.
                                      If False, a new vector is created. Defaults to False.

        Returns:
            Vector: The resulting vector after addition.
        """
        vector = self if inplace else self.copy()
        vector.x += other.x
        vector.y += other.y

        return vector

    def scale(self, scalar, inplace=False):
        """
        Scale the vector by a scalar value.

        Args:
            scalar (float): The value to scale the vector by.
            inplace (bool, optional): If True, the current vector is modified in-place.
                                      If False, a new vector is created. Defaults to False.

        Returns:
            Vector: The resulting vector after scaling.
        """
        vector = self if inplace else self.copy()
        vector.x *= scalar
        vector.y *= scalar

        return vector
