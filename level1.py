import turtle
import random
import math
import time
from ui_elements import draw_heart, create_turtle, clear_turtles

screen = turtle.Screen()
screen.title("Level 1 - 3D Drone Evasion")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

lives_display = create_turtle()
lives_display.color("cyan")

hearts_turtle_ref = None


def update_lives_display(lives):
    global hearts_turtle_ref
    
    clear_turtles(hearts_turtle_ref)
    
    lives_display.clear()
    lives_display.goto(-350, 250)
    lives_display.write("Lives:", font=("Courier", 14, "bold"))
    
    hearts_turtle_ref = create_turtle()
    for i in range(lives):
        draw_heart(hearts_turtle_ref, -280 + (i * 20), 255, size=7, color="#ff0066")
    
    hearts_turtle_ref.goto(-280 + (lives * 20) + 10, 250)


status_display = create_turtle()
status_display.color("white")
status_display.goto(0, 0)

player = turtle.Turtle()
player.hideturtle()
player.penup()
player.speed(0)
player.goto(-350, -250)


def draw_player(x, y, invincible=False):
    player.clear()
    player.goto(x, y)
    
    if not invincible or int(x * 5) % 2 == 0:
        faces = [
            (x, y - 15, x - 12, y - 25, x + 12, y - 25, "cyan" if not invincible else "light cyan"),
            (x, y - 15, x - 12, y - 25, x, y - 35, "dark cyan" if not invincible else "cyan"),
            (x, y - 15, x + 12, y - 25, x, y - 35, "light cyan" if not invincible else "white"),
        ]
        for face in faces:
            player.penup()
            player.goto(face[0], face[1])
            player.pendown()
            player.fillcolor(face[6])
            player.begin_fill()
            player.goto(face[2], face[3])
            player.goto(face[4], face[5])
            player.goto(face[0], face[1])
            player.end_fill()


key = turtle.Turtle()
key.hideturtle()
key.penup()
key.speed(0)
key_pos = [350, 250]


def draw_key():
    key.clear()
    x, y = key_pos
    
    key.penup()
    key.goto(x - 15, y - 15)
    key.pendown()
    key.fillcolor("gold")
    key.begin_fill()
    for _ in range(4):
        key.forward(30)
        key.left(90)
    key.end_fill()
    
    key.penup()
    key.goto(x - 15, y + 15)
    key.pendown()
    key.fillcolor("yellow")
    key.begin_fill()
    key.goto(x - 5, y + 25)
    key.goto(x + 25, y + 25)
    key.goto(x + 15, y + 15)
    key.goto(x - 15, y + 15)
    key.end_fill()
    
    key.penup()
    key.goto(x + 15, y - 15)
    key.pendown()
    key.fillcolor("dark goldenrod")
    key.begin_fill()
    key.goto(x + 25, y - 5)
    key.goto(x + 25, y + 25)
    key.goto(x + 15, y + 15)
    key.goto(x + 15, y - 15)
    key.end_fill()


buildings = []


class Building:
    def __init__(self, x, y, size, height):
        self.x, self.y, self.size, self.height = x, y, size, height
        self.turtle = create_turtle()
        self.draw()
    
    def draw(self):
        t = self.turtle
        x, y, size, height = self.x, self.y, self.size, self.height
        
        t.goto(x - size, y - size)
        t.pendown()
        t.fillcolor("saddle brown")
        t.begin_fill()
        for _ in range(4):
            t.forward(size * 2)
            t.left(90)
        t.end_fill()
        
        t.penup()
        t.goto(x - 8, y - size)
        t.pendown()
        t.fillcolor("dark red")
        t.begin_fill()
        for _ in range(2):
            t.forward(16)
            t.left(90)
            t.forward(20)
            t.left(90)
        t.end_fill()
        
        t.penup()
        t.goto(x - size + 8, y)
        t.pendown()
        t.fillcolor("light blue")
        t.begin_fill()
        for _ in range(4):
            t.forward(12)
            t.left(90)
        t.end_fill()
        
        t.penup()
        t.goto(x + size, y - size)
        t.pendown()
        t.fillcolor("peru")
        t.begin_fill()
        t.goto(x + size + height, y - size + height)
        t.goto(x + size + height, y + size + height)
        t.goto(x + size, y + size)
        t.goto(x + size, y - size)
        t.end_fill()
        
        t.penup()
        t.goto(x - size, y + size)
        t.pendown()
        t.fillcolor("dark red")
        t.begin_fill()
        t.goto(x - size + height, y + size + height)
        t.goto(x + height, y + size + height + 20)
        t.goto(x, y + size + 20)
        t.goto(x - size, y + size)
        t.end_fill()
        
        t.penup()
        t.goto(x + size, y + size)
        t.pendown()
        t.fillcolor("red")
        t.begin_fill()
        t.goto(x + size + height, y + size + height)
        t.goto(x + height, y + size + height + 20)
        t.goto(x, y + size + 20)
        t.goto(x + size, y + size)
        t.end_fill()
    
    def collides_with(self, px, py):
        return abs(px - self.x) < self.size + 5 and abs(py - self.y) < self.size + 5


