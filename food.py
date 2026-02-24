# food.py

class Food:
    """Food class representing the food item on the board."""

    # ATTRIBUTES

    _position: tuple
    _color: str

    # CONSTRUCTOR

    def __init__(self, position: tuple, color: str):
        """
        Initialize the food with a starting position.
        """
        if color not in {"RED", "GREEN"}:
            raise ValueError("Invalid color. Use 'RED' or 'GREEN'.")
        self._position = position
        self._color = color

    # METHODS

    # Getters
    def get_position(self) -> tuple:
        """
        Get the current position of the food.
        """
        return self._position

    def get_color(self) -> str:
        """Get the color of the food."""
        return self._color
