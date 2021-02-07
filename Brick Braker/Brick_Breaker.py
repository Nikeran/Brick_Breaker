"""Game resolution: 1366x768"""
"""CHEAT COSE UP+DOWN+UP"""
from tkinter import Tk, Canvas, PhotoImage, Button, Label, Radiobutton, IntVar
from random import randint as rand, seed
from time import sleep, time
from ast import literal_eval

seed(time())


def enter_canvas(page, current_page):
    """changes through the game pages, packing and unpacking them
    :param page is the page that you intend to go
    :param current_page
    """
    current_page.pack_forget()
    if page == 0:
        enter_menu()
    elif page == 1:
        enter_game()
    elif page == 3:
        enter_settings()
    elif page==4:
        enter_instructions()

def boss_key(event):
    """hides and unhides the window through the window_hidden variable"""
    global window_hidden
    if event.keysym == boss_keysym:
        if window_hidden:
            window_hidden = False
            window.attributes('-alpha', 1.0)
        else:
            window_hidden = True
            window.attributes('-alpha', 0)

# initialises the window
window = Tk()
window.title("Brick_Breaker")
window.geometry("1366x768")



settings_image = PhotoImage(file="settings_button.png")
back_image = PhotoImage(file="arrow-back.gif")
game_name = PhotoImage(file="title_picture.gif")
ball = PhotoImage(file="the_ball.png")

# list of brick pictures by category and endurence
brick = []
brick.append([PhotoImage(file="wood_brick.png"), PhotoImage(file="wood_brick_1.png")])
brick.append([PhotoImage(file="normal_brick.png"), PhotoImage(file="normal_brick_1.png"), PhotoImage(file="normal_brick_2.png")])
brick.append([PhotoImage(file="stone_brick.png"), PhotoImage(file="stone_brick_1.png"), PhotoImage(file="stone_brick_2.png"),PhotoImage(file="stone_brick_3.png")])
brick.append([PhotoImage(file="ceramic_brick.png")])

window.bind("<Key>", boss_key)
window_hidden = False


# GLOBAL VARIABLES

bar_move_left = False
bar_move_right = False
delay = 0.005
initials = ""
left_keysym = "Left"
right_keysym = "Right"
pause_keysym = "p"
unpause_keysym = "o"
boss_keysym = "b"
pause = False
game_score = 0
step =[0]*3
score_board ={}






def enter_menu():
    """ main menu canvas"""

    global score_board

    with open("score_file.txt", 'w') as score_file:
        score_file.write(str(score_board))

    def move_brick(index):
        """ first try at default animation for the the menu"""
        global brick
        x, y = menu.coords(menu_brick[index])
        if y > 780:
            x = rand(10, 1300)
            y = rand(-700, -30)
            brick_number = rand(0, 3)
            menu.itemconfig(menu_brick[index], image=brick[brick_number][0])
        else:
            y += 1

        menu.coords(menu_brick[index], x, y)

    # load the menu canvas
    menu = Canvas(window)
    menu.pack()
    menu.configure(bg="black", width=1350, height=750)

    game_name_label = Label(menu, image=game_name, width=455, height=256)
    game_name_label.place(x=683, y=100)


    #score board on the menu
    score_board_sorted = sorted(score_board.items())
    score_board_text = "TOP SCORES\n"
    index=0
    for name, score in score_board_sorted[::-1]:
        score_board_text += name + " : " + str(score) + "\n"
        if index == 4:
            break
        else:
            index += 1

    top_score = menu.create_text(10, 20, text=score_board_text, fill="#7C2816", font="Times 30 italic bold")
    menu.coords(top_score, 900, 550)

    # buttons
    new_game_button = Button(menu, width=13, height=1, text="NEW_GAME", bg="#7C2816", font="Times 30 italic bold",
                             command=lambda: enter_canvas(1, menu), activebackground="#652214")
    new_game_button.place(x=100, y=350)

    instructions_button = Button(menu, width=13, height=1, text="INSTRUCTIONS", bg="#7C2816",
                                font="Times 30 italic bold",
                                command=lambda: enter_canvas(4,menu), activebackground="#652214")
    instructions_button.place(x=100, y=460)

    quit_button = Button(menu, width=13, height=1, text="EXIT", bg="#7C2816",
                                font="Times 30 italic bold",
                                command=window.destroy, activebackground="#652214")
    quit_button.place(x=100, y=570)

    settings_button = Button(menu, image=settings_image, width=150, height=150, command=lambda: enter_canvas(3, menu))
    settings_button.place(x=0, y=0)

    # hardcoding of the menu bricks (experiment on learning the library)
    menu_brick_x = [rand(10, 1300), rand(10, 1300), rand(10, 1300)]
    menu_brick_y = [-30, rand(-700, -30), rand(-700, -30)]
    brick_number = [rand(0, 3), rand(0, 3), rand(0, 3)]
    menu_brick = []
    menu_brick.append(menu.create_image(menu_brick_x[0], menu_brick_y[0], image=brick[brick_number[0]][0]))
    menu_brick.append(menu.create_image(menu_brick_x[1], menu_brick_y[1], image=brick[brick_number[1]][0]))
    menu_brick.append(menu.create_image(menu_brick_x[2], menu_brick_y[2], image=brick[brick_number[2]][0]))


    # brick animation loop
    while True:

        for index in range(3):
            move_brick(index)

        sleep(0.01)
        window.update()