def create_buildings():
    if buildings:
        return
    for i in range(-300, 350, 150):
        for j in range(-200, 250, 150):
            if not (i == 0 and j == 0):
                buildings.append(Building(i, j, 30, 15))


drones = []


class Drone:
    def __init__(self):
        self.turtle = create_turtle()
        self.x = random.randint(-300, 300)
        self.y = random.randint(-200, 200)
        self.dx = random.choice([-3, -2, 2, 3])
        self.dy = random.choice([-3, -2, 2, 3])
        self.rotation = 0
    
    def draw(self):
        self.turtle.clear()
        x, y = self.x, self.y
        
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.fillcolor("red")
        self.turtle.begin_fill()
        self.turtle.circle(15)
        self.turtle.end_fill()
        
        self.turtle.penup()
        self.turtle.goto(x - 5, y + 20)
        self.turtle.pendown()
        self.turtle.fillcolor("yellow")
        self.turtle.begin_fill()
        self.turtle.circle(3)
        self.turtle.end_fill()
        
        self.turtle.penup()
        self.turtle.goto(x + 5, y + 20)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.circle(3)
        self.turtle.end_fill()
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.x < -350 or self.x > 350:
            self.dx = -self.dx
        if self.y < -250 or self.y > 250:
            self.dy = -self.dy


def create_drones():
    if drones:
        return
    for _ in range(4):
        drones.append(Drone())


player_x, player_y = -350, -250
player_speed = 8
keys = {"w": False, "s": False, "a": False, "d": False}


def press_w(): keys["w"] = True
def press_s(): keys["s"] = True
def press_a(): keys["a"] = True
def press_d(): keys["d"] = True
def release_w(): keys["w"] = False
def release_s(): keys["s"] = False
def release_a(): keys["a"] = False
def release_d(): keys["d"] = False


screen.listen()
for key_name, press_fn, release_fn in [
    ("w", press_w, release_w), ("s", press_s, release_s),
    ("a", press_a, release_a), ("d", press_d, release_d)
]:
    screen.onkeypress(press_fn, key_name)
    screen.onkeyrelease(release_fn, key_name)

screen.onkeypress(press_w, "Up")
screen.onkeypress(press_s, "Down")
screen.onkeypress(press_a, "Left")
screen.onkeypress(press_d, "Right")
screen.onkeyrelease(release_w, "Up")
screen.onkeyrelease(release_s, "Down")
screen.onkeyrelease(release_a, "Left")
screen.onkeyrelease(release_d, "Right")

lives = 3
game_over = False
level_complete = False
invincible = False
invincible_counter = 0


def respawn_player():
    global player_x, player_y, invincible, invincible_counter
    player_x, player_y = -350, -250
    invincible = True
    invincible_counter = 60


def check_collision(x1, y1, x2, y2, distance=35):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < distance


def can_move_to(new_x, new_y):
    for building in buildings:
        if building.collides_with(new_x, new_y):
            return False
    return -380 <= new_x <= 380 and -280 <= new_y <= 280


