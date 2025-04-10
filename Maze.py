import random

import arcade

from HeapObject import HeapObject
from Scene import Scene
from glob import glob
from BinarySearchTree import BST


#Gold is Treasure, Blue is Map, Black is Dijkstra Probe, Green is Robot, Purple is Breadth, Bronze is Depth
class Maze(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.finished = False
        files = glob('Pics/*.jpg')
        self.start_screen = True
        self.maze_array = []
        self.current_index = (0, 0)
        self.treasures = [(0, 5), (5, 0), (5, 5)]
        self.current_energy = 200
        self.score = 0
        self.queue = []
        self.stack = []
        self.checked = []
        self.HeapTree = []
        self.num_elements = 81
        # self.map = (random.randint(0, 5), random.randint(0, 5))
        self.map = (1, 1)
        self.show_map = False
        self.cheap_probe = (0, 0)
        self.show_cheap_probe = False
        self.breadth_probe = (0, 0)
        self.show_breadth_probe = False
        self.breadth_dictionary = {}
        self.breadth_target = (-1, -1)
        self.breadth_list = []
        self.show_depth_probe = False
        self.depth_probe = (0, 0)
        self.depth_dictionary = {}
        self.depth_target = (-1, -1)
        self.depth_list = []
        self.picked_up_breadth = False
        self.picked_up_depth = False
        self.show_robot = False
        self.robot = (0, 0)
        self.robot_energy = 200
        for i in range(9):
            self.maze_array.append([])
            for j in range(9):
                if i == 0 and j == 0:
                    self.maze_array[i].append(Scene(files[i * 3 + j], key=0))
                else:
                    self.maze_array[i].append(Scene(files[i * 3 + j]))
        for i in range(9):
            for j in range(9):
                self.maze_array[i][j].current = (i, j)
                if j != 8:
                    self.maze_array[i][j].right = self.maze_array[i][j + 1]
                if i != 8:
                    self.maze_array[i][j].down = self.maze_array[i + 1][j]
                if j != 0:
                    self.maze_array[i][j].left = self.maze_array[i][j - 1]
                if i != 0:
                    self.maze_array[i][j].up = self.maze_array[i - 1][j]
        #Assigning costs to paths
        for i in range(9):
            for j in range(9):
                if j > 0:
                    self.maze_array[i][j].cost_left = random.randint(1, 10)
                if j < 8:
                    self.maze_array[i][j].cost_right = random.randint(1, 10)
                if i > 0:
                    self.maze_array[i][j].cost_up = random.randint(1, 10)
                if i < 8:
                    self.maze_array[i][j].cost_down = random.randint(1, 10)

    def get_score(self):
        return self.score

    def on_draw(self):
        if self.finished:
            arcade.close_window()
        elif self.start_screen:
            arcade.draw_text('Press the button to begin:', 150, 300, font_size=40)
            arcade.draw_text('Finish the maze. Find items along the way', 50, 260, font_size=20)
            arcade.draw_text('Gold is Treasure, Blue is a Map, Black is Probe to find a cheap path', 50, 230,
                             font_size=20)
            arcade.draw_text('Purple and Bronze find paths to treasure, Green is a robot that', 50, 200, font_size=20)
            arcade.draw_text('gets the treasure based on paths found', 50, 170, font_size=20)
            arcade.draw_rectangle_filled(400, 100, 80, 40, arcade.color.MAGENTA)
        elif self.current_energy < 0:
            arcade.draw_text('GAMEOVER - points: ' + str(self.score), 200, 300, font_size=30)
            self.finished = True
        elif self.current_index == (8, 8):
            arcade.draw_text('You Won!! - points: ' + str(self.score), 200, 300, font_size=30)
            self.finished = True

        else:

            arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height,
                                                self.maze_array[self.current_index[0]][
                                                    self.current_index[1]].background)
            arcade.draw_text('energy: ' + str(self.current_energy), 30, 30, arcade.color.MAGENTA, font_size=20)
            arcade.draw_text('score: ' + str(self.score), 700, 570, arcade.color.MAGENTA, font_size=20)

            arcade.draw_rectangle_filled(100, 300, 40, 40, arcade.color.MAGENTA)
            arcade.draw_rectangle_filled(700, 300, 40, 40, arcade.color.MAGENTA)
            arcade.draw_rectangle_filled(400, 75, 40, 40, arcade.color.MAGENTA)
            arcade.draw_rectangle_filled(400, 525, 40, 40, arcade.color.MAGENTA)

            for loc in self.treasures:
                if self.current_index == loc:
                    arcade.draw_rectangle_filled(400, 300, 40, 40, arcade.color.GOLD)
            if self.map == self.current_index:
                arcade.draw_rectangle_filled(200, 300, 40, 40, arcade.color.BLUE)
            if self.show_map:
                for i in range(8):
                    print()
                    for j in range(8):
                        if self.current_index == (i, j):
                            print('X, ', end="")
                        elif (i, j) in self.treasures:
                            print('!, ', end="")
                        else:
                            print('_, ', end="")
                self.show_map = False
            if self.cheap_probe == self.current_index:
                arcade.draw_rectangle_filled(600, 300, 40, 40, arcade.color.BLACK)
            if self.show_cheap_probe:
                print(self.dikjstra())
                self.show_cheap_probe = False

            if self.show_breadth_probe:
                print(self.breadth_first_search())
                self.show_breadth_probe = False

            if self.show_depth_probe:
                print(self.depth_first_search())
                self.show_depth_probe = False

            if self.current_index == self.breadth_probe:
                arcade.draw_rectangle_filled(200, 500, 40, 40, arcade.color.PURPLE)
            if self.current_index == self.depth_probe:
                arcade.draw_rectangle_filled(600, 500, 40, 40, arcade.color.BRONZE)
            if self.robot == self.current_index:
                arcade.draw_rectangle_filled(200, 100, 40, 40, arcade.color.GREEN)

    def update(self, delta_time):
        if self.finished:
            self.finish_game()  # Close window and handle cleanup
            return
    def finish_game(self):
        arcade.close_window()  # Close the game window safely
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.start_screen:
            if 360 <= x <= 440 and 80 <= y <= 120:
                self.start_screen = False
        elif self.finished == False:
            if 280 <= y <= 320:
                if 80 <= x <= 120:
                    if self.maze_array[self.current_index[0]][self.current_index[1]].left is not None:
                        self.current_index = self.maze_array[self.current_index[0]][self.current_index[1]].left.current
                        self.current_energy -= self.maze_array[self.current_index[0]][self.current_index[1]].cost_left
                if 680 <= x <= 720:
                    if self.maze_array[self.current_index[0]][self.current_index[1]].right is not None:
                        self.current_index = self.maze_array[self.current_index[0]][self.current_index[1]].right.current
                        self.current_energy -= self.maze_array[self.current_index[0]][self.current_index[1]].cost_right
            if 380 <= x <= 420:
                if 55 <= y <= 95:
                    if self.maze_array[self.current_index[0]][self.current_index[1]].down is not None:
                        self.current_index = self.maze_array[self.current_index[0]][self.current_index[1]].down.current
                        self.current_energy -= self.maze_array[self.current_index[0]][self.current_index[1]].cost_down
                if 505 <= y <= 545:
                    if self.maze_array[self.current_index[0]][self.current_index[1]].up is not None:
                        self.current_index = self.maze_array[self.current_index[0]][self.current_index[1]].up.current
                        self.current_energy -= self.maze_array[self.current_index[0]][self.current_index[1]].cost_up

                if self.current_index in self.treasures:
                    if 380 <= x <= 420 and 280 <= y <= 320:
                        self.score += 1
                        self.treasures.remove(self.current_index)
            if self.current_index == self.map:
                if 180 <= x <= 220 and 280 <= y <= 320:
                    self.map = (-1, -1)
                    self.show_map = True
            if self.current_index == self.cheap_probe:
                if 580 <= x <= 620 and 280 <= y <= 320:
                    self.cheap_probe = (-1, -1)
                    self.show_cheap_probe = True
            if self.current_index == self.breadth_probe:
                if 180 <= x <= 220 and 480 <= y <= 520:
                    self.breadth_probe = (-1, -1)
                    self.show_breadth_probe = True
                    self.picked_up_breadth = True
            if self.current_index == self.depth_probe:
                if 580 <= x <= 620 and 480 <= y <= 520:
                    self.depth_probe = (-1, -1)
                    self.show_depth_probe = True
                    self.picked_up_depth = True

            if self.current_index == self.robot:
                pass
            if 180 <= x <= 220 and 80 <= y <= 120:
                if self.picked_up_breadth:
                    self.robot = (-1, -1)
                    if self.robot_send(self.breadth_list):
                        self.score += 1
                        self.treasures.remove(self.breadth_list[len(self.breadth_list) - 1])
                        self.picked_up_breadth = False
                    else:
                        print("Not enough energy")
                elif self.picked_up_depth:
                    self.robot = (-1, -1)
                    if self.robot_send(self.depth_list):
                        self.score += 1
                        self.treasures.remove(self.depth_list[len(self.depth_list) - 1])
                        self.picked_up_depth = False
                    else:
                        print("Not enough energy")

    def get_direction(self, current_pos, next_pos):
        """ Determines the direction based on the position change """
        if next_pos[0] == current_pos[0]:
            if next_pos[1] > current_pos[1]:
                return 'right'
            elif next_pos[1] < current_pos[1]:
                return 'left'
        elif next_pos[1] == current_pos[1]:
            if next_pos[0] > current_pos[0]:
                return 'down'
            elif next_pos[0] < current_pos[0]:
                return 'up'
        return None  # No valid direction if the positions are not adjacent

    def robot_send(self, list):
        current_pos = list[0]
        for i in range(1, len(list)):
            next_pos = list[i]

            direction = self.get_direction(current_pos, next_pos)

            if direction is None:
                return False  # Invalid direction, not adjacent

            # Retrieve the Scene object at the current position
            current_scene = self.maze_array[current_pos[0]][current_pos[1]]
            move_cost = current_scene.get_cost(direction)

            if self.robot_energy < move_cost:
                return False
            else:
                self.robot_energy -= move_cost
            current_pos = next_pos

        return True

    def breadth_first_search(self):
        self.queue = []
        self.queue.append(self.maze_array[0][0])
        self.checked = [False] * 81
        self.checked[0] = True
        self.breadth_dictionary[(0, 0)] = None
        for box in self.queue:
            i, j = box.current[0], box.current[1]

            # check right
            if j + 1 < 9:
                if not self.checked[i * 9 + j + 1]:
                    self.queue.append(self.maze_array[i][j + 1])
                    self.checked[i * 9 + j + 1] = True
                    self.breadth_dictionary[self.maze_array[i][j + 1].current] = box.current
                    if self.maze_array[i][j + 1].current in self.treasures:
                        self.breadth_target = self.maze_array[i][j + 1].current
                        break
            # check left
            if j - 1 > -1:
                if not self.checked[i * 9 + j - 1]:
                    self.queue.append(self.maze_array[i][j - 1])
                    self.checked[i * 9 + j - 1] = True
                    self.breadth_dictionary[self.maze_array[i][j - 1].current] = box.current
                    if self.maze_array[i][j - 1].current in self.treasures:
                        self.breadth_target = self.maze_array[i][j - 1].current
                        break

            # check up
            if i - 1 > -1:
                if not self.checked[(i - 1) * 9 + j]:
                    self.queue.append(self.maze_array[i - 1][j])
                    self.checked[(i - 1) * 9 + j] = True
                    self.breadth_dictionary[self.maze_array[i - 1][j].current] = box.current
                    if self.maze_array[i - 1][j].current in self.treasures:
                        self.breadth_target = self.maze_array[i - 1][j].current
                        break
            # check down
            if i + 1 < 9:
                if not self.checked[(i + 1) * 9 + j]:
                    self.queue.append(self.maze_array[i + 1][j])
                    self.checked[(i + 1) * 9 + j] = True
                    self.breadth_dictionary[self.maze_array[i + 1][j].current] = box.current
                    if self.maze_array[i + 1][j].current in self.treasures:
                        self.breadth_target = self.maze_array[i + 1][j].current
                        break
        if self.breadth_target != (-1, -1):
            self.breadth_list = self.cheapest_path(self.breadth_dictionary, self.breadth_target)
            print(self.breadth_list)

    def depth_first_search(self):
        self.stack = []
        self.stack.append(self.maze_array[0][0])
        self.checked = [False] * 81
        self.checked[0] = True
        self.depth_dictionary[(0, 0)] = None

        while len(self.stack) > 0:
            box = self.stack.pop()
            i, j = box.current[0], box.current[1]

            #up
            if i - 1 > -1:
                if not self.checked[(i - 1) * 9 + j]:
                    self.stack.append(self.maze_array[i - 1][j])
                    self.checked[(i - 1) * 9 + j] = True
                    self.depth_dictionary[self.maze_array[i - 1][j].current] = box.current
                    if self.maze_array[i - 1][j].current in self.treasures:
                        self.depth_target = self.maze_array[i - 1][j].current
                        break

            #right
            if j + 1 < 9:
                if not self.checked[i * 9 + j + 1]:
                    self.stack.append(self.maze_array[i][j + 1])
                    self.checked[i * 9 + j + 1] = True
                    self.depth_dictionary[self.maze_array[i][j + 1].current] = box.current
                    if self.maze_array[i][j + 1].current in self.treasures:
                        self.depth_target = self.maze_array[i][j + 1].current
                        break
            #down
            if i + 1 < 9:
                if not self.checked[(i + 1) * 9 + j]:
                    self.stack.append(self.maze_array[i + 1][j])
                    self.checked[(i + 1) * 9 + j] = True
                    self.depth_dictionary[self.maze_array[i + 1][j].current] = box.current
                    if self.maze_array[i + 1][j].current in self.treasures:
                        self.depth_target = self.maze_array[i + 1][j].current
                        break
            #left
            if j - 1 > -1:
                if not self.checked[i * 9 + j - 1]:
                    self.stack.append(self.maze_array[i][j - 1])
                    self.checked[i * 9 + j - 1] = True
                    self.depth_dictionary[self.maze_array[i][j - 1].current] = box.current
                    if self.maze_array[i][j - 1].current in self.treasures:
                        self.depth_target = self.maze_array[i][j - 1].current
                        break
        if self.depth_target != (-1, -1):
            self.depth_list = self.cheapest_path(self.depth_dictionary, self.depth_target)
            print(self.depth_list)

    def decrease_key(self, index, new_key):
        subject = self.HeapTree[index]
        subject.key = new_key
        if index > 0:
            if self.HeapTree[(index - 1) // 2].key > new_key:
                self.HeapTree[index] = self.HeapTree[(index - 1) // 2]
                self.HeapTree[(index - 1) // 2] = subject
                self.decrease_key((index - 1) // 2, new_key)

    def extract_min(self):
        minimum = self.HeapTree[0]
        self.HeapTree[0] = self.HeapTree[self.num_elements - 1]
        self.HeapTree[self.num_elements - 1] = None
        self.num_elements -= 1
        self.heapify(0)
        return minimum

    def heapify(self, index):
        element = self.HeapTree[index]
        if index * 2 + 1 < self.num_elements:
            if self.HeapTree[index * 2 + 1] is not None:
                smallest = self.HeapTree[index * 2 + 1]
                if self.HeapTree[index * 2 + 2] is not None:
                    if smallest.key > self.HeapTree[index * 2 + 2].key:
                        if element.key > self.HeapTree[index * 2 + 2].key:
                            self.HeapTree[index] = self.HeapTree[index * 2 + 2]
                            self.HeapTree[index * 2 + 2] = element
                        self.heapify(index * 2 + 2)
                    else:
                        if smallest.key < element.key:
                            self.HeapTree[index] = smallest
                            self.HeapTree[index * 2 + 1] = element
                        self.heapify(index * 2 + 1)

    def cheapest_path(self, dictionary, target):
        current = target
        path = []

        while current is not None:
            path.append(current)
            current = dictionary[current]
        path.reverse()
        return path

    def dikjstra(self):
        for i in range(9):
            for j in range(9):
                self.HeapTree.append(self.maze_array[i][j])

        pred_dict = {}
        pred_dict[(0, 0)] = None
        current_node = self.extract_min()
        while current_node is not None:
            if current_node.current[0] < 8 and current_node.right in self.HeapTree and current_node.right is not None:
                if current_node.key + current_node.cost_right < current_node.right.key:
                    self.decrease_key(self.HeapTree.index(current_node.right),
                                      current_node.key + current_node.cost_right)
                    pred_dict[current_node.right.current] = current_node.current
            if current_node.current[0] > 0 and current_node.left in self.HeapTree and current_node.left is not None:
                if current_node.key + current_node.cost_left < current_node.left.key:
                    self.decrease_key(self.HeapTree.index(current_node.left),
                                      current_node.key + current_node.cost_left)
                    pred_dict[current_node.left.current] = current_node.current
            if current_node.current[1] < 8 and current_node.down in self.HeapTree and current_node.down is not None:
                if current_node.key + current_node.cost_down < current_node.down.key:
                    self.decrease_key(self.HeapTree.index(current_node.down),
                                      current_node.key + current_node.cost_down)
                    pred_dict[current_node.down.current] = current_node.current
            if current_node.current[1] > 0 and current_node.up in self.HeapTree and current_node.up is not None:
                if current_node.key + current_node.cost_up < current_node.up.key:
                    self.decrease_key(self.HeapTree.index(current_node.up),
                                      current_node.key + current_node.cost_up)
                    pred_dict[current_node.up.current] = current_node.current
            if self.HeapTree[0] is None:
                pred_dict[(8, 8)] = current_node.current
            current_node = self.extract_min()
        return self.cheapest_path(pred_dict, (8, 8))


def read_scores_from_file(filename):
    bst = BST()
    try:
        with open(filename, "r") as file:
            for line in file:
                name, score = line.strip().split(',')
                bst.insert(name, int(score))
    except ValueError:
        print("Empty")
    return bst


def write_scores_to_file(filename, bst):
    with open(filename, "w") as file:
        scores = bst.in_order()
        for name, score in scores:
            file.write(f"{name},{score}\n")


# Ask for someone's name
name = input("What's your name? ")
filename = "scores.txt"
bst = read_scores_from_file(filename)
try:
    player_name = input("Enter the player's name to search: ")
    score = bst.searchRecursively(player_name)
    print(f"{player_name}'s score is {score}.")
except AttributeError:
    print("Empty")
maze = Maze(800, 600, "Maze Game")
arcade.window = maze
arcade.run()

bst.insert(name, maze.get_score())
print(f"Score for {name} added.")
write_scores_to_file(filename, bst)
print("Scores saved to file. Exiting...")
