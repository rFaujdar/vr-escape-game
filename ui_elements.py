import turtle


def draw_heart(turtle_obj, x, y, size=10, color="#ff0066"):
    """Draw a heart shape using turtle.
    
    Args:
        turtle_obj: The turtle object to draw with
        x, y: Position coordinates
        size: Size of the heart (default: 10)
        color: Color of the heart (default: pink)
    """
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


def draw_lives_display(screen, x, y, lives, label="Lives:", horizontal=True, color="#ff0066"):
    """Draw lives as hearts with a label.
    
    Args:
        screen: Turtle screen object
        x, y: Starting position
        lives: Number of lives to display
        label: Text label (default: "Lives:")
        horizontal: If True, hearts are horizontal; if False, vertical
        color: Color of hearts (default: pink)
    
    Returns:
        tuple: (label_turtle, hearts_turtle) for cleanup
    """
    # Create label
    label_turtle = turtle.Turtle()
    label_turtle.hideturtle()
    label_turtle.penup()
    label_turtle.goto(x, y)
    label_turtle.color("#ffffff")
    label_turtle.write(label, align="left", font=("Courier", 11, "bold"))
    
    # Create hearts
    hearts_turtle = turtle.Turtle()
    hearts_turtle.hideturtle()
    hearts_turtle.penup()
    hearts_turtle.speed(0)
    
    if horizontal:
        # Draw hearts horizontally
        heart_x = x + 70  # Offset from label
        for i in range(lives):
            draw_heart(hearts_turtle, heart_x + (i * 20), y + 5, size=7, color=color)
    else:
        # Draw hearts vertically
        for i in range(lives):
            draw_heart(hearts_turtle, x + 10, y - 25 - (i * 20), size=7, color=color)
    
    screen.update()
    return label_turtle, hearts_turtle


def clear_turtles(*turtles):
    """Clear and hide multiple turtles.
    
    Args:
        *turtles: Variable number of turtle objects to clear
    """
    for t in turtles:
        if t is not None:
            try:
                t.clear()
                t.hideturtle()
            except Exception:
                pass