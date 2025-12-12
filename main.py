import turtle
import time
import level1
import wheel
import hangman

# Game setup - use the screen from level1 to avoid conflicts
screen = level1.screen
screen.title("VR Escape - The Gem of Reality")
screen.bgcolor("black")

# Game state
lives = 3
game_active = True

# Text display
text = turtle.Turtle()
text.hideturtle()
text.color("white")
text.penup()
text.goto(0, 250)

# Transient message turtle
msg = turtle.Turtle()
msg.hideturtle()
msg.color("white")
msg.penup()
msg.goto(0, 0)

# Intro/story turtle
intro_turtle = turtle.Turtle()
intro_turtle.hideturtle()
intro_turtle.penup()
intro_turtle.color("white")

# Use level1's lives display (hearts) instead of creating a second lives turtle here.
# main will delegate display updates to level1.update_lives_display
# Create a minimal `lives_display` turtle so other modules (e.g. hangman)
# can be passed a valid turtle object. We won't draw HUD from this turtle
# during Level 1 (level1 handles its own hearts), but hangman expects
# a `lives_display` parameter so keep a placeholder here.
lives_display = turtle.Turtle()
lives_display.hideturtle()
lives_display.penup()
lives_display.color("cyan")

# Global ESC to exit
screen.listen()
screen.onkey(lambda: screen.bye(), "Escape")


def update_displays():
    """Update HUD displays. Delegate lives display to `level1` to
    avoid duplicate overlays (hearts + text)."""
    try:
        # Sync lives into level1 and let level1 draw its own hearts text
        level1.lives = lives
        level1.update_lives_display(level1.lives)
    except Exception:
        # If level1 isn't available for some reason, silently skip
        pass


def cleanup_level_turtles(keep=None):
    """Hide/clear all turtles except those in keep list."""
    if keep is None:
        keep = []
    keep_ids = set()
    for k in keep:
        try:
            keep_ids.add(id(k))
        except Exception:
            pass

    for t in turtle.turtles():
        try:
            if id(t) in keep_ids:
                continue
            # Keep our primary UI turtles and the level1 lives display
            if (
                t is text or t is msg or t is intro_turtle or t is lives_display or
                (hasattr(level1, 'lives_display') and t is level1.lives_display)
            ):
                continue
            t.hideturtle()
            t.clear()
        except Exception:
            pass


def show_message(message, duration=2):
    try:
        msg.clear()
        msg.goto(0, 0)
        msg.write(message, align="center", font=("Courier", 20, "bold"))
        screen.update()
        time.sleep(duration)
        msg.clear()
    except Exception:
        try:
            print(message)
            time.sleep(duration)
        except Exception:
            pass


def show_story(lines, line_delay=1.5):
    """Display a short story intro."""
    try:
        intro_turtle.clear()
        y = 80
        for line in lines:
            intro_turtle.goto(0, y)
            intro_turtle.write(line, align="center", font=("Courier", 16, "normal"))
            y -= 28
            screen.update()
            time.sleep(line_delay)
        time.sleep(0.5)
        intro_turtle.clear()
        screen.update()
    except Exception:
        for line in lines:
            print(line)
            time.sleep(line_delay)


def run_level_1():
    """Run Level 1 and return updated lives."""
    global lives
    
    level1.lives = lives
    level1.game_over = False
    level1.level_complete = False
    
    level1.show_intro()
    level1.update_lives_display(level1.lives)
    level1.start_level()
    
    while not level1.level_complete and not level1.game_over:
        try:
            screen.update()
            time.sleep(0.05)
        except Exception:
            break
    
    lives = level1.lives
    return level1.level_complete


def run_wheel_of_fate():
    """Run the Wheel of Fate and return updated lives."""
    global lives
    lives = wheel.wheel_of_fate(screen, lives, cleanup_level_turtles)
    return True


def run_level_2():
    """Run Level 2 (Hangman) and return success status."""
    global lives, game_active
    
    # Show Level 2 intro
    level2_lines = [
        "The darkness fades...",
        "You find yourself lying on a deserted highway.",
        "Your wrists and ankles are bound with glowing restraints.",
        "",
        "Far down the road, headlights flicker to life.",
        "A massive truck begins rolling forward.",
        "",
        '"This is RACEMAX."',
        '"You cannot run. You cannot dodge."',
        '"Your mind is your only weapon."',
    ]
    show_story(level2_lines, line_delay=1.2)
    
    state = {"lives": lives, "game_active": game_active}
    hangman.level_2_hangman(
        state,
        screen,
        text,
        lives_display,
        level1.player,
        update_displays,
        show_message,
        victory,
    )
    
    lives = state.get('lives', lives)
    game_active = state.get('game_active', game_active)
    
    return game_active