def clear_level():
    global hearts_turtle_ref
    
    for b in buildings:
        clear_turtles(b.turtle)
    for d in drones:
        clear_turtles(d.turtle)
    
    clear_turtles(hearts_turtle_ref)
    hearts_turtle_ref = None
    
    try:
        key.clear()
        key.hideturtle()
        player.clear()
        player.hideturtle()
        status_display.clear()
        lives_display.clear()
    except Exception:
        pass


def game_loop():
    global player_x, player_y, lives, game_over, level_complete, invincible, invincible_counter
    
    if game_over or level_complete:
        return
    
    if keys["w"]:
        new_y = min(player_y + player_speed, 270)
        if can_move_to(player_x, new_y):
            player_y = new_y
    if keys["s"]:
        new_y = max(player_y - player_speed, -270)
        if can_move_to(player_x, new_y):
            player_y = new_y
    if keys["a"]:
        new_x = max(player_x - player_speed, -380)
        if can_move_to(new_x, player_y):
            player_x = new_x
    if keys["d"]:
        new_x = min(player_x + player_speed, 380)
        if can_move_to(new_x, player_y):
            player_x = new_x
    
    if invincible:
        invincible_counter -= 1
        if invincible_counter <= 0:
            invincible = False
    
    for drone in drones:
        drone.move()
        drone.draw()
        
        if not invincible and check_collision(player_x, player_y, drone.x, drone.y):
            lives -= 1
            
            status_display.clear()
            status_display.goto(0, 0)
            status_display.color("red")
            status_display.write("CAUGHT BY DRONE!", align="center", font=("Courier", 24, "bold"))
            screen.update()
            update_lives_display(lives)
            time.sleep(1)
            status_display.clear()
            
            if lives <= 0:
                game_over = True
                status_display.goto(0, 0)
                status_display.color("red")
                status_display.write("GAME OVER!\nYou lost all lives!", align="center", font=("Courier", 32, "bold"))
                clear_level()
                return
            else:
                status_display.goto(0, 0)
                status_display.color("yellow")
                status_display.write(f"RESPAWNING...\n{lives} Lives Remaining", align="center", font=("Courier", 20, "bold"))
                screen.update()
                time.sleep(1)
                status_display.clear()
                respawn_player()
    
    draw_player(player_x, player_y, invincible)
    draw_key()
    
    if check_collision(player_x, player_y, key_pos[0], key_pos[1], 40):
        level_complete = True
        
        messages = [
            (0, 50, "gold", "DATA KEY ACQUIRED!", 28, "bold", 2.0),
            (0, 20, "cyan", "The city freezes around you...", 18, "normal", 2.0),
            (0, 0, "white", '"Good... The first gate opens."', 16, "italic", 2.5),
            (0, 0, "lime", "LEVEL 1 COMPLETE!\nPreparing next trial...", 24, "bold", 2.5),
        ]
        
        for y, _, color, text, size, style, delay in messages:
            status_display.clear()
            status_display.goto(0, y)
            status_display.color(color)
            status_display.write(text, align="center", font=("Courier", size, style))
            screen.update()
            time.sleep(delay)
        
        clear_level()
        return
    
    screen.update()
    screen.ontimer(game_loop, 50)


intro_turtle = create_turtle()
intro_turtle.color("white")


def show_intro():
    try:
        clear_level()
    except Exception:
        pass
    intro_turtle.clear()
    intro_lines = [
        "You close your eyes for a short nap.",
        "A sleek demo VR headset rests on your face.",
        "When you open your eyes, you are not in your room.",
        "A neon-lit digital city floats in darkness.",
        "Drones hum like red-eyed insects overhead.",
        "Find the Data Key to open the next gate.",
        "",
        "Press SPACE or Enter to begin...",
    ]
    y = 80
    for line in intro_lines:
        intro_turtle.goto(0, y)
        intro_turtle.write(line, align="center", font=("Courier", 16, "normal"))
        y -= 28
    screen.update()


def start_level():
    intro_turtle.clear()
    try:
        create_buildings()
        create_drones()
    except Exception:
        pass
    update_lives_display(lives)
    game_loop()


screen.listen()
screen.onkey(start_level, 'space')
screen.onkey(start_level, 'Return')

if __name__ == '__main__':
    show_intro()
    screen.mainloop()