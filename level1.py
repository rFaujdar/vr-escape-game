import turtle
import random
import math
import time
from ui_elements import draw_heart, clear_turtles

# Get the existing screen (don't create a new one)
screen = turtle.Screen()
screen.title("Level 1 - 3D Drone Evasion")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Lives display turtle
lives_display = turtle.Turtle()
lives_display.hideturtle()
lives_display.penup()
lives_display.color("cyan")

# Track hearts turtle for cleanup
hearts_turtle_ref = None


def update_lives_display(lives):
    """Update lives display: Lives: [hearts] | WASD to Move"""
    global hearts_turtle_ref
    
    # Clear previous hearts
    if hearts_turtle_ref is not None:
        try:
            hearts_turtle_ref.clear()
            hearts_turtle_ref.hideturtle()
        except Exception:
            pass
    
    # Clear and redraw lives display
    lives_display.clear()
    lives_display.goto(-350, 250)
    lives_display.write("Lives:", font=("Courier", 14, "bold"))
    
    # Draw hearts next to "Lives:" text
    hearts_turtle_ref = turtle.Turtle()
    hearts_turtle_ref.hideturtle()
    hearts_turtle_ref.speed(0)
    
    for i in range(lives):
        draw_heart(hearts_turtle_ref, -280 + (i * 20), 255, size=7, color="#ff0066")
    
    # (Removed controls text here to avoid duplicate/overlapping HUD elements)
    # Position hearts_turtle_ref so other code can add text nearby if needed
    hearts_turtle_ref.penup()
    hearts_turtle_ref.goto(-280 + (lives * 20) + 10, 250)


# Game status display
status_display = turtle.Turtle()
status_display.hideturtle()
status_display.penup()
status_display.color("white")
status_display.goto(0, 0)

# Player setup (3D pyramid effect)
player = turtle.Turtle()
player.hideturtle()
player.penup()
player.speed(0)
player.goto(-350, -250)


def draw_player(x, y, invincible=False):
    player.clear()
    player.goto(x, y)
    
    # Draw 3D pyramid effect with blinking when invincible
    if not invincible or (invincible and int(x * 5) % 2 == 0):
        # Front face (cyan)
        player.penup()
        player.goto(x, y - 15)
        player.pendown()
        player.fillcolor("cyan" if not invincible else "light cyan")
        player.begin_fill()
        player.goto(x - 12, y - 25)
        player.goto(x + 12, y - 25)
        player.goto(x, y - 15)
        player.end_fill()
        
        # Left face (darker cyan)
        player.penup()
        player.goto(x, y - 15)
        player.pendown()
        player.fillcolor("dark cyan" if not invincible else "cyan")
        player.begin_fill()
        player.goto(x - 12, y - 25)
        player.goto(x, y - 35)
        player.goto(x, y - 15)
        player.end_fill()
        
        # Right face (light cyan)
        player.penup()
        player.goto(x, y - 15)
        player.pendown()
        player.fillcolor("light cyan" if not invincible else "white")
        player.begin_fill()
        player.goto(x + 12, y - 25)
        player.goto(x, y - 35)
        player.goto(x, y - 15)
        player.end_fill()


# Data Key setup (3D cube effect) - STATIC, no rotation
key = turtle.Turtle()
key.hideturtle()
key.penup()
key.speed(0)
key_pos = [350, 250]


def draw_key():
    key.clear()
    x = key_pos[0]
    y = key_pos[1]
    
    # Front face (gold)
    key.penup()
    key.goto(x - 15, y - 15)
    key.pendown()
    key.fillcolor("gold")
    key.begin_fill()
    for _ in range(4):
        key.forward(30)
        key.left(90)
    key.end_fill()
    
    # Top face (yellow)
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
    
    # Right face (dark goldenrod)
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


# Buildings setup (3D cubes)
buildings = []