def victory():
    """Display victory screen with credits - NO lives counter."""
    global game_active
    
    # Set game_active to False to prevent loops
    game_active = False
    
    # Clear ALL turtles including lives_display
    for t in turtle.turtles():
        try:
            t.clear()
            t.hideturtle()
        except Exception:
            pass
    
    screen.bgcolor("#1a0a0a")
    
    # Show Level 2 completion sequence
    story_msg = turtle.Turtle()
    story_msg.hideturtle()
    story_msg.penup()
    
    story_msg.goto(0, 60)
    story_msg.color("#00ff00")
    story_msg.write("WORD COMPLETE!", align="center", font=("Courier", 26, "bold"))
    screen.update()
    time.sleep(1.5)
    
    story_msg.clear()
    story_msg.goto(0, 30)
    story_msg.color("#ffff00")
    story_msg.write("The truck screeches to a halt...", align="center", font=("Courier", 16, "normal"))
    screen.update()
    time.sleep(1.5)
    
    story_msg.clear()
    story_msg.goto(0, 0)
    story_msg.color("#00ffff")
    story_msg.write('"Correct. You have earned the coordinates."', align="center", font=("Courier", 14, "italic"))
    screen.update()
    time.sleep(2)
    
    story_msg.clear()
    story_msg.goto(0, -30)
    story_msg.color("#ffffff")
    story_msg.write("The restraints disintegrate into glowing dust...", align="center", font=("Courier", 14, "normal"))
    screen.update()
    time.sleep(1.5)
    
    story_msg.clear()
    story_msg.goto(0, 0)
    story_msg.color("#00ff88")
    story_msg.write("LEVEL 2 COMPLETE!\nApproaching the Gem...", align="center", font=("Courier", 22, "bold"))
    screen.update()
    time.sleep(2)
    
    # Clear for final screen
    story_msg.clear()
    
    # Change to credits background
    screen.bgcolor("#0a0a1a")
    
    # Victory message - NO lives display anywhere
    victory_title = turtle.Turtle()
    victory_title.hideturtle()
    victory_title.color("#ffd700")
    victory_title.penup()
    victory_title.goto(0, 150)
    victory_title.write("GEM OF REALITY OBTAINED!", align="center", font=("Courier", 24, "bold"))
    
    victory_sub = turtle.Turtle()
    victory_sub.hideturtle()
    victory_sub.color("#00ff88")
    victory_sub.penup()
    victory_sub.goto(0, 110)
    victory_sub.write("YOU ESCAPED THE SIMULATION!", align="center", font=("Courier", 18, "bold"))
    
    # Credits section
    credits_line1 = turtle.Turtle()
    credits_line1.hideturtle()
    credits_line1.color("#888888")
    credits_line1.penup()
    credits_line1.goto(0, 60)
    credits_line1.write("=" * 30, align="center", font=("Courier", 14, "normal"))
    
    credits_title = turtle.Turtle()
    credits_title.hideturtle()
    credits_title.color("#ffffff")
    credits_title.penup()
    credits_title.goto(0, 30)
    credits_title.write("DEVELOPED BY", align="center", font=("Courier", 14, "bold"))
    
    dev1 = turtle.Turtle()
    dev1.hideturtle()
    dev1.color("#00ddff")
    dev1.penup()
    dev1.goto(0, 0)
    dev1.write("Izma Arshad", align="center", font=("Courier", 16, "normal"))
    
    dev2 = turtle.Turtle()
    dev2.hideturtle()
    dev2.color("#00ddff")
    dev2.penup()
    dev2.goto(0, -30)
    dev2.write("Shreya", align="center", font=("Courier", 16, "normal"))
    
    dev3 = turtle.Turtle()
    dev3.hideturtle()
    dev3.color("#00ddff")
    dev3.penup()
    dev3.goto(0, -60)
    dev3.write("Yashasvini", align="center", font=("Courier", 16, "normal"))
    
    dev4 = turtle.Turtle()
    dev4.hideturtle()
    dev4.color("#00ddff")
    dev4.penup()
    dev4.goto(0, -90)
    dev4.write("Rajan", align="center", font=("Courier", 16, "normal"))
    
    credits_line2 = turtle.Turtle()
    credits_line2.hideturtle()
    credits_line2.color("#888888")
    credits_line2.penup()
    credits_line2.goto(0, -130)
    credits_line2.write("=" * 30, align="center", font=("Courier", 14, "normal"))
    
    thanks = turtle.Turtle()
    thanks.hideturtle()
    thanks.color("#ffaa00")
    thanks.penup()
    thanks.goto(0, -170)
    thanks.write("Thanks for playing!", align="center", font=("Courier", 12, "italic"))
    
    screen.update()


def main():
    global lives, game_active
    
    cleanup_level_turtles()
    
    # Opening storyline
    story_lines = [
        "You close your eyes for what was meant to be a short nap.",
        "The new VR headset-sleek, experimental-rests lightly on your face.",
        "But when you open your eyes...",
        "you're no longer in your room.",
        "",
        "A neon-lit digital city floats in darkness.",
        "Drones hum like red-eyed insects overhead.",
        "Skyscrapers twist at impossible angles.",
        "",
        '"Welcome, Player. You are inside the system now."',
        '"To return to your world, you must recover the Gem of Reality."',
    ]
    show_story(story_lines, line_delay=1.2)
    
    show_message("You try to remove the headset...", 1.5)
    show_message("But there's nothing on your face.", 1.5)
    show_message("You are fully inside the simulation.", 2)
    
    update_displays()
    
    # Level 1
    if game_active:
        level1_complete = run_level_1()
        if not level1_complete:
            game_active = False
    
    # Wheel of Fate
    if game_active:
        run_wheel_of_fate()
    
    # Level 2
    if game_active:
        run_level_2()
    
    # Keep window open
    screen.mainloop()


if __name__ == "__main__":
    main()