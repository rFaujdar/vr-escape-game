import turtle
import time
import level1
import wheel
import hangman
from ui_elements import create_turtle, clear_turtles, safe_clear_all, display_ending_screen

screen = level1.screen
screen.title("VR Escape - The Gem of Reality")
screen.bgcolor("black")

lives = 3
game_active = True

text = create_turtle()
text.color("white")
text.goto(0, 250)

msg = create_turtle()
msg.color("white")
msg.goto(0, 0)

intro_turtle = create_turtle()
intro_turtle.color("white")

lives_display = create_turtle()
lives_display.color("cyan")

screen.listen()
screen.onkey(lambda: screen.bye(), "Escape")


def update_displays():
    try:
        level1.lives = lives
        level1.update_lives_display(level1.lives)
    except Exception:
        pass


def cleanup_level_turtles(keep=None):
    if keep is None:
        keep = []
    keep_ids = {id(k) for k in keep if k}
    
    for t in turtle.turtles():
        try:
            if id(t) in keep_ids:
                continue
            if t in (text, msg, intro_turtle, lives_display):
                continue
            if hasattr(level1, 'lives_display') and t is level1.lives_display:
                continue
            t.hideturtle()
            t.clear()
        except Exception:
            pass


def show_message(message, duration=2, y_pos=-50):
    try:
        msg.clear()
        msg.goto(0, y_pos)
        msg.write(message, align="center", font=("Courier", 20, "bold"))
        screen.update()
        time.sleep(duration)
        msg.clear()
    except Exception:
        pass


def game_over_ending_level1():
    global game_active
    game_active = False
    display_ending_screen(screen, is_victory=False, ending_type="level1")


def game_over_ending():
    global game_active
    game_active = False
    display_ending_screen(screen, is_victory=False, ending_type="level2")


def victory():
    global game_active
    game_active = False
    display_ending_screen(screen, is_victory=True)


def show_story(lines, line_delay=2.0):
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
        pass


def run_level_1():
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
    global lives
    lives = wheel.wheel_of_fate(screen, lives, cleanup_level_turtles)
    return True


def run_level_2():
    global lives, game_active
    
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
    show_story(level2_lines, line_delay=2.0)
    
    state = {"lives": lives, "game_active": game_active}
    hangman.level_2_hangman(
        state, screen, text, lives_display, level1.player,
        update_displays, show_message, victory, game_over_ending
    )
    
    lives = state.get('lives', lives)
    game_active = state.get('game_active', game_active)
    
    return game_active


def main():
    global lives, game_active
    
    cleanup_level_turtles()
    
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
    show_story(story_lines, line_delay=2.0)
    
    show_message("You try to remove the headset...", 2.0, -50)
    show_message("But there's nothing on your face.", 2.0, -50)
    show_message("You are fully inside the simulation.", 2.5, -50)
    
    update_displays()
    
    if game_active:
        level1_complete = run_level_1()
        if not level1_complete:
            game_active = False
            if level1.game_over:
                time.sleep(1)
                game_over_ending_level1()
    
    if game_active:
        run_wheel_of_fate()
    
    if game_active:
        run_level_2()
    
    screen.mainloop()


if __name__ == "__main__":
    main()