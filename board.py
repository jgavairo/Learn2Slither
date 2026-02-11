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

    def _symbol_at(self, position: tuple) -> str:
        """
        Return the symbol at a given position for snake vision.
        """
        if not self.is_valid_position(position):
            return "W"

        head = self._snake.get_body()[0]
        if position == head:
            return "H"

        if position in self._snake.get_body()[1:]:
            return "S"

        for food_item in self._food:
            if food_item.get_position() == position:
                return "G" if food_item.get_color() == "GREEN" else "R"

        return "0"

    @staticmethod
    def simplify_distance(distance: int) -> int:
        """
        Simplify the distance value for snake vision.
        0: No object
        1: Object is 1 step away
        2: Object is beetween 2 and 5 steps away
        3: Object is 6 or more steps away
        """
        match distance:
            case 0:
                return 0
            case 1:
                return 1
            case 2 | 3 | 4 | 5:
                return 2
            case _:
                return 3

    def get_snake_vision(self) -> dict[str, list[int]]:
        """
        Return the snake vision in 4 directions from its head up to the wall.
        Each direction includes the head symbol as the first element.
        """
        print (self._snake.get_body()[0])
        head_x, head_y = self._snake.get_body()[0]
        directions = {
            "UP": (0, -1),
            "LEFT": (-1, 0),
            "DOWN": (0, 1),
            "RIGHT": (1, 0),
        }

        vision: dict[str, list[int]] = {}
        for name, (dx, dy) in directions.items():
            wall_distance : int = 0
            green_apple_distance : int = 0
            red_apple_distance : int = 0
            steps : int = 0

            x, y = head_x, head_y

            while True:

                x += dx
                y += dy
                steps += 1

                if not self.is_valid_position((x, y)) or (x, y) in self._snake.get_body():
                    wall_distance = steps
                    break
                symbol = self._symbol_at((x, y))
                if symbol == "G" and green_apple_distance == 0:
                    green_apple_distance = steps
                if symbol == "R" and red_apple_distance == 0:
                    red_apple_distance = steps
            vision[name] = [self.simplify_distance(wall_distance), self.simplify_distance(green_apple_distance), self.simplify_distance(red_apple_distance)]

        return vision
    
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