class Building:
    def __init__(self, x, y, size, height):
        self.x = x
        self.y = y
        self.size = size
        self.height = height
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.speed(0)
        self.draw()
    
    def draw(self):
        # Front face (building wall)
        self.turtle.goto(self.x - self.size, self.y - self.size)
        self.turtle.pendown()
        self.turtle.fillcolor("saddle brown")
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(self.size * 2)
            self.turtle.left(90)
        self.turtle.end_fill()
        
        # Door
        self.turtle.penup()
        self.turtle.goto(self.x - 8, self.y - self.size)
        self.turtle.pendown()
        self.turtle.fillcolor("dark red")
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(16)
            self.turtle.left(90)
            self.turtle.forward(20)
            self.turtle.left(90)
        self.turtle.end_fill()
        
        # Window
        self.turtle.penup()
        self.turtle.goto(self.x - self.size + 8, self.y)
        self.turtle.pendown()
        self.turtle.fillcolor("light blue")
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(12)
            self.turtle.left(90)
        self.turtle.end_fill()
        
        # Right side wall
        self.turtle.penup()
        self.turtle.goto(self.x + self.size, self.y - self.size)
        self.turtle.pendown()
        self.turtle.fillcolor("peru")
        self.turtle.begin_fill()
        self.turtle.goto(self.x + self.size + self.height, self.y - self.size + self.height)
        self.turtle.goto(self.x + self.size + self.height, self.y + self.size + self.height)
        self.turtle.goto(self.x + self.size, self.y + self.size)
        self.turtle.goto(self.x + self.size, self.y - self.size)
        self.turtle.end_fill()
        
        # Roof (triangular top)
        self.turtle.penup()
        self.turtle.goto(self.x - self.size, self.y + self.size)
        self.turtle.pendown()
        self.turtle.fillcolor("dark red")
        self.turtle.begin_fill()
        self.turtle.goto(self.x - self.size + self.height, self.y + self.size + self.height)
        self.turtle.goto(self.x + self.height, self.y + self.size + self.height + 20)
        self.turtle.goto(self.x, self.y + self.size + 20)
        self.turtle.goto(self.x - self.size, self.y + self.size)
        self.turtle.end_fill()
        
        # Roof right side
        self.turtle.penup()
        self.turtle.goto(self.x + self.size, self.y + self.size)
        self.turtle.pendown()
        self.turtle.fillcolor("red")
        self.turtle.begin_fill()
        self.turtle.goto(self.x + self.size + self.height, self.y + self.size + self.height)
        self.turtle.goto(self.x + self.height, self.y + self.size + self.height + 20)
        self.turtle.goto(self.x, self.y + self.size + 20)
        self.turtle.goto(self.x + self.size, self.y + self.size)
        self.turtle.end_fill()
    
    def collides_with(self, px, py):
        return (abs(px - self.x) < self.size + 5 and 
                abs(py - self.y) < self.size + 5)


def draw_building(x, y, size, height):
    b = Building(x, y, size, height)
    buildings.append(b)


def create_buildings():
    """Create the static buildings (houses) for the level."""
    if buildings:
        return
    for i in range(-300, 350, 150):
        for j in range(-200, 250, 150):
            if not (i == 0 and j == 0):
                draw_building(i, j, 30, 15)


# AI Drones setup
drones = []


class Drone:
    def __init__(self):
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.speed(0)
        self.x = random.randint(-300, 300)
        self.y = random.randint(-200, 200)
        self.dx = random.choice([-3, -2, 2, 3])
        self.dy = random.choice([-3, -2, 2, 3])
        self.rotation = 0
    
    def draw(self):
        self.turtle.clear()
        # Draw 3D sphere-like drone with red glowing effect
        self.turtle.goto(self.x, self.y - 18)
        self.turtle.pendown()
        self.turtle.fillcolor("#ff3333")
        self.turtle.begin_fill()
        self.turtle.circle(18)
        self.turtle.end_fill()
        self.turtle.penup()
        
        self.turtle.goto(self.x, self.y - 14)
        self.turtle.pendown()
        self.turtle.fillcolor("#990000")
        self.turtle.begin_fill()
        self.turtle.circle(14)
        self.turtle.end_fill()
        self.turtle.penup()
        
        self.turtle.goto(self.x, self.y - 6)
        self.turtle.pendown()
        self.turtle.fillcolor("#ff0000")
        self.turtle.begin_fill()
        self.turtle.circle(6)
        self.turtle.end_fill()
        self.turtle.penup()
    
    def move(self):
        # Basic movement
        self.x += self.dx
        self.y += self.dy

        # Screen bounds bounce
        if self.x < -350 or self.x > 350:
            self.dx = -self.dx
            self.x = max(-350, min(350, self.x))
        if self.y < -250 or self.y > 250:
            self.dy = -self.dy
            self.y = max(-250, min(250, self.y))

        # Building collisions: push the drone out along a small nudge
        # and add a tiny random offset to the bounce so it doesn't
        # repeatedly flip in-place and get stuck.
        for building in buildings:
            if building.collides_with(self.x, self.y):
                # Small randomization to help escape tight corners
                try:
                    # Reverse direction with a slight random change
                    self.dx = -self.dx + random.choice([-1, 0, 1])
                    self.dy = -self.dy + random.choice([-1, 0, 1])
                except Exception:
                    self.dx = -self.dx
                    self.dy = -self.dy

                # Ensure non-zero velocity so drone keeps moving
                if self.dx == 0:
                    self.dx = random.choice([-2, 2])
                if self.dy == 0:
                    self.dy = random.choice([-2, 2])

                # Nudge the drone away a bit more to resolve overlap
                self.x += self.dx * 4
                self.y += self.dy * 4

                # If still colliding, perform a vector push directly away
                if building.collides_with(self.x, self.y):
                    vx = self.x - building.x
                    vy = self.y - building.y
                    if vx == 0 and vy == 0:
                        vx, vy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                    dist = math.hypot(vx, vy) or 1.0
                    nx, ny = vx / dist, vy / dist
                    push_dist = building.size + 18 + 6
                    self.x = building.x + nx * push_dist
                    self.y = building.y + ny * push_dist

                break


def create_drones():
    """Create the drones for the level."""
    if drones:
        return
    for _ in range(4):
        d = Drone()
        drones.append(d)


# Player position and speed
player_x = -350
player_y = -250
player_speed = 8

