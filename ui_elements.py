import turtle
import time

DEVELOPERS = ["Izma Arshad", "Shreya Jagtap", "Yashaswini", "Saarang"]
FONT_FAMILY = "Courier"


def create_turtle():
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.speed(0)
    return t


def draw_heart(turtle_obj, x, y, size=10, color="#ff0066"):
    turtle_obj.penup()
    turtle_obj.goto(x, y)
    turtle_obj.setheading(0)
    turtle_obj.color(color)
    turtle_obj.fillcolor(color)
    turtle_obj.begin_fill()
    turtle_obj.left(140)
    turtle_obj.forward(size)
    turtle_obj.circle(-size / 2, 200)
    turtle_obj.left(120)
    turtle_obj.circle(-size / 2, 200)
    turtle_obj.forward(size)
    turtle_obj.end_fill()


def draw_text(t, x, y, text, color="#ffffff", size=14, style="normal", align="center"):
    t.goto(x, y)
    t.color(color)
    t.write(text, align=align, font=(FONT_FAMILY, size, style))


def clear_turtles(*turtles):
    for t in turtles:
        if t is not None:
            try:
                t.clear()
                t.hideturtle()
            except Exception:
                pass


def safe_clear_all():
    try:
        all_turtles = list(turtle.turtles())
        for t in all_turtles:
            try:
                if t.isvisible():
                    t.hideturtle()
                t.clear()
            except Exception:
                pass
    except Exception:
        pass


def display_credits(screen, start_y=40, dev_color="#00ddff"):
    t = create_turtle()
    draw_text(t, 0, start_y, "DEVELOPED BY", "#ffffff", 14, "bold")
    y = start_y - 30
    for name in DEVELOPERS:
        draw_text(t, 0, y, name, dev_color, 14, "normal")
        y -= 25
    screen.update()
    return t


def display_story_sequence(screen, messages, default_delay=2.0):
    t = create_turtle()
    for msg in messages:
        try:
            t.clear()
            draw_text(t, 0, msg.get("y", 0), msg.get("text", ""),
                     msg.get("color", "#ffffff"), msg.get("size", 16), msg.get("style", "normal"))
            screen.update()
            time.sleep(msg.get("delay", default_delay))
        except Exception:
            pass
    return t


def display_ending_screen(screen, is_victory=True):
    try:
        screen.tracer(0)
    except Exception:
        pass
    
    safe_clear_all()
    
    if is_victory:
        try:
            screen.bgcolor("#0a0a1a")
        except Exception:
            pass
        story = [
            {"text": "WORD COMPLETE!", "color": "#00ff00", "y": 60, "size": 26, "style": "bold", "delay": 2.0},
            {"text": "The truck screeches to a halt...", "color": "#ffff00", "y": 30, "size": 16, "delay": 2.0},
            {"text": '"Correct. You have earned the coordinates."', "color": "#00ffff", "y": 0, "size": 14, "style": "italic", "delay": 2.5},
            {"text": "The restraints disintegrate into glowing dust...", "color": "#ffffff", "y": -30, "size": 14, "delay": 2.0},
            {"text": "LEVEL 2 COMPLETE!\nApproaching the Gem...", "color": "#00ff88", "y": 0, "size": 22, "style": "bold", "delay": 2.5},
        ]
        cfg = {
            "title": "GEM OF REALITY OBTAINED!", "title_color": "#ffd700",
            "subtitle": "YOU ESCAPED THE SIMULATION!", "subtitle_color": "#00ff88",
            "dev_color": "#00ddff", "footer": "Thanks for playing!"
        }
    else:
        try:
            screen.bgcolor("#0a0008")
        except Exception:
            pass
        story = [
            {"text": "THE TRUCK ADVANCES...", "color": "#ff0000", "y": 60, "size": 22, "style": "bold", "delay": 2.0},
            {"text": "Your mind couldn't solve the puzzle in time.", "color": "#ff3333", "y": 30, "size": 14, "delay": 2.0},
            {"text": "The simulation claims another soul...", "color": "#ff6666", "y": 0, "size": 14, "style": "italic", "delay": 2.5},
            {"text": '"Perhaps in another iteration, Player."', "color": "#00ffff", "y": 20, "size": 16, "style": "italic", "delay": 2.5},
            {"text": '"The Gem of Reality remains hidden..."', "color": "#888888", "y": -10, "size": 14, "style": "italic", "delay": 2.5},
        ]
        cfg = {
            "title": "GAME OVER", "title_color": "#ff0000",
            "subtitle": "You remain trapped in the simulation forever.", "subtitle_color": "#ff6666",
            "dev_color": "#00aaff", "footer": "Press ESC to exit or restart to try again!"
        }
    
    try:
        story_t = display_story_sequence(screen, story)
        story_t.clear()
        
        if not is_victory:
            screen.bgcolor("#0a0a0a")
        
        t = create_turtle()
        draw_text(t, 0, 150, cfg["title"], cfg["title_color"], 30, "bold")
        draw_text(t, 0, 110, cfg["subtitle"], cfg["subtitle_color"], 14, "normal")
        draw_text(t, 0, 70, "=" * 35, "#444444", 12, "normal")
        display_credits(screen, 40, cfg["dev_color"])
        draw_text(t, 0, -100, "=" * 35, "#444444", 12, "normal")
        draw_text(t, 0, -140, cfg["footer"], "#ffaa00", 11, "normal")
        screen.update()
    except Exception:
        pass