def enter_game():
    """game canvas"""
    game_bricks = []
    game_balls = []
    global game_score, delay, initials, left_keysym, right_keysym, pause_keysym, unpause_keysym, pause, step, scoreboard
    game_score = 0
    game_time = 0
    delay = 0.01
    initials = ""
    pause = False

    def create_random_brick(brick_number):
        """
        this function generates a random bricks,
        after it confirms it does not overlap with another one
        """

        global brick

        valid = False
        while not valid:
            valid = True
            x = rand(50, 1300)
            y = rand(30, 500)

            for brick_instance in game_bricks:
                x_brick, y_brick = game.coords(brick_instance[0])
                if x < (x_brick + 30) and (x + 30) > x_brick and y < (y_brick + 20) and (y + 20) > y_brick:
                    valid = False
                    break

        # this is really ugly USE CLASSES IN THE FUTURE!!!
        # brick[image,[image_category, image_category_position], index]
        game_bricks.append([game.create_image(x, y, image=brick[brick_number][0]), [brick_number, 0], len(game_bricks)])

    def create_ball():
        """create a ball at specific coordinates which moves diagonally"""
        x = 1350 / 2
        y = 650

        # the directions of the ball
        x_direction = -1
        y_direction = -1

        game_balls.append([game.create_image(x, y, image=ball), x_direction, y_direction])

    def game_run():
        """ this function executes each frame of the game, doing all the collision checks"""
        global bar_move_left, bar_move_right, delay

        ball_index = 0
        for ball in game_balls:

            ball_position = game.coords(ball[0])
            ball_position.append(ball_position[0] + 30)
            ball_position.append(ball_position[1] + 20)

            # wall collision
            if ball_position[0] < 5 or ball_position[2] > 1370:
                ball[1] = -ball[1]

            if ball_position[1] < 0:
                ball[2] = -ball[2]

            # exit through bottom
            if ball_position[3] > 780:
                game.delete(game_balls[ball_index])
                game_balls.pop(ball_index)

            # brick collision
            for brick_instance in game_bricks:
                brick_position = game.coords(brick_instance[0])
                brick_position.append(brick_position[0] + 30)
                brick_position.append(brick_position[1] + 20)

                if (int(ball_position[0]) <= brick_position[2] and int(ball_position[2]) >= brick_position[0] and
                        int(ball_position[1]) <= brick_position[3] and int(ball_position[3]) >= brick_position[1]):

                    if ((int(ball_position[0]) == brick_position[2]) or (int(ball_position[2]) == brick_position[0] or
                                                                         int(ball_position[0]) == (
                                                                                 brick_position[2] - 1)) or int(
                        ball_position[2]) == (brick_position[0] + 1)):
                        ball[1] = -ball[1]

                    if (ball_position[1] == brick_position[3]) or (ball_position[3] == brick_position[1]):
                        ball[2] = -ball[2]

                    crack_brick(brick_instance)
                    print(ball_position, ' ', brick_position, '\n')

                # flush last to added coordinates
                brick_position.pop()
                brick_position.pop()

            # bar collision
            # !!! It changes the coordinates to float
            x, y, z, t = game.coords(bar)
            if (ball_position[0] <= z and ball_position[2] >= x and
                    ball_position[1] <= t and ball_position[3] >= y + 10):
                # bar collision formula
                ball[1] = ((ball_position[0] + 15) - (x + 75)) / 30
                ball[2] = -ball[2]

            game.move(ball[0], ball[1], ball[2])

            # flush last to added coordinates
            ball_position.pop()
            ball_position.pop()

            ball_index += 1

            # formulas to keep the speed of the bar constant as the game accelerates
            if bar_move_left == True and x > 0:
                game.move(bar, -(delay / 0.005) * 8, 0)
            if bar_move_right == True and z < 1360:
                game.move(bar, (delay / 0.005) * 8, 0)

    def create_bar():
        return game.create_rectangle(1350 / 2 - 2 * 30 - 15, 742, 1350 / 2 + 2 * 30 - 15, 762, fill="green")

    def move_bar(event, move):
        """
        depending on the preseted keys this moves the bar to the left or to the right while also
        doing checks for the boss key, the cheat code, and the pauses
        """
        global bar_move_left, bar_move_right, pause, step
        x, y, z, t = game.coords(bar)


        if move == False:
            boss_key(event)


        # cheat code
        if move == False:
            if step[0]:
                if step[1]:
                    if event.keysym == "Up":
                        create_ball()
                        step[0]=0
                        step[1]=0
                    else:
                        step[0]=0
                        step[1]=0
                else:
                    if event.keysym == "Down":
                        step[1] = 1
                    else:
                        step[0]=0
            else:
                if event.keysym == "Up":
                    step[0] = 1



        # integrate pause in keyboard input
        if event.keysym == pause_keysym:
            pause = True
        elif event.keysym == unpause_keysym:
            pause = False
        else:
            if move:
                if event.keysym == left_keysym:
                    if x > 0:
                        bar_move_left = True
                        bar_move_right = False
                if event.keysym == right_keysym:
                    if (x + 150) < 1360:
                        bar_move_right = True
                        bar_move_left = False
            else:
                bar_move_left = False
                bar_move_right = False

    def crack_brick(brick_instance):
        """
        changes the image of the brick to the corresponding cracked version, using variables saved
        in the brick array(the indexes and position in the brickimages list) until we reach the end
        of the list, at which point we eliminate that brick from the global list
        """
        global game_score, delay

        if brick_instance[1][1] < len(brick[brick_instance[1][0]]) - 1:
            brick_instance[1][1] += 1
            game.itemconfig(brick_instance[0], image=brick[brick_instance[1][0]][brick_instance[1][1]])

        else:
            game.delete(brick_instance[0])
            game_score += 1
            game.itemconfig(score_text, text="SCORE: " + str(game_score))

            index_base = brick_instance[2]
            game_bricks.pop(brick_instance[2])
            for brick_instance in game_bricks:
                if brick_instance[2] > index_base:
                    brick_instance[2] -= 1

            # ball acceleration
            delay /= 1.2

    def game_end():
        """start the end game screen"""
        global initials
        end = True

        game.itemconfig(game_over_text,
                        text="GAME OVER\n   FINAL SCORE: " + str(game_score) + "\n     ENTER 3 INITIALS:" + initials,
                        font="Times 30 italic bold", fill="#7C2816")
        window.update()

    def exit_game():
        """exits the game and saves the score"""
        global score_board
        score_board[initials] = game_score
        enter_canvas(0, game)


    def get_initials(event):
        global initials

        try:
            if len(initials) < 3 and event.char.isalpha():
                initials += event.char.upper()
                window.update()
        except:
            pass
        game.itemconfig(game_over_text,
                        text="GAME OVER\n   FINAL SCORE: " + str(game_score) + "\n      ENTER 3 INITIALS:" + initials)
        window.update()

    # game starts here
    window.bind("<KeyPress>", lambda e: move_bar(event=e, move=True))
    window.bind("<KeyRelease>", lambda e: move_bar(event=e, move=False))

    game = Canvas(window)
    game.pack()
    game.configure(bg="black", width=1350, height=750)


    #initialise the game with 20 random bricks
    for bricks_number in range(20):
        create_random_brick(rand(0, 3))
    create_ball()
    bar = create_bar()

    score_text = game.create_text(65, 15, text="SCORE: " + str(game_score), font="Times 20 italic bold", fill="#7C2816")
    game_over_text = game.create_text(650, 600, text="")

    # game loop
    while True:
        if not pause:
            # create random bricks as the game progresses
            game_time += 1
            if (game_time % 50) == 0:
                rgn = rand(1, 10)
                if rgn == 10:
                    create_random_brick(rand(0, 3))

            #load frame
            game_run()

            #end if there are no more balls
            if len(game_balls) == 0:
                game_end()
                break

            sleep(delay)

        window.update()

    #get the initials at the end of the game
    window.bind("<Key>", get_initials)
    menu_button = Button(game, width=13, height=1, text="MENU", bg="#7C2816", font="Times 30 italic bold",
                         command= exit_game, activebackground="#652214")
    menu_button.place(x=400, y=450)

    window.mainloop()







