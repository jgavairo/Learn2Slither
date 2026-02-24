# board.py
import random
import time
from food import Food
import snake

# Toggle verbose debugging (disabled by default to avoid flooding the UI)
DEBUG = False


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
        if self.set_snake() == 404:
            self.set_gameOver(True)
            return
        self.set_food()


    def reset(self):
        self.set_gameOver(False)
        self.set_score(0)
        if self.set_snake() == 404:
            self.set_gameOver(True)
            return
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

        attempts = 0
        random_direction = None
        random_position = None

        # When re-placing the snake (reset), avoid treating the old snake
        # body as occupied — otherwise generate_random_position may never
        # find a valid interior spot. Only consider food positions as occupied.
        occupied_for_placement = set()
        if self._food:
            for f in self._food:
                occupied_for_placement.add(f.get_position())

        while True:
            try:
                attempts += 1
                random_direction = self.get_random_direction()
                random_position = self.generate_random_position(occupied_positions=occupied_for_placement)
            except ValueError:
                return 404

            if (random_position[0] > 2 and random_position[0] < self._size - 2
                    and random_position[1] > 2 and random_position[1] < self._size - 2):
                break

            if DEBUG and attempts % 50 == 0:
                print(f"[DEBUG][set_snake] attempt={attempts} pos={random_position} size={self._size}")

            # Safety guard to avoid infinite loop on tiny boards
            if attempts > 2000:
                raise RuntimeError(f"Unable to place snake after {attempts} attempts. Board size={self._size}")

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
    def get_occupied_positions(self) -> set:
        """
        Get a set of positions occupied by the snake and food.
        """
        occupied_positions = set()
        if self._snake:
            for segment in self._snake.get_body():
                occupied_positions.add(segment)
        if self._food:
            for food_item in self._food:
                occupied_positions.add(food_item.get_position())
        return occupied_positions

    def generate_random_position(self, occupied_positions: set = None) -> tuple:
        """
        Generate a random position on the board that is not occupied.
        """
        if occupied_positions is None:
            occupied_positions = self.get_occupied_positions()
        if len(occupied_positions) >= self._size * self._size:
            raise ValueError("No available positions on the board.")
        
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
        # Build the set of all board positions
        all_positions = {(x, y) for x in range(self._size) for y in range(self._size)}
        occupied = self.get_occupied_positions()

        # Free positions are those not occupied by snake or existing food
        free_positions = list(all_positions - occupied)
        if not free_positions:
            # No available cell to place new food
            return 404

        # Choose a random free cell deterministically from the available ones
        position = random.choice(free_positions)
        food_item = Food(position, color)
        self._food.append(food_item)
        return position

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

    def display_vision(self):
        """
        Affiche la vision du serpent de manière linéaire et lisible.
        Exemple: UP : 0 0 G 0 W
        """
        head_pos = self._snake.get_body()[0]
        directions = {
            "UP": (0, -1),
            "DOWN": (0, 1),
            "LEFT": (-1, 0),
            "RIGHT": (1, 0),
        }

        print(f"\nVision (from Head):")
        
        for name, (dx, dy) in directions.items():
            x, y = head_pos
            line_symbols = []
            
            # On avance dans la direction jusqu'à heurter un mur ou le corps
            while True:
                x += dx
                y += dy
                
                symbol = self._symbol_at((x, y))
                line_symbols.append(symbol)
                
                # La vision s'arrête au premier obstacle bloquant (Mur ou Corps)
                if symbol in ["W"]:
                    break
            
            # On joint les symboles avec un espace pour la lisibilité
            print(f"{name:5} : {' '.join(line_symbols)}")
        print("")

    def get_snake_vision(self) -> dict[str, list[int]]:
        """
        Return the snake vision in 4 directions from its head up to the wall.
        Each direction includes the head symbol as the first element.
        """
        head_x, head_y = self._snake.get_body()[0]
        directions = {
            "UP": (0, -1),
            "LEFT": (-1, 0),
            "DOWN": (0, 1),
            "RIGHT": (1, 0),
        }

        vision: dict[str, list[int]] = {}
        for name, (dx, dy) in directions.items():
            wall_distance: int = 0
            green_apple_distance: int = 0
            red_apple_distance: int = 0
            steps: int = 0

            x, y = head_x, head_y
            iteration = 0
            start_t = time.perf_counter()
            max_steps = max(self._size * 3, 100)  # safety guard
            if DEBUG:
                print(f"[DEBUG][vision] direction={name} head=({head_x},{head_y}) dx={dx} dy={dy} max_steps={max_steps}")

            while True:
                iteration += 1
                x += dx
                y += dy
                steps += 1

                if DEBUG:
                    elapsed = time.perf_counter() - start_t
                    in_body = (x, y) in self._snake.get_body()
                    symbol = self._symbol_at((x, y)) if self.is_valid_position((x, y)) else 'W'
                    print(f"[DEBUG][vision] dir={name} iter={iteration} pos=({x},{y}) steps={steps} sym={symbol} in_body={in_body} elapsed={elapsed:.6f}s")

                # Safety: break if we go beyond reasonable steps
                if steps > max_steps:
                    print(f"[DEBUG][vision][ERROR] exceeded max_steps={max_steps} in direction={name}; breaking")
                    wall_distance = steps
                    break

                if not self.is_valid_position((x, y)) or (x, y) in self._snake.get_body():
                    wall_distance = steps
                    if DEBUG:
                        print(f"[DEBUG][vision] hit wall/body at ({x},{y}) after {steps} steps")
                    break

                symbol = self._symbol_at((x, y))
                if symbol == "G" and green_apple_distance == 0:
                    green_apple_distance = steps
                    if DEBUG:
                        print(f"[DEBUG][vision] found GREEN at ({x},{y}) steps={steps}")
                if symbol == "R" and red_apple_distance == 0:
                    red_apple_distance = steps
                    if DEBUG:
                        print(f"[DEBUG][vision] found RED at ({x},{y}) steps={steps}")
            
            vision[name] = [self.simplify_distance(wall_distance), self.simplify_distance(green_apple_distance), self.simplify_distance(red_apple_distance)]
            if DEBUG:
                print(f"[DEBUG][vision] result {name} = {vision[name]}\n")

        return vision

    def update(self):
        """
        Update the board state.
        """
        reward = 0

        if self._gameOver:
            return
        
        next_position = self._snake.get_next_head()

        if self.verify_collision(next_position):
            reward = -100
            return reward
        
        for food_item in self._food:
            if food_item.get_position() == next_position:
                item_color = food_item.get_color()
                self._snake.eat(item_color)
                if item_color == "GREEN":
                    reward = 10
                    self.increase_score(10)
                elif item_color == "RED":
                    reward = -15
                    self.decrease_score(10)

                self.remove_food_at_position(next_position)
                if (self.add_food(food_item.get_color()) == 404):
                    self._gameOver = True
                    reward = 1000
                break
        if self._snake.is_alive():
            self._snake.move(next_position)
        else:
            self._gameOver = True

        if reward == 0:
            reward = -1

        return reward