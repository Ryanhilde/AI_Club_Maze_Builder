from df_maze import Maze
import turtle  # import turtle library
import sys
import time
from collections import deque

# Maze dimensions (ncols, nrows)
nx, ny = 10, 8
# Maze entry position
ix, iy = 0, 0

# Create an instance variable to represent the Maze
maze = Maze(nx, ny, ix, iy)
maze.make_maze()

# Write the maze to a svg file
maze.write_svg('maze.svg')
maze_builder = str(maze).split(",")

# Setup lists to traverse the visual representation
walls = []
path = []
visited = set()
frontier = deque()
solution = {}  # solution dictionary

# Setup variables for the GUI window
wn = turtle.Screen()  # define the turtle screen
wn.bgcolor("black")  # set the background colour
wn.title("A Maze Solving Program")
wn.setup(1300, 700)  # setup the dimensions of the working window


# this is the class for the Maze
class MazeRepresentation(turtle.Turtle):  # define a Maze class
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")  # the turtle shape
        self.color("white")  # colour of the turtle
        self.penup()  # lift up the pen so it do not leave a trail
        self.speed(0)


# This is the class for the finish line - green square in the maze
class Green(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)


class Blue(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)


# This is the class for the start line - red square in the maze
class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)


class Yellow(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("yellow")
        self.penup()
        self.speed(0)


# set up classes
maze = MazeRepresentation()
red = Red()
blue = Blue()
green = Green()
yellow = Yellow()
done = False


def setup_maze(maze_builder):  # define a function called setup_maze
    global start_x, start_y, end_x, end_y  # set up global variables for start and end locations
    for y in range(len(maze_builder)):  # read in the grid line by line
        for x in range(len(maze_builder[y])):  # read each cell in the line
            character = maze_builder[y][x]  # assign the varaible "character" the the x and y location od the grid
            screen_x = -588 + (x * 24)  # move to the x location on the screen staring at -588
            screen_y = 288 - (y * 24)  # move to the y location of the screen starting at 288

            if character == "+":
                maze.goto(screen_x, screen_y)  # move pen to the x and y locaion and
                maze.stamp()  # stamp a copy of the turtle on the screen
                walls.append((screen_x, screen_y))  # add coordinate to walls list

            if character == " " or character == "e":
                path.append((screen_x, screen_y))  # add " " and e to path list

            if character == "e":
                green.color("purple")
                green.goto(screen_x, screen_y)  # send green sprite to screen location
                end_x, end_y = screen_x, screen_y  # assign end locations variables to end_x and end_y
                green.stamp()
                green.color("green")

            if character == "s":
                start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                red.goto(screen_x, screen_y)


def endProgram():
    wn.exitonclick()
    sys.exit()


def search(x, y):
    frontier.append((x, y))
    solution[x, y] = x, y

    while len(frontier) > 0:  # exit while loop when frontier queue equals zero
        time.sleep(0)
        x, y = frontier.popleft()  # pop next entry in the frontier queue an assign to x and y location

        if (x - 24, y) in path and (x - 24, y) not in visited:  # check the cell on the left
            cell = (x - 24, y)
            solution[cell] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            frontier.append(cell)  # add cell to frontier list
            visited.add((x - 24, y))  # add cell to visited list

        if (x, y - 24) in path and (x, y - 24) not in visited:  # check the cell down
            cell = (x, y - 24)
            solution[cell] = x, y
            frontier.append(cell)
            visited.add((x, y - 24))

        if (x + 24, y) in path and (x + 24, y) not in visited:  # check the cell on the  right
            cell = (x + 24, y)
            solution[cell] = x, y
            frontier.append(cell)
            visited.add((x + 24, y))

        if (x, y + 24) in path and (x, y + 24) not in visited:  # check the cell up
            cell = (x, y + 24)
            solution[cell] = x, y
            frontier.append(cell)
            visited.add((x, y + 24))
        green.goto(x, y)
        green.stamp()


def backRoute(x, y):
    yellow.goto(x, y)
    yellow.stamp()
    while (x, y) != (start_x, start_y):  # stop loop when current cells == start cell
        yellow.goto(solution[x, y])  # move the yellow sprite to the key value of solution ()
        yellow.stamp()
        x, y = solution[x, y]  # "key value" now becomes the new key


fin = False
cor_path = []


def depth_first_search(x, y, ex, ey, fin):
    rec_fin = False
    visited.add((x, y))
    cor_path.append((x, y))
    green.goto(x, y)
    green.stamp()
    if x == ex and y == ey:
        """end case"""
        fin = True
    elif not fin:
        """recursively checking neighboring cells"""
        if (x - 24, y) in path and (x - 24, y) not in visited:
            rec_fin = depth_first_search(x - 24, y, ex, ey, fin)
            if rec_fin is True:
                fin = rec_fin
        if (x, y - 24) in path and (x, y - 24) not in visited:
            rec_fin = depth_first_search(x, y - 24, ex, ey, fin)
            if rec_fin is True:
                fin = rec_fin
        if (x + 24, y) in path and (x + 24, y) not in visited:
            rec_fin = depth_first_search(x + 24, y, ex, ey, fin)
            if rec_fin is True:
                fin = rec_fin
        if (x, y + 24) in path and (x, y + 24) not in visited:
            rec_fin = depth_first_search(x, y + 24, ex, ey, fin)
            if rec_fin is True:
                fin = rec_fin

    if not fin:
        """recursion ends w/out exit -> dead end"""
        cor_path.remove((x, y))
    return fin


def print_path():
    # print cells that were visited but not declared dead ends (on path)
    for x, y in cor_path:
        yellow.goto(x, y)
        yellow.stamp()
        if (x, y) == (end_x, end_y):
            break


# main program starts here ####
setup_maze(maze_builder)
search(start_x, start_y)
backRoute(end_x, end_y)

# depth_first_search(start_x,start_y,end_x,end_y,fin)
# print_path()
wn.exitonclick()