def enter_settings():
    """ enter the canvas which sets the key binds for each command of the game"""
    global left_keysym, right_keysym, pause_keysym, unpause_keysym, boss_keysym



    def change_left(event):
        global left_keysym
        boss_key(event)
        left_keysym = event.keysym
        left_button['text'] = "MOVE LEFT: " + left_keysym

    def change_right(event):
        global right_keysym
        boss_key(event)
        right_keysym = event.keysym
        right_button['text'] = "MOVE RIGHT: " + right_keysym

    def change_pause(event):
        global pause_keysym
        boss_key(event)
        pause_keysym = event.keysym
        pause_button['text'] = "PAUSE: " + pause_keysym

    def change_unpause(event):
        global unpause_keysym
        boss_key(event)
        unpause_keysym = event.keysym
        unpause_button['text'] = "UNPAUSE: " + unpause_keysym

    def change_boss(event):
        global boss_keysym
        boss_key(event)
        boss_keysym = event.keysym
        boss_button['text'] = "BOSS KEY: " + boss_keysym

    def select_key(key):
        if key == left_keysym:
            window.bind("<Key>",change_left)
        elif key == right_keysym:
            window.bind("<Key>", change_right)
        elif key == pause_keysym:
            window.bind("<Key>", change_pause)
        elif key == unpause_keysym:
            window.bind("<Key>", change_unpause)
        elif key == boss_keysym:
            window.bind("<Key>", change_boss)




    settings = Canvas(window)
    settings.pack()
    settings.configure(bg="black", width=1350, height=750)
    button_variable = IntVar()

    #key bind buttons
    back_button = Button(settings, width=100, height=100, image=back_image, command=lambda: enter_canvas(0, settings))
    back_button.place(x=0, y=0)


    settings.create_text(680, 100, text = "KEY BINDS", font="Times 50 italic bold", fill ="#652214" )


    left_button = Radiobutton(settings, width=20, height=1, text="MOVE LEFT: " + left_keysym,
                              font="Times 30 italic bold",
                              background="#652214", command= lambda : select_key(left_keysym),
                              variable=button_variable, indicatoron=0, value = 1)
    left_button.place(x=450, y=250)

    right_button = Radiobutton(settings, width=20, height=1, text="MOVE RIGHT: " + right_keysym,
                              font="Times 30 italic bold",
                              background="#652214", command= lambda : select_key(right_keysym),
                              variable=button_variable, indicatoron=0, value = 2)
    right_button.place(x=450, y=350)

    pause_button = Radiobutton(settings, width=20, height=1, text="PAUSE: " + pause_keysym,
                               font="Times 30 italic bold",
                               background="#652214", command=lambda: select_key(pause_keysym),
                               variable=button_variable, indicatoron=0, value=3)
    pause_button.place(x=450, y=450)

    unpause_button = Radiobutton(settings, width=20, height=1, text="UNPAUSE: " + unpause_keysym,
                               font="Times 30 italic bold",
                               background="#652214", command=lambda: select_key(unpause_keysym),
                               variable=button_variable, indicatoron=0, value=4)
    unpause_button.place(x=450, y=550)

    boss_button = Radiobutton(settings, width=20, height=1, text="BOSS KEY: " + boss_keysym,
                                 font="Times 30 italic bold",
                                 background="#652214", command=lambda: select_key(boss_keysym),
                                 variable=button_variable, indicatoron=0, value=5)
    boss_button.place(x=450, y=650)


    window.mainloop()







