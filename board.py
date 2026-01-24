# board.py
import random
from food import Food
import snake


class Board:
    """
    Board class representing the game board.
    """


    ################### ATTRIBUTES #####################

    _size: int = 10
    _gameOver: bool = False
    _score: int = 0
    _snake: snake.Snake = None
    _food: list[Food] = []


    ################### CONSTRUCTOR #####################

    def __init__(self, size=10):
        """
        Initialize the board with a given size.
        """
        self.set_size(size)
        self.set_gameOver(False)
        self.set_score(0)
        self.set_snake()
        self.set_food()


    def reset(self):
        self.set_gameOver(False)
        self.set_score(0)
        self.set_snake()
        self.set_food()

    ################### SETTERS #####################

    def set_size(self, size: int):
        """
        Set the size of the board.
        """
        self._size = size

    def set_snake(self):
        """
        Set the snake object on the board.
        """
        while (True):
            random_direction = self.get_random_direction()
            random_position = self.generate_random_position()

            if random_position[0] > 2 and random_position[0] < self._size - 2 and random_position[1] > 2 and random_position[1] < self._size - 2:
                break
        
        _snake = snake.Snake(random_position, random_direction)
        self._snake = _snake

    def set_food(self):
        """
        Set the food objects on the board.
        """
        food_list = []
        for color in ["RED", "GREEN", "GREEN"]:
            position = self.generate_random_position()
            food_item = Food(position, color)
            food_list.append(food_item)
        self._food = food_list

    def set_score(self, score: int):
        """
        Set the current score of the game.
        """
        self._score = score

    def set_gameOver(self, status: bool):
        """
        Set the game over status.
        """
        self._gameOver = status

    
    ################### GETTERS #####################

    def get_size(self) -> int:
        """
        Get the size of the board.
        """
        return self._size
    
    def get_snake(self) -> snake.Snake:
        """
        Get the snake object on the board.
        """
        return self._snake
    
    def get_food(self) -> list[Food]:
        """
        Get the food objects on the board.
        """
        return self._food
    
    def get_score(self) -> int:
        """
        Get the current score of the game.
        """
        return self._score
    
    def is_gameOver(self) -> bool:
        """
        Check if the game is over.
        """
        return self._gameOver


    ################### METHODS #####################
        
    def generate_random_position(self) -> tuple:
        """
        Generate a random position on the board that is not occupied.
        """
        occupied_positions = set()
        if self._snake:
            for segment in self._snake.get_body():
                occupied_positions.add(segment)
        if self._food:
            for food_item in self._food:
                occupied_positions.add(food_item.get_position())
        
        while True:
            position = (random.randint(0, self._size - 1), random.randint(0, self._size - 1))
            if position not in occupied_positions:
                occupied_positions.add(position)
                return position
            
    def get_random_direction(self) -> str:
        """
        Get a random direction for the snake.
        """
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        return random.choice(directions)
    
    def increase_score(self, points: int):
        """
        Increase the current score by a given number of points.
        """
        self._score += points

    def decrease_score(self, points: int):
        """
        Decrease the current score by a given number of points.
        """
        self._score -= points

    def remove_food_at_position(self, position: tuple):
        """
        Remove the food item at the given position.
        """
        self._food = [food for food in self._food if food.get_position() != position]

    def add_food(self, color: str):
        """
        Add a new food item at a random position.
        """
        position = self.generate_random_position()
        food_item = Food(position, color)
        self._food.append(food_item)

    def is_valid_position(self, position: tuple) -> bool:
        """
        Check if the given position is within the board boundaries.
        """
        x, y = position
        return 0 <= x < self._size and 0 <= y < self._size

    def verify_collision(self, position: tuple) -> bool:
        """
        Verify if the given position collides with the snake's body.
        """
        if (not self.is_valid_position(position) or position in self._snake.get_body()):
            self._gameOver = True
            return True
    
    def update(self):
        """
        Update the board state.
        """
        if self._gameOver:
            return
        
        next_position = self._snake.get_next_head()

        if self.verify_collision(next_position):
            return
        
        for food_item in self._food:
            if food_item.get_position() == next_position:
                item_color = food_item.get_color()
                self._snake.eat(item_color)
                if item_color == "GREEN":
                    self.increase_score(10)
                elif item_color == "RED":
                    self.decrease_score(10)

                self.remove_food_at_position(next_position)
                self.add_food(food_item.get_color())
                break
        if self._snake.is_alive():
            self._snake.move(next_position)
        else:
            self._gameOver = True