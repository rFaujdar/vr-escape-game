import turtle
import random
import time
import math
from ui_elements import draw_heart, create_turtle, clear_turtles


def wheel_of_fate(screen, lives, cleanup_callback):
    cleanup_callback()
    
    for t in turtle.turtles():
        try:
            t.clear()
        except Exception:
            pass
    
    screen.bgcolor("#0a0520")
    
    title = create_turtle()
    title.goto(0, 250)
    title.color("#ffaa00")
    title.write("WHEEL OF FATE", align="center", font=("Courier", 24, "bold"))
    
    announcement = create_turtle()
    announcement.color("#00ffff")
    announcement.goto(0, 215)
    announcement.write('"Spin to determine your vitality for the next trial."', 
                      align="center", font=("Courier", 12, "italic"))
    
    lives_label = create_turtle()
    lives_label.goto(-350, 175)
    lives_label.color("#ffffff")
    lives_label.write("Current Lives:", align="left", font=("Courier", 11, "bold"))
    
    lives_hearts = create_turtle()
    for i in range(lives):
        draw_heart(lives_hearts, -230 + (i * 20), 180, size=7, color="#ff0066")
    
    wheel_center_x, wheel_center_y, wheel_radius = 0, 40, 80
    
    wheel_bg = create_turtle()
    wheel_bg.goto(wheel_center_x, wheel_center_y - wheel_radius)
    wheel_bg.pendown()
    wheel_bg.fillcolor("#1a1a3a")
    wheel_bg.begin_fill()
    wheel_bg.circle(wheel_radius)
    wheel_bg.end_fill()
    
    segment_colors = ["#ff0000", "#00ff00", "#ffaa00", "#0088ff"]
    segment_labels = ["0", "10", "20", "30"]
    segment_lives = [0, 1, 2, 3]
    
    wheel_segments = []
    for i in range(4):
        seg = create_turtle()
        angle = 90 * i
        label_distance = wheel_radius + 25
        label_x = wheel_center_x + label_distance * math.cos(math.radians(angle + 45))
        label_y = wheel_center_y + label_distance * math.sin(math.radians(angle + 45))
        seg.goto(label_x, label_y)
        seg.color(segment_colors[i])
        seg.write(segment_labels[i], align="center", font=("Courier", 24, "bold"))
        wheel_segments.append(seg)
    
    divider = create_turtle()
    divider.color("#ffffff")
    divider.width(3)
    for i in range(4):
        divider.goto(wheel_center_x, wheel_center_y)
        divider.setheading(90 * i)
        divider.pendown()
        divider.forward(wheel_radius)
        divider.penup()
    
    pointer = create_turtle()
    pointer.goto(wheel_center_x, wheel_center_y + wheel_radius + 15)
    pointer.setheading(270)
    pointer.pendown()
    pointer.color("#ffff00")
    pointer.fillcolor("#ffff00")
    pointer.begin_fill()
    pointer.forward(12)
    pointer.right(120)
    pointer.forward(16)
    pointer.right(120)
    pointer.forward(16)
    pointer.right(120)
    pointer.forward(4)
    pointer.end_fill()
    
    legend = create_turtle()
    legend.color("#aaaaaa")
    legend.goto(0, -70)
    legend.write("0 = No bonus  |  10 = +1 life  |  20 = +2 lives  |  30 = +3 lives",
                align="center", font=("Courier", 9, "normal"))
    
    spin_button = turtle.Turtle()
    spin_button.shape("circle")
    spin_button.color("#ff00ff")
    spin_button.shapesize(2, 2)
    spin_button.penup()
    spin_button.goto(0, -130)
    
    spin_label = create_turtle()
    spin_label.goto(0, -105)
    spin_label.color("#ffffff")
    spin_label.write("CLICK TO SPIN", align="center", font=("Courier", 12, "bold"))
    
    instruction = create_turtle()
    instruction.goto(0, -165)
    instruction.color("#888888")
    instruction.write("(or press SPACE)", align="center", font=("Courier", 9, "normal"))
    
    screen.update()
    
    result = {"done": False, "bonus": 0}
    
    def spin_wheel(x=None, y=None):
        if result["done"]:
            return
        result["done"] = True
        
        spin_button.hideturtle()
        spin_label.clear()
        instruction.clear()
        
        spin_msg = create_turtle()
        spin_msg.goto(0, -120)
        spin_msg.color("#ffff00")
        spin_msg.write("SPINNING...", align="center", font=("Courier", 16, "bold"))
        screen.update()
        
        result_index = random.randint(0, 3)
        total_spins = 20 + result_index
        
        for i in range(total_spins):
            current_segment = i % 4
            for j, seg in enumerate(wheel_segments):
                seg.clear()
                angle = 90 * j
                label_distance = wheel_radius + 25
                label_x = wheel_center_x + label_distance * math.cos(math.radians(angle + 45))
                label_y = wheel_center_y + label_distance * math.sin(math.radians(angle + 45))
                seg.goto(label_x, label_y)
                
                if j == current_segment:
                    seg.color("#ffffff")
                    seg.write(segment_labels[j], align="center", font=("Courier", 28, "bold"))
                else:
                    seg.color(segment_colors[j])
                    seg.write(segment_labels[j], align="center", font=("Courier", 24, "bold"))
            
            screen.update()
            time.sleep(0.05 + (i * 0.003))
        
        spin_msg.clear()
        bonus = segment_lives[result_index]
        result["bonus"] = bonus
        
        result_msg = create_turtle()
        result_msg.goto(0, wheel_center_y)
        result_msg.color(segment_colors[result_index])
        result_msg.write(segment_labels[result_index], align="center", font=("Courier", 48, "bold"))
        screen.update()
        time.sleep(1.5)
        
        result_msg.clear()
        result_msg.goto(0, -120)
        result_msg.color("#00ff00")
        if bonus == 0:
            result_msg.write("No bonus lives granted.", align="center", font=("Courier", 14, "normal"))
        else:
            result_msg.write(f"+{bonus} LIFE BONUS!", align="center", font=("Courier", 18, "bold"))
        screen.update()
        time.sleep(1.5)
        
        lives_hearts.clear()
        lives_label.clear()
        lives_label.goto(-350, 175)
        lives_label.write("Updated Lives:", align="left", font=("Courier", 11, "bold"))
        new_total = lives + bonus
        for i in range(new_total):
            draw_heart(lives_hearts, -230 + (i * 20), 180, size=7, color="#00ff88")
        screen.update()
        
        result_msg.clear()
        result_msg.goto(0, -155)
        result_msg.color("#ffaa00")
        result_msg.write(f"Total Lives: {new_total}", align="center", font=("Courier", 16, "bold"))
        screen.update()
        time.sleep(2)
        
        for seg in wheel_segments:
            clear_turtles(seg)
        
        clear_turtles(wheel_bg, divider, pointer, legend, result_msg, 
                     announcement, title, spin_button, lives_hearts, lives_label, spin_msg)
    
    spin_button.onclick(spin_wheel)
    screen.onkey(spin_wheel, "space")
    screen.onkey(spin_wheel, "Return")
    screen.listen()
    
    while not result["done"]:
        try:
            screen.update()
            time.sleep(0.1)
        except Exception:
            break
    
    return lives + result["bonus"]