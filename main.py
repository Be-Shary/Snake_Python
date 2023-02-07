import pgzrun
import random


class Snake:
    def __init__(self, x, y):
        self.cords = [{'x': x - 2, 'y': y}, {'x': x - 1, 'y': y}, {'x': x, 'y': y}]
        self.color = [(200,200,200), (0,200,0)]
        self.direct = "RIGHT"
        self.grown = False
        self.crash = False
        self.score = 0
        self.x = x
        self.y = y

    def draw(self):
        for part in self.cords:
            if not self.crash:
                screen.draw.filled_rect(Rect((part['x'] * CELL, part['y'] * CELL), (CELL - 1, CELL -1)), self.color[1])
            else:
                screen.draw.filled_rect(Rect((part['x'] * CELL, part['y'] * CELL), (CELL - 1, CELL - 1)), self.color[0])

    def move(self):
        if self.direct == "RIGHT":
            if self.x < ROW_X - 1:
                self.x += 1
            else:
                self.x = 0
        elif self.direct == "LEFT":
            if self.x > 0:
                self.x -= 1
            else:
                self.x = ROW_X - 1
        elif self.direct == "UP":
            if self.y > 0:
                self.y -= 1
            else:
                self.y = ROW_Y - 1
        elif self.direct == "DOWN":
            if self.y < ROW_Y - 1:
                self.y += 1
            else:
                self.y = 0

        player.collidetect()
        self.cords.append({'x': self.x, 'y': self.y})

        if not self.grown:
            self.cords.remove(self.cords[0])
        else:
            self.grown = False

    def eat(self, x, y):
        if self.x == x and self.y == y:
            self.score += 10
            self.grown = True
            return True
        return False

    def collidetect(self):
        for part in self.cords[:-1]:
            if self.x == part['x'] and self.y == part['y']:
                self.crash = True

    def reset_snake(self):
        self.score = 0
        self.cords = []
        self.grown = False
        self.crash = False
        self.direct = "RIGHT"
        self.x = round(ROW_X / 2)
        self.y = round(ROW_Y / 2)
        self.cords = [{'x': self.x - 2, 'y': self.y}, {'x': self.x - 1, 'y': self.y}, {'x': self.x, 'y': self.y}]


class Food:
    def __init__(self):
        self.make_food()

    def draw(self):
        screen.draw.filled_rect(Rect((self.x * CELL, self.y * CELL), (CELL - 1, CELL - 1)), (180, 20, 20))

    def make_food(self):
        self.x = random.randint(0, ROW_X - 1)
        self.y = random.randint(0, ROW_Y - 1)


#some vars
CELL = 25
ROW_X = 20
ROW_Y = 20
WIDTH = ROW_X * CELL
HEIGHT = ROW_Y * CELL + CELL
timer = 0
player = Snake(round(ROW_X / 2), round(ROW_Y / 2))
food = Food()


def keyboard_check():
    if keyboard.RIGHT:
        if not player.direct == "LEFT":
            player.direct = "RIGHT"
    if keyboard.LEFT:
        if not player.direct == "RIGHT":
            player.direct = "LEFT"
    if keyboard.UP:
        if not player.direct == "DOWN":
            player.direct = "UP"
    if keyboard.DOWN:
        if not player.direct == "UP":
            player.direct = "DOWN"


def update(time):
    global timer

    timer += time

    if player.crash and timer > 3:
        timer = 0
        food.make_food()
        player.reset_snake()

    keyboard_check()
    if timer > 0.10 and not player.crash:
        timer = 0
        player.move()

    if player.eat(food.x, food.y):
        food.make_food()


def draw():
    screen.clear()
    for y in range(ROW_Y):
        for x in range(ROW_X):
            screen.draw.filled_rect(Rect((x * CELL, y * CELL), (CELL - 1, CELL - 1)), (20, 20, 150))
    player.draw()
    food.draw()
    screen.draw.text("Score: " + str(player.score), (20, HEIGHT - CELL), color=(255, 0, 0), fontname="arcade", fontsize=16, shadow=(2,2))


pgzrun.go()