def enter_instructions():
    """enter the instructions canvas"""



    instructions = Canvas(window)
    instructions.pack()
    instructions.configure(bg="black", width=1350, height=750)

    instructions_text=("THE OBJECTIVE OF THE GAME IS TO BREAK AS \nMANY BRICKS AS YOU CAN BEFORE AND NOT LET THE BALL FALL \n" +
                       "BUT WATCH OUT BECAUSE THE GAME \nACCELERATES THE MORE BRICKS YOU BRAKE \n"+
                       "AND SOME BRICKS BREAK EASIER THAN OTHERS\n"+
                       "THE CLOSER THE MIDDLE OF THE BAR YOU CATCH \nTHE BALL THE MORE PERPENDICULAR IT WILL GO BACK UP\n"+
                       "BRICKS WILL CONTINUE TO SPAWN AS THE GAME PROGRESSES\n"+
                       "AT THE END ENTER DON'T FORGET TO ENTER 3 INITIALS \n"+
                       "       NOW GO AND GIVE IT A SHOT\n")

    instructions.create_text(680, 350, text = instructions_text, font="Times 30 italic bold", fill ="#652214" )

    back_button = Button(instructions, width=100, height=100, image=back_image, command=lambda: enter_canvas(0, instructions))
    back_button.place(x=0, y=0)








# program starts here
with open("score_file.txt") as score_file:
    score = score_file.read()
# get the score record from the score file
score_board = literal_eval(score)

#start by entering the menu
enter_menu()

