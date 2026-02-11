# snake.py

#   USAGE EXAMPLE:
# # Dans Game ou Board.update()
# next_pos = self.snake.get_next_head()

# # 1. VALIDATION
# if self.is_out_of_bounds(next_pos):
#     self.gameOver = True  # Game Over, pas de malus = punition suffit
#     return

# if self.is_collision(next_pos):
#     self.gameOver = True
#     return

# # 2. SI VALIDE, le serpent bouge
# self.snake.move(next_pos)

# # 3. VÉRIFIER LES RÉCOMPENSES
# if next_pos == self.food.position:
#     self.score += 10
#     self.snake.eat()
#     self.food.spawn()

class Snake:
    """
    Snake class representing the snake in the game with her position and direction.
    """
    ################### ATTRIBUTES #####################

    _position:  tuple
    _direction: tuple
    _body:      list[tuple]
    _growing:   bool
    _is_alive:  bool


    ################### CONSTRUCTOR #####################

    def __init__(self, start_position: tuple, direction: str):
        """
        Initialize the snake with a starting position and direction.
        """
        # Ensure _direction exists before calling setter to avoid AttributeError
        self._direction = None
        self.set_direction(direction)
        self.set_position(start_position)  # body is a list of tuples
        self._growing = False
        self._is_alive = True

    ################### METHODS #####################

    ### Setters ###

    def set_direction(self, direction: str):
        """
        Set the snake's direction based on a string input.
        """
        directions = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        current_direction = getattr(self, '_direction', None)
        if direction in directions:
            # If current direction is not set yet, allow any initial direction.
            if self._direction is not None:
                if (directions[direction][0] == -self._direction[0] and
                    directions[direction][1] == -self._direction[1]):
                    return
            self._direction = directions[direction]
        else:
            raise ValueError("Invalid direction. Use 'UP', 'DOWN', 'LEFT', or 'RIGHT'.")
        
    def set_position(self, position: tuple):
        """
        Set the snake's position of entire body.
        """
        self._body = [position]
        for i in range (1, 3):  # Initial length of 3
            body_position_x = position[0] - i * self._direction[0]
            body_position_y = position[1] - i * self._direction[1]
            self._body.append((body_position_x, body_position_y))


    ### Getters ###

    def is_alive(self) -> bool:
        """
        Check if the snake is alive.
        """
        return self._is_alive
    
    def get_next_head(self) -> tuple:
        """
        Calculate the next head position based on the current direction.
        """
        head_x, head_y = self._body[0]
        next_x = head_x + self._direction[0]
        next_y = head_y + self._direction[1]
        return (next_x, next_y)
    
    def get_body(self) -> list[tuple]:
        """
        Get the current body positions of the snake.
        """
        return self._body
    
    def get_direction(self) -> tuple:
        """
        Get the current direction of the snake.
        """
        return self._direction 
    

    ### Actions ###

    def die(self):
        """
        Handle the snake's death.
        """
        self._is_alive = False

    def move(self, next_position: tuple):
        """
        Move the snake to the next position.
        """
        self._body.insert(0, next_position)  # Add new head

        if not self._growing:
            self._body.pop()  # Remove tail
        else:
            self._growing = False  # Reset growing flag

    def eat(self, color_apple: str):
        """
        Grow the snake by adding a new segment at the tail.
        """
        if color_apple == "GREEN":
            self._growing = True
        elif color_apple == "RED":
            if len(self._body) > 1:
                self._body.pop()  # Remove tail segment
            else:
                self.die()

    # def share_vision(self) -> list[tuple]:
    #     """
    #     Share the snake's body positions for vision purposes.
    #     """
    #     return self._body.copy()

