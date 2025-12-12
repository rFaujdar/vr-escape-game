import turtle
import random
import time
from ui_elements import draw_heart, clear_turtles


def level_2_hangman(state, screen, text, lives_display, player, update_displays, show_message, victory):
    """RACEMAX hangman level with improved UI."""
    lives_key = 'lives'
    active_key = 'game_active'

    # Clear screen with better background color
    screen.bgcolor("#1a0a0a")
    text.clear()
    
    # Title - moved down to avoid cramping
    text.color("#ff6b35")
    text.goto(0, 200)
    text.write("LEVEL 2: RACEMAX", align="center", font=("Courier", 20, "bold"))
    
    # Subtitle - below title with good spacing
    subtitle = turtle.Turtle()
    subtitle.hideturtle()
    subtitle.color("#ffaa00")
    subtitle.penup()
    subtitle.goto(0, 165)
    subtitle.write("Type letters to guess the word before the truck crushes you!", 
                   align="center", font=("Courier", 11, "normal"))

    words = ["ESCAPE", "REALITY", "SYSTEM", "CYBER", "DIGITAL", "MATRIX", "PLAYER", "PORTAL"]
    word = random.choice(words)
    guessed = ["_"] * len(word)

    # Pre-fill some letters
    num_hints = max(1, len(word) // 3)
    hint_positions = random.sample(range(len(word)), num_hints)
    for pos in hint_positions:
        guessed[pos] = word[pos]

    used_letters = []
    wrong_guesses = 0
    max_wrong = 6
    hints_used = 0
    max_hints = 2
    
    # Flag to prevent multiple victory calls
    victory_called = False

    # Truck
    truck = turtle.Turtle()
    truck.shape("square")
    truck.color("#cc0000")
    truck.shapesize(3, 4)
    truck.penup()
    truck.goto(-350, 0)

    # Display
    word_display = turtle.Turtle()
    word_display.hideturtle()
    word_display.color("white")
    word_display.penup()
    word_display.goto(0, 60)

    used_display = turtle.Turtle()
    used_display.hideturtle()
    used_display.color("#aaaaaa")
    used_display.penup()
    used_display.goto(0, 10)
    
    # Track hearts turtle for cleanup
    hearts_t = None
    wrong_text = None

    def update_word_display():
        nonlocal hearts_t, wrong_text
        
        word_display.clear()
        word_display.write(" ".join(guessed), align="center", font=("Courier", 28, "bold"))
        used_display.clear()
        used_text = (
            "Used: " + ' '.join(sorted(used_letters))
            + "   |   Hints: " + str(max_hints - hints_used)
        )
        used_display.write(used_text, align="center", font=("Courier", 12, "normal"))
        
        # Update lives display with hearts
        lives_display.clear()
        lives_display.goto(-350, 250)
        lives_display.write("Lives:", font=("Courier", 14, "bold"))
        
        # Clear previous hearts
        if hearts_t is not None:
            try:
                hearts_t.clear()
                hearts_t.hideturtle()
            except Exception:
                pass
        
        # Draw hearts
        hearts_t = turtle.Turtle()
        hearts_t.hideturtle()
        hearts_t.speed(0)
        for i in range(state[lives_key]):
            draw_heart(hearts_t, -280 + (i * 18), 255, size=6, color="#ff0066")
        
        # Clear previous wrong text
        if wrong_text is not None:
            try:
                wrong_text.clear()
                wrong_text.hideturtle()
            except Exception:
                pass
        
        # Add wrong guesses text
        wrong_text = turtle.Turtle()
        wrong_text.hideturtle()
        wrong_text.penup()
        wrong_text.goto(-280 + (state[lives_key] * 18) + 15, 250)
        wrong_text.color("cyan")
        wrong_text.write(f"| Wrong: {wrong_guesses}/{max_wrong}", font=("Courier", 14, "bold"))

        # Truck distance warning
        try:
            distance = 350 + truck.xcor()
        except Exception:
            distance = 999
        if distance < 150:
            used_display.color("#ff0000")
        elif distance < 250:
            used_display.color("#ff9900")
        else:
            used_display.color("#aaaaaa")

    def cleanup_hangman():
        """Clean up all hangman UI elements"""
        nonlocal hearts_t, wrong_text
        try:
            instr_turtle.clear()
        except Exception:
            pass
        try:
            word_display.clear()
        except Exception:
            pass
        try:
            used_display.clear()
        except Exception:
            pass
        try:
            truck.hideturtle()
        except Exception:
            pass
        try:
            subtitle.clear()
        except Exception:
            pass
        try:
            text.clear()
        except Exception:
            pass
        try:
            lives_display.clear()
        except Exception:
            pass
        if hearts_t is not None:
            try:
                hearts_t.clear()
                hearts_t.hideturtle()
            except Exception:
                pass
        if wrong_text is not None:
            try:
                wrong_text.clear()
                wrong_text.hideturtle()
            except Exception:
                pass

    def guess_letter(letter):
        nonlocal wrong_guesses, word, guessed, used_letters, hints_used, victory_called

        # Prevent actions after victory
        if victory_called or "_" not in guessed:
            return

        letter = letter.upper()
        if letter in used_letters or not letter.isalpha():
            return

        used_letters.append(letter)

        if letter in word:
            for i, char in enumerate(word):
                if char == letter:
                    guessed[i] = letter
            if truck.xcor() > -350:
                truck.setx(truck.xcor() - 30)
            word_display.color("#00ff00")
            update_word_display()
            screen.update()
            time.sleep(0.2)
            word_display.color("white")
        else:
            wrong_guesses += 1
            truck.setx(truck.xcor() + 50)
            word_display.color("#ff0000")
            update_word_display()
            screen.update()
            time.sleep(0.3)
            word_display.color("white")

            if wrong_guesses >= max_wrong:
                state[lives_key] -= 1
                if state[lives_key] <= 0:
                    state[active_key] = False
                    show_message("CRUSHED! GAME OVER", 3)
                    return
                else:
                    show_message(f"CRUSHED! {state[lives_key]} lives remaining. Retry!", 2)
                    word = random.choice(words)
                    guessed[:] = ["_"] * len(word)
                    num_hints_local = max(1, len(word) // 3)
                    hint_positions_local = random.sample(range(len(word)), num_hints_local)
                    for pos in hint_positions_local:
                        guessed[pos] = word[pos]
                    used_letters.clear()
                    wrong_guesses = 0
                    truck.goto(-350, 0)

        update_word_display()
        try:
            screen.update()
        except Exception:
            state[active_key] = False
            return

        # Check win - only call victory ONCE
        if "_" not in guessed and not victory_called:
            victory_called = True
            state[active_key] = False  # Stop the game loop
            cleanup_hangman()
            victory()

    # Ensure the screen is listening
    screen.listen()

    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        screen.onkey(lambda ch=char: guess_letter(ch), char.lower())
        screen.onkey(lambda ch=char: guess_letter(ch), char.upper())

    def use_hint():
        nonlocal hints_used, guessed, word, victory_called
        
        if victory_called or "_" not in guessed:
            return
            
        if hints_used >= max_hints:
            show_message("No hints remaining!", 1)
            return
        unrevealed = [i for i, g in enumerate(guessed) if g == "_"]
        if not unrevealed:
            return
        pos = random.choice(unrevealed)
        guessed[pos] = word[pos]
        hints_used += 1
        if truck.xcor() > -350:
            truck.setx(max(truck.xcor() - 40, -350))
        update_word_display()
        screen.update()
        word_display.color("#00ffff")
        time.sleep(0.2)
        word_display.color("white")
        
        if "_" not in guessed and not victory_called:
            victory_called = True
            state[active_key] = False
            time.sleep(0.3)
            cleanup_hangman()
            victory()

    screen.onkey(use_hint, 'h')
    screen.onkey(use_hint, 'H')

    # Instructions on right side
    instr_turtle = turtle.Turtle()
    instr_turtle.hideturtle()
    instr_turtle.color('#ffaa00')
    instr_turtle.penup()
    instr_turtle.goto(280, 120)
    
    instr_text = (
        "== CONTROLS ==\n\n"
        "Type Letters\n"
        "  Guess word\n\n"
        "Press H\n"
        "  Use hint\n"
        "  (2 total)\n\n"
        "Press ESC\n"
        "  Exit game"
    )
    instr_turtle.write(instr_text, align='left', font=("Courier", 10, "normal"))

    update_word_display()

    # Run the level loop - with proper exit condition
    try:
        while state[active_key] and "_" in guessed and not victory_called:
            try:
                screen.update()
            except Exception:
                state[active_key] = False
                break
            time.sleep(0.1)
    finally:
        # Only cleanup if victory wasn't called (victory handles its own cleanup)
        if not victory_called:
            cleanup_hangman()