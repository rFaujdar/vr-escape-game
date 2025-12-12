import turtle
import random
import time
from ui_elements import draw_heart, create_turtle, clear_turtles


def reset_word(words):
    word = random.choice(words)
    guessed = ["_"] * len(word)
    num_hints = max(1, len(word) // 3)
    for pos in random.sample(range(len(word)), num_hints):
        guessed[pos] = word[pos]
    return word, guessed


def level_2_hangman(state, screen, text, lives_display, player, update_displays, show_message, victory, game_over_ending=None):
    lives_key = 'lives'
    active_key = 'game_active'
    
    screen.bgcolor("#1a0a0a")
    text.clear()
    text.color("#ff6b35")
    text.goto(0, 200)
    text.write("LEVEL 2: THE MIND GAME", align="center", font=("Courier", 20, "bold"))
    
    subtitle = create_turtle()
    subtitle.color("#ffaa00")
    subtitle.goto(0, 165)
    subtitle.write("Guess the word before your memories are extracted!", 
                   align="center", font=("Courier", 11, "normal"))

    words = ["ESCAPE", "REALITY", "SYSTEM", "CYBER", "DIGITAL", "MATRIX", "PLAYER", "PORTAL"]
    word, guessed = reset_word(words)
    
    used_letters = []
    wrong_guesses = 0
    max_wrong = 4
    hints_used = 0
    max_hints = 2
    victory_called = False
    game_over_called = False

    truck = turtle.Turtle()
    truck.shape("square")
    truck.color("#cc0000")
    truck.shapesize(3, 4)
    truck.penup()
    truck.goto(-350, 0)
    truck.hideturtle()

    word_display = create_turtle()
    word_display.color("white")
    word_display.goto(0, 60)

    used_display = create_turtle()
    used_display.color("#aaaaaa")
    used_display.goto(0, 10)
    
    hearts_t = None
    wrong_text = None

    def update_word_display():
        nonlocal hearts_t, wrong_text
        
        word_display.clear()
        word_display.write(" ".join(guessed), align="center", font=("Courier", 28, "bold"))
        
        used_display.clear()
        used_display.write(f"Used: {' '.join(sorted(used_letters))}   |   Hints: {max_hints - hints_used}",
                          align="center", font=("Courier", 12, "normal"))
        
        lives_display.clear()
        lives_display.goto(-350, 250)
        lives_display.write("Lives:", font=("Courier", 14, "bold"))
        
        clear_turtles(hearts_t, wrong_text)
        
        hearts_t = create_turtle()
        for i in range(state[lives_key]):
            draw_heart(hearts_t, -280 + (i * 18), 255, size=6, color="#ff0066")
        
        wrong_text = create_turtle()
        wrong_text.goto(-280 + (state[lives_key] * 18) + 15, 250)
        wrong_text.color("cyan")
        wrong_text.write(f"| Wrong: {wrong_guesses}/{max_wrong}", font=("Courier", 14, "bold"))

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
        nonlocal hearts_t, wrong_text
        clear_turtles(instr_turtle, word_display, used_display, subtitle, hearts_t, wrong_text)
        try:
            truck.hideturtle()
            text.clear()
            lives_display.clear()
        except Exception:
            pass

    def handle_wrong_guess():
        nonlocal wrong_guesses, word, guessed, used_letters, game_over_called
        
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
                if not game_over_called:
                    game_over_called = True
                    state[active_key] = False
                    cleanup_hangman()
                    if game_over_ending:
                        game_over_ending()
                return True
            else:
                show_message(f"MEMORY EXTRACTED! {state[lives_key]} lives remaining. Retry!", 2, -80)
                word, guessed[:] = reset_word(words)
                used_letters.clear()
                wrong_guesses = 0
                truck.goto(-350, 0)
        return False

    def check_victory():
        nonlocal victory_called
        if "_" not in guessed and not victory_called and not game_over_called:
            victory_called = True
            state[active_key] = False
            cleanup_hangman()
            victory()
            return True
        return False

    def guess_letter(letter):
        nonlocal wrong_guesses, word, guessed, used_letters, victory_called, game_over_called

        if victory_called or game_over_called or "_" not in guessed:
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
            if handle_wrong_guess():
                return

        update_word_display()
        try:
            screen.update()
        except Exception:
            state[active_key] = False
            return

        check_victory()

    screen.listen()
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        screen.onkey(lambda ch=char: guess_letter(ch), char.lower())
        screen.onkey(lambda ch=char: guess_letter(ch), char.upper())

    def use_hint():
        nonlocal hints_used, guessed, word, victory_called, game_over_called
        
        if victory_called or game_over_called or "_" not in guessed:
            return
            
        if hints_used >= max_hints:
            show_message("No hints remaining!", 1, -80)
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
        
        if "_" not in guessed and not victory_called and not game_over_called:
            victory_called = True
            state[active_key] = False
            time.sleep(0.3)
            cleanup_hangman()
            victory()

    screen.onkey(use_hint, 'h')
    screen.onkey(use_hint, 'H')

    instr_turtle = create_turtle()
    instr_turtle.color('#ffaa00')
    instr_turtle.goto(280, 120)
    instr_turtle.write("== CONTROLS ==\n\nType Letters\n  Guess word\n\nPress H\n  Use hint\n  (2 total)\n\nPress ESC\n  Exit game",
                      align='left', font=("Courier", 10, "normal"))

    update_word_display()

    try:
        while state[active_key] and "_" in guessed and not victory_called and not game_over_called:
            try:
                screen.update()
            except Exception:
                state[active_key] = False
                break
            time.sleep(0.1)
    finally:
        if not victory_called and not game_over_called:
            cleanup_hangman()