# Key states for smooth movement
keys = {"w": False, "s": False, "a": False, "d": False}


def press_w():
    keys["w"] = True


def press_s():
    keys["s"] = True


def press_a():
    keys["a"] = True


def press_d():
    keys["d"] = True


def release_w():
    keys["w"] = False


def release_s():
    keys["s"] = False


def release_a():
    keys["a"] = False


def release_d():
    keys["d"] = False


# Bind keys
screen.listen()
screen.onkeypress(press_w, "w")
screen.onkeypress(press_s, "s")
screen.onkeypress(press_a, "a")
screen.onkeypress(press_d, "d")
screen.onkeypress(press_w, "Up")
screen.onkeypress(press_s, "Down")
screen.onkeypress(press_a, "Left")
screen.onkeypress(press_d, "Right")

screen.onkeyrelease(release_w, "w")
screen.onkeyrelease(release_s, "s")
screen.onkeyrelease(release_a, "a")
screen.onkeyrelease(release_d, "d")
screen.onkeyrelease(release_w, "Up")
screen.onkeyrelease(release_s, "Down")
screen.onkeyrelease(release_a, "Left")
screen.onkeyrelease(release_d, "Right")

# Game state
lives = 3
game_over = False
level_complete = False
invincible = False
invincible_counter = 0


def respawn_player():
    global player_x, player_y, invincible, invincible_counter
    player_x = -350
    player_y = -250
    invincible = True
    invincible_counter = 60


def check_collision(x1, y1, x2, y2, distance=35):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) < distance


def can_move_to(new_x, new_y):
    for building in buildings:
        if building.collides_with(new_x, new_y):
            return False
    if new_x < -380 or new_x > 380:
        return False
    if new_y < -280 or new_y > 280:
        return False
    return True


def clear_level():
    """Hide and clear all level-specific turtles."""
    global hearts_turtle_ref
    
    try:
        for b in buildings:
            try:
                b.turtle.clear()
                b.turtle.hideturtle()
            except Exception:
                pass
        for d in drones:
            try:
                d.turtle.clear()
                d.turtle.hideturtle()
            except Exception:
                pass
        try:
            key.clear()
            key.hideturtle()
        except Exception:
            pass
        try:
            player.clear()
            player.hideturtle()
        except Exception:
            pass
        try:
            status_display.clear()
        except Exception:
            pass
        try:
            lives_display.clear()
        except Exception:
            pass
        if hearts_turtle_ref is not None:
            try:
                hearts_turtle_ref.clear()
                hearts_turtle_ref.hideturtle()
            except Exception:
                pass
            # Release reference so future updates create a fresh turtle
            try:
                hearts_turtle_ref = None
            except Exception:
                pass
    except Exception:
        pass


# Game loop
def game_loop():
    global player_x, player_y, lives, game_over, level_complete
    global invincible, invincible_counter
    
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
            status_display.write("CAUGHT BY DRONE!", 
                               align="center", 
                               font=("Courier", 24, "bold"))
            screen.update()
            
            update_lives_display(lives)
            
            time.sleep(1)
            status_display.clear()
            
            if lives <= 0:
                game_over = True
                status_display.goto(0, 0)
                status_display.color("red")
                status_display.write("GAME OVER!\nYou lost all lives!", 
                                   align="center", 
                                   font=("Courier", 32, "bold"))
                clear_level()
                return
            else:
                status_display.goto(0, 0)
                status_display.color("yellow")
                status_display.write(f"RESPAWNING...\n{lives} Lives Remaining", 
                                   align="center", 
                                   font=("Courier", 20, "bold"))
                screen.update()
                time.sleep(1)
                status_display.clear()
                respawn_player()
    
    draw_player(player_x, player_y, invincible)
    draw_key()
    
    if check_collision(player_x, player_y, key_pos[0], key_pos[1], 40):
        level_complete = True
        
        status_display.goto(0, 50)
        status_display.color("gold")
        status_display.write("DATA KEY ACQUIRED!", 
                           align="center", 
                           font=("Courier", 28, "bold"))
        screen.update()
        time.sleep(1.5)
        
        status_display.clear()
        status_display.goto(0, 20)
        status_display.color("cyan")
        status_display.write("The city freezes around you...", 
                           align="center", 
                           font=("Courier", 18, "normal"))
        screen.update()
        time.sleep(1.5)
        
        status_display.clear()
        status_display.goto(0, 0)
        status_display.color("white")
        status_display.write('"Good... The first gate opens."', 
                           align="center", 
                           font=("Courier", 16, "italic"))
        screen.update()
        time.sleep(2)
        
        status_display.clear()
        status_display.goto(0, 0)
        status_display.color("lime")
        status_display.write("LEVEL 1 COMPLETE!\nPreparing next trial...", 
                           align="center", 
                           font=("Courier", 24, "bold"))
        screen.update()
        time.sleep(2)
        
        clear_level()
        return
    
    screen.update()
    screen.ontimer(game_loop, 50)


# Intro splash
intro_turtle = turtle.Turtle()
intro_turtle.hideturtle()
intro_turtle.penup()
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