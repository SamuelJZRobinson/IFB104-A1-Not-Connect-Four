
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: n10464948
#    Student name: Samuel Robinson
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  NOT CONNECT-4
#
#  This assignment tests your skills at processing data stored in
#  lists, creating reusable code and following instructions to display
#  a complex visual image. The incomplete Python program below is
#  missing a crucial function, "play_game". You are required to
#  complete this function so that when the program is run it fills
#  a grid with various rectangular tokens, using data stored in a
#  list to determine which tokens to place and where. See the
#  instruction sheet accompanying this file for full details.
#
#  Note that this assignment is in two parts, the second of which
#  will be released only just before the final deadline. This
#  template file will be used for both parts and you will submit
#  your final solution as a single Python 3 file, whether or not you
#  complete both parts of the assignment.
#
#--------------------------------------------------------------------#  



#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must NOT rely on any non-standard Python
# modules that need to be downloaded and installed separately,
# because the markers will not have access to such modules.
from turtle import *
from math import *
from random import *

# Define constant values for setting up the drawing canvas
cell_size = 100 # pixels (default is 100)
num_columns = 7 # cells (default is 7)
num_rows = 6 # cells (default is 6)
x_margin = cell_size * 2.75 # pixels, the size of the margin left/right of the board
y_margin = cell_size // 2 # pixels, the size of the margin below/above the board
canvas_height = num_rows * cell_size + y_margin * 2
canvas_width = num_columns * cell_size + x_margin * 2

# Validity checks on board size
assert cell_size >= 80, 'Cells must be at least 80x80 pixels in size'
assert num_columns >= 7, 'Board must be at least 7 columns wide'
assert num_rows >= 6, 'Board must be at least 6 rows high'

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# manage the drawing canvas for your image.  You should not change
# any of the code in this section.
#

# Set up the canvas and draw the background for the overall image
def create_drawing_canvas(mark_legend_spaces = False, # show text for legend
                          mark_axes = True, # show labels on axes
                          bg_colour = 'light grey', # background colour
                          line_colour = 'slate grey'): # line colour for board
    
    # Set up the drawing canvas with enough space for the board and
    # legend
    setup(canvas_width, canvas_height)
    bgcolor(bg_colour)

    # Draw as quickly as possible
    tracer(False)

    # Get ready to draw the board
    penup()
    color(line_colour)
    width(2)

    # Determine the left-bottom coords of the board
    left_edge = -(num_columns * cell_size) // 2 
    bottom_edge = -(num_rows * cell_size) // 2

    # Draw the horizontal grid lines
    setheading(0) # face east
    for line_no in range(0, num_rows + 1):
        penup()
        goto(left_edge, bottom_edge + line_no * cell_size)
        pendown()
        forward(num_columns * cell_size)
        
    # Draw the vertical grid lines
    setheading(90) # face north
    for line_no in range(0, num_columns + 1):
        penup()
        goto(left_edge + line_no * cell_size, bottom_edge)
        pendown()
        forward(num_rows * cell_size)

    # Mark the centre of the board (coordinate [0, 0])
    penup()
    home()
    dot(10)

    # Optionally label the axes
    if mark_axes:

        # Define the font and position for the labels
        small_font = ('Arial', (18 * cell_size) // 100, 'normal')
        y_offset = (27 * cell_size) // 100 # pixels

        # Draw each of the labels on the x axis
        penup()
        for x_label in range(0, num_columns):
            goto(left_edge + (x_label * cell_size) + (cell_size // 2), bottom_edge - y_offset)
            write(chr(x_label + ord('a')), align = 'center', font = small_font)

        # Draw each of the labels on the y axis
        penup()
        x_offset, y_offset = 7, 10 # pixels
        for y_label in range(0, num_rows):
            goto(left_edge - x_offset, bottom_edge + (y_label * cell_size) + (cell_size // 2) - y_offset)
            write(str(y_label + 1), align = 'right', font = small_font)

    # Optionally mark the spaces for drawing the legend
    if mark_legend_spaces:
        # Font for marking the legend's position
        big_font = ('Arial', (24 * cell_size) // 100, 'normal')
        # Left side
        goto(-(num_columns * cell_size) // 2 - 50, -25)
        write('Put your token\ndescriptions here', align = 'right', font = big_font)    
        # Right side
        goto((num_columns * cell_size) // 2 + 50, -25)
        write('Put your token\ndescriptions here', align = 'left', font = big_font)    

    # Reset everything ready for the student's solution
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)


# End the program and release the drawing canvas to the operating
# system.  By default the cursor (turtle) is hidden when the
# program ends.  Call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any drawing still in progress is displayed
    if hide_cursor:
        hideturtle()
    done()
    
#
#--------------------------------------------------------------------#



#-----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the "play_game" function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the "random_game" function appearing below.
# Your program must work correctly for any data set that can be
# generated by the "random_game" function.
#
# Each of the data sets is a list of instructions, each specifying
# in which column to drop a particular type of game token.  The
# general form of each instruction is
#
#     [column, token_type]
#
# where the columns range from 'a' to 'g' and the token types
# range from 1 to 4.
#
# Note that the fixed patterns below all assume the board has its
# default dimensions of 7x6 cells.
#

# The following data sets each draw just one token type once
fixed_game_a0 = [['a', 1]]
fixed_game_a1 = [['b', 2]]
fixed_game_a2 = [['c', 3]]
fixed_game_a3 = [['d', 4]]

# The following data sets each draw just one type
# of token multiple times
fixed_game_a4 = [['c', 1], ['f', 1], ['g', 1], ['c', 1]] 
fixed_game_a5 = [['d', 2], ['d', 2], ['a', 2], ['c', 2]] 
fixed_game_a6 = [['c', 3], ['f', 3], ['g', 3], ['c', 3]] 
fixed_game_a7 = [['f', 4], ['f', 4], ['c', 4], ['c', 4]]

# The following small data sets each draw all four kinds
# of token
fixed_game_a8 = [['e', 3], ['e', 4], ['f', 3], ['e', 1],
                 ['c', 2], ['g', 4]]

fixed_game_a9 = [['g', 3], ['d', 4], ['b', 3], ['e', 1],
                 ['f', 2], ['g', 4], ['c', 2], ['g', 4]]

fixed_game_a10 = [['f', 3], ['d', 1], ['c', 3], ['c', 4],
                  ['e', 2], ['b', 1], ['b', 3]]

fixed_game_a11 = [['e', 3], ['c', 3], ['d', 3], ['c', 2],
                  ['c', 3], ['d', 4], ['a', 4], ['f', 1]]

fixed_game_a12 = [['f', 1], ['b', 4], ['f', 1], ['f', 4],
                  ['e', 2], ['a', 3], ['c', 3], ['b', 2],
                  ['a', 2]]

fixed_game_a13 = [['b', 3], ['f', 4], ['d', 4], ['b', 1],
                  ['b', 4], ['f', 4], ['b', 2], ['c', 4],
                  ['d', 3], ['a', 1], ['g', 3]]

fixed_game_a14 = [['c', 1], ['c', 4], ['g', 2], ['d', 4],
                  ['d', 1], ['f', 3], ['f', 4], ['f', 1],
                  ['g', 2], ['c', 2]]

fixed_game_a15 = [['d', 3], ['d', 4], ['a', 1], ['c', 2],
                 ['g', 3], ['d', 3], ['g', 1], ['a', 2],
                 ['a', 2], ['f', 4], ['a', 3], ['c', 2]]

# The following large data sets are each a typical game
# as generated by the "play_game" function.  (They are
# divided into five groups whose significance will be
# revealed in Part B of the assignment.)
fixed_game_b0_0 = [['d', 4], ['e', 1], ['f', 1], ['d', 1],
                   ['e', 2], ['c', 3], ['a', 2], ['e', 4],
                   ['g', 1], ['d', 4], ['a', 2], ['f', 2]]

fixed_game_b0_1 = [['f', 3], ['a', 2], ['d', 2], ['f', 4],
                   ['b', 2], ['a', 2], ['f', 3], ['f', 3],
                   ['e', 1], ['b', 2], ['e', 1], ['c', 1],
                   ['a', 3], ['d', 3], ['f', 1], ['f', 4],
                   ['b', 4], ['b', 1], ['c', 4], ['d', 1],
                   ['a', 3], ['e', 1], ['b', 2], ['c', 3],
                   ['d', 3], ['c', 2], ['c', 1], ['a', 2],
                   ['d', 4], ['b', 4], ['g', 2]]

fixed_game_b0_2 = [['d', 3], ['d', 4], ['a', 4], ['g', 3],
                   ['d', 2], ['g', 2], ['f', 1], ['b', 2],
                   ['a', 1], ['a', 3], ['a', 4], ['c', 3],
                   ['f', 3], ['b', 2], ['c', 3], ['a', 4],
                   ['g', 1]]

fixed_game_b1_0 = [['e', 3], ['a', 4], ['c', 2], ['f', 1],
                   ['a', 1], ['c', 4], ['g', 3], ['d', 1],
                   ['f', 3], ['d', 1], ['f', 1], ['g', 1],
                   ['e', 3], ['f', 3], ['f', 3], ['e', 4],
                   ['b', 2], ['a', 2], ['g', 1], ['d', 1],
                   ['a', 1], ['a', 1]]

fixed_game_b1_1 = [['f', 3], ['g', 1], ['g', 2], ['b', 1],
                   ['c', 2], ['c', 2], ['f', 3], ['g', 3],
                   ['b', 4], ['g', 4], ['d', 4], ['b', 1],
                   ['e', 3], ['e', 3], ['a', 2], ['c', 1],
                   ['f', 4], ['f', 3], ['e', 3], ['a', 2],
                   ['f', 4], ['g', 1], ['f', 4], ['a', 1]]

fixed_game_b1_2 = [['d', 2], ['f', 1], ['f', 1], ['c', 1],
                   ['c', 4], ['c', 4], ['d', 1], ['d', 4],
                   ['b', 2], ['d', 4], ['b', 1], ['d', 3],
                   ['d', 1], ['a', 1], ['f', 2], ['c', 2],
                   ['c', 4], ['c', 1], ['g', 1], ['g', 1],
                   ['g', 4], ['g', 2], ['a', 1], ['g', 1],
                   ['f', 2], ['e', 4], ['b', 1], ['e', 3],
                   ['b', 4], ['a', 4], ['b', 1], ['a', 4],
                   ['f', 2], ['g', 2], ['a', 1], ['f', 4],
                   ['e', 1], ['b', 4], ['a', 4], ['e', 2],
                   ['e', 3], ['e', 1]]

fixed_game_b2_0 = [['g', 2], ['d', 2], ['f', 2], ['f', 2],
                   ['b', 2], ['e', 1], ['d', 1], ['d', 3],
                   ['e', 1], ['e', 1], ['b', 1], ['b', 1],
                   ['d', 3], ['f', 3], ['d', 3]]

fixed_game_b2_1 = [['c', 2], ['g', 3], ['e', 4], ['g', 2],
                   ['a', 2], ['f', 2], ['f', 2], ['c', 1],
                   ['d', 2], ['b', 3], ['f', 2], ['d', 4],
                   ['b', 4], ['e', 2], ['g', 3], ['b', 4],
                   ['a', 1], ['g', 3], ['f', 1], ['e', 4],
                   ['d', 3], ['a', 1], ['a', 1], ['d', 2],
                   ['g', 3], ['d', 2], ['c', 4], ['f', 2],
                   ['g', 1], ['e', 4], ['f', 3], ['e', 3],
                   ['e', 3], ['b', 1], ['d', 2], ['c', 1],
                   ['c', 3]]

fixed_game_b2_2 = [['e', 2], ['b', 2], ['e', 2], ['g', 2],
                   ['f', 3], ['e', 3], ['e', 2], ['g', 2],
                   ['d', 2], ['e', 2], ['a', 1], ['c', 2],
                   ['e', 2], ['a', 3], ['f', 1], ['a', 3],
                   ['d', 2], ['g', 3], ['b', 4], ['b', 2],
                   ['f', 2], ['g', 4], ['d', 3], ['f', 1],
                   ['d', 3], ['a', 1], ['a', 4], ['g', 1],
                   ['f', 3], ['b', 3], ['c', 4], ['a', 3],
                   ['g', 2], ['c', 1], ['f', 3], ['b', 2],
                   ['b', 4], ['c', 3], ['d', 4], ['c', 4],
                   ['d', 1], ['c', 1]]

fixed_game_b3_0 = [['b', 2], ['d', 4], ['g', 2], ['e', 3],
                   ['d', 3], ['f', 4], ['g', 3], ['a', 3],
                   ['g', 2], ['d', 4], ['g', 4], ['f', 4],
                   ['a', 4], ['a', 4], ['f', 2], ['b', 1]]

fixed_game_b3_1 = [['d', 2], ['b', 2], ['e', 4], ['e', 3],
                   ['d', 3], ['c', 2], ['e', 3], ['b', 4],
                   ['b', 4], ['d', 4], ['f', 1], ['c', 2],
                   ['a', 1], ['e', 3], ['b', 4], ['f', 3],
                   ['c', 3], ['b', 3], ['c', 2], ['b', 2],
                   ['d', 3], ['e', 4], ['f', 2], ['g', 3],
                   ['g', 4], ['e', 2], ['c', 1], ['d', 3],
                   ['d', 1], ['f', 3], ['g', 3], ['f', 3],
                   ['c', 3], ['g', 4], ['g', 3], ['g', 3]]

fixed_game_b3_2 = [['a', 2], ['c', 1], ['f', 2], ['d', 2],
                   ['a', 3], ['c', 2], ['b', 3], ['e', 3],
                   ['e', 3], ['f', 4], ['a', 1], ['a', 2],
                   ['b', 1], ['c', 3], ['a', 2], ['c', 2],
                   ['g', 3], ['g', 3], ['d', 3], ['b', 2],
                   ['c', 4], ['g', 3], ['f', 3], ['a', 3],
                   ['f', 2], ['f', 1], ['d', 4], ['d', 4],
                   ['g', 2], ['e', 3], ['e', 4], ['f', 3],
                   ['d', 3], ['e', 4], ['g', 4], ['c', 3],
                   ['d', 1], ['e', 2], ['b', 2], ['b', 1],
                   ['g', 1]]

fixed_game_b4_0 = [['g', 3], ['f', 3], ['e', 4], ['a', 4],
                   ['a', 4], ['c', 4], ['e', 3], ['e', 4],
                   ['a', 4], ['a', 2], ['a', 2], ['c', 4],
                   ['f', 4], ['d', 4], ['c', 4], ['f', 3],
                   ['e', 1], ['b', 2], ['c', 2], ['a', 3],
                   ['g', 4], ['d', 3], ['f', 1], ['f', 2],
                   ['e', 2], ['d', 1], ['c', 4]]

fixed_game_b4_1 = [['a', 3], ['d', 4], ['g', 4], ['b', 3],
                   ['e', 1], ['b', 4], ['e', 3], ['f', 1],
                   ['f', 4], ['b', 4], ['d', 2], ['e', 4],
                   ['g', 4], ['d', 2], ['c', 3], ['b', 2],
                   ['f', 4], ['d', 2], ['b', 2], ['e', 4],
                   ['c', 3], ['d', 2], ['a', 1], ['e', 1],
                   ['d', 2], ['g', 1], ['g', 3]]

fixed_game_b4_2 = [['c', 1], ['c', 4], ['d', 1], ['c', 2],
                   ['d', 3], ['d', 4], ['g', 3], ['e', 1],
                   ['g', 4], ['c', 3], ['f', 1], ['b', 4],
                   ['a', 3], ['c', 4], ['e', 2], ['e', 3],
                   ['b', 3], ['d', 1], ['c', 3], ['f', 4],
                   ['e', 1], ['g', 4], ['b', 4], ['g', 3],
                   ['b', 4], ['b', 3], ['b', 3], ['g', 3],
                   ['e', 3], ['f', 1], ['e', 1], ['a', 1],
                   ['a', 4], ['a', 1], ['f', 4], ['f', 2],
                   ['f', 3], ['d', 1], ['d', 3], ['a', 3],
                   ['a', 1], ['g', 2]]

# If you want to create your own test data sets put them here,
# otherwise call function random_game to obtain data sets.
 
#
#--------------------------------------------------------------------#



#-----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to assess your solution.
# Do not change any of the code in this section.

# The following function creates a random data set describing a
# game to draw. Your program must work for any data set that
# can be returned by this function. The results returned by calling
# this function will be used as the argument to your "play_game"
# function during marking. For convenience during code development
# and marking this function also prints each move in the game to the
# shell window. NB: Your code should not print anything else to
# the shell. Make sure any debugging calls to the "print" function
# are disabled before you submit your solution.
#
# To maximise the amount of "randomness" the function makes no attempt
# to give each of the four "players" the same number of turns. (We
# assume some other random mechanism, such as rolling a die, determines
# who gets to drop a token into the board at each turn.) However the
# function has been designed so that it will never attempt to overfill
# a column of the board. Also, the function will not necessarily
# generate enough moves to fill every cell in the board.
#
def random_game():
    # Welcoming message
    print('Welcome to the game!')
    print('Here are the randomly-generated moves:')
    # Initialise the list of moves
    game = []
    # Keep track of free spaces
    vacant = [["I'm free!"] * num_rows] * num_columns
    # print(vacant)
    # Decide how many tokens to insert
    num_tokens = randint(0, num_rows * num_columns * 1.5)
    # Drop random tokens into the board, provided they won't
    # overfill a column
    for move in range(num_tokens):
        # Choose a random column and token type
        column_num = randint(0, num_columns - 1)
        column = chr(column_num + ord('a'))
        token = randint(1, 4)
        # Add the move, provided it won't overfill the board
        if vacant[column_num] != []:
            # Display the move
            print([column, token])
            # Remember it
            game.append([column, token])
            vacant[column_num] = vacant[column_num][1:]
    # Print a final message and return the completed game
    print('Game over!')
    if len(game) == 0:
        print('Zero moves were generated')
    elif len(game) == 1:
        print('Only one move was generated')
    else:
        print('There were', len(game), 'moves generated')
    return game

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#

## Setup Hammer Drawing Template
# A Hammer consist of a handle, cheek, claw, neck, bell, and face.
def draw_token_one(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)

    # 2. Set the token's bottom-left corner as the central drawing position.
    x_token_edge = int(xcor())
    y_token_edge = int(ycor())
    
    # 3. Create the token box.
    setheading(90) # Face north.
    pensize(2) # Set token outline thickness.
    pencolor("black") # Set default token and pen outline colour.
    pendown()
    begin_fill()
    fillcolor("dark sea green")
    for square in range(4):
        forward(cell_size)
        right(90)
    end_fill()
    penup()
    pensize(1) # Set default pen outline thickness.

##    # 4. Create the grid assistant.
##    # I would like to make it clear that no images were traced and all drawings
##    # were created by hand over various iterations.
##    # Along with separate reference images this grid was used to aid drawing.
##    # References to a 3*3 grid can be seen in the goto command for each shape.
##    # 4a. Define variables
##    grid_size = 3 # How many boxes to draw per row.
##    # 4b. Move to the relevant location.
##    goto(x_token_edge, y_token_edge)
##    setheading(0) # Face east.
##    pencolor("red")
##    pendown()
##    # 4c. Draw the grid.
##    for rows in range(grid_size):
##        # For every iteration move upwards.
##        goto(x_token_edge,\
##             y_token_edge + ((cell_size / grid_size) * rows))
##        pendown()
##        forward(cell_size)
##        penup()
##    setheading(270) # Face south.
##    for rows in range(grid_size):
##        # For every iteration move right.
##        goto(x_token_edge + ((cell_size / grid_size) * rows),\
##             y_token_edge + cell_size)
##        pendown()
##        forward(cell_size)
##        penup()
##    pencolor("black")
##    penup()

    # 5. Draw the wooden handle.
    # 5a. Define measurements.
    handle_width = 12 # Width of the handle in pixels, not mirrored.
    top_handle_length = 8 # Smooth surface length in pixels, mirrored.
    middle_handle_length = 18 # Smooth surface length in pixels, mirrored.
    bottom_handle_length = 6 # Smooth surface length in pixels, mirrored.
    upper_indent_length = 13 # Indent deepness in pixels, mirrored.
    upper_indent_angle = 8 # Indent sharpness in degrees, mirrored.
    lower_indent_length = 9 # Indent deepness in pixels, mirrored.
    lower_indent_angle = 7 # Indent sharpness in degrees, mirrored.
    #5b. Move to the shape's starting location.
    goto(x_token_edge + (cell_size // 3),\
         y_token_edge + 2.1 * (cell_size // 3))
    setheading(33) # Face north-east.
    pendown()
    fillcolor("peru")
    begin_fill()
    # 5c. Draw the handle width.
    forward(handle_width)
    right(90)
    # 5d. Draw the top handle, upper indent, and  middle handle for the right side.
    forward(top_handle_length)
    right(upper_indent_angle)
    forward(upper_indent_length)
    left(upper_indent_angle * 2)
    forward(upper_indent_length)
    right(upper_indent_angle)
    forward(middle_handle_length)
    # 5e. Draw the lower indent and bottom handle for the right side.
    right(lower_indent_angle)
    forward(lower_indent_length)
    left(lower_indent_angle * 2)
    forward(lower_indent_length)
    right(lower_indent_angle)
    forward(bottom_handle_length)
    # 5f. Loop around.
    circle((-handle_width / 2), 180)
    # 5g. Draw the lower indent and bottom handle for the left side.
    forward(lower_indent_length)
    right(lower_indent_angle)
    forward(lower_indent_length)
    left(lower_indent_angle * 2)
    forward(bottom_handle_length)
    right(lower_indent_angle)
    # 5h. Draw the top handle, upper indent, and middle handle for the left side.
    forward(middle_handle_length)
    right(upper_indent_angle)
    forward(upper_indent_length)
    left(upper_indent_angle * 2)
    forward(upper_indent_length)
    right(upper_indent_angle)
    forward(top_handle_length)
    end_fill()
    penup()

    # 6. Draw the neck and face.
    # 6a. Define measurements.
    cheek_offset = 3 # How many pixels the cheek should extend from the handle.
    face_length = 10 # Pixels, must stay at 10.
    neck_radius = 12 # Pixels, must stay at 12.
    bell_length = 7 # Pixels, must stay 7.
    # 6b. Move to the shape's starting location.
    goto(x_token_edge + (cell_size // 3),\
         y_token_edge + 2.1 * (cell_size // 3))
    # 6c. Draw the bottom side of the neck.
    pendown()
    setheading(180 + 33) # Face south-west.
    begin_fill()
    fillcolor("dim gray")
    forward(cheek_offset)
    right(90 - 20)
    circle(neck_radius, 90)
    # 6d. Draw the bell and face.
    forward(bell_length)
    right(90 + 20)
    forward(face_length)
    right(90)
    forward(bell_length)
    right(90)
    left(90 - 20)
    # 6e. Draw the top side of the neck.
    circle(neck_radius, 90)
    end_fill()
    penup()

    # 7. Draw the cheek and claw.
    # 7a. Define measurements.
    cheek_length = 12 # Pixels.
    claw_initial_height = 8 # Pixels.
    claw_radius = 4 # Pixels.
    claw_end_thickness = 2 # Pixels.
    # On the left side of the cheek there are three faces which form a trapezoid.
    # The total height of the cheek is approximately 24 pixels.
    cheek_t_b_face_length = 10 # Pixel length of the slanted top and bottom faces.
    cheek_m_face_length = 4 # Pixel length of the parallel middle face.
    # 7b. Move to the shape's starting location.
    goto(x_token_edge + (cell_size // 3),\
         y_token_edge + 2.1 * (cell_size // 3))
    setheading(180 + 33) # Face south-west.
    # 7c. Draw the bottom of the cheek.
    pendown()
    begin_fill()
    fillcolor("dim gray")
    forward(cheek_offset)
    right(180)
    forward(cheek_length + (cheek_offset * 2))
    # 7d. Draw the claw.
    left(90)
    forward(claw_initial_height)
    circle(-claw_radius, 140)
    forward(cheek_length)
    setheading(33) # Face north-west.
    forward(claw_end_thickness)
    left(90 + 20)
    forward(cheek_length + 2)
    circle((claw_radius * 3), (140 / 2))
    # 7e. Draw the top side of the cheek.
    setheading(180 + 33) # Face south-west.
    forward(cheek_length + (cheek_offset * 2))
    # 7f. Draw the trapezoid on the left side of the cheek.
    left(90 - 20)
    forward(cheek_t_b_face_length)
    left(90 - 70)
    forward(cheek_m_face_length)
    left(90 - 70)
    forward(cheek_t_b_face_length) 
    end_fill()
    penup()

## Setup Pliers Drawing Template
# Pliers consist of handles, exposed handles, fulcrum, jaws, cutters,
# and pipe grips.
def draw_token_two(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)

    # 2. Set the token's bottom-left corner as the central drawing position.
    x_token_edge = int(xcor())
    y_token_edge = int(ycor())
    
    # 3. Create the token box.
    setheading(90) # Face north.
    pensize(2) # Set token outline thickness.
    pencolor("black") # Set default token and pen outline colour.
    pendown()
    begin_fill()
    fillcolor("sky blue")
    for square in range(4):
        forward(cell_size)
        right(90)
    end_fill()
    penup()
    pensize(1) # Set default pen outline thickness.

    # 4. Draw the left and right handles.
    # 4a. Define measurements.
    handle_bottom_radius = 3 # Pixels.
    handle_radius = 32 # Pixels.
    handle_top_face_length = 8 # Pixels.
    # 4b. Move to the shape's starting location.
    goto(x_token_edge + (1.35 *(cell_size // 3)),\
         y_token_edge + (0.25 * (cell_size // 3)))
    # 4c. Draw the left handle.
    setheading(270 + 45) # Face south-east.
    pendown()
    fillcolor("gold")
    begin_fill()
    circle(-handle_bottom_radius, 180)
    circle(-handle_radius, 90)
    setheading(10) # Face north-east.
    forward(handle_top_face_length)
    setheading(180 + 43) # Face south-west.
    circle(handle_radius, 85)
    end_fill()
    penup()
    # 4d. Move to the shape's starting location.
    goto(x_token_edge + (1.7 *(cell_size // 3)),\
         y_token_edge + (0.25 * (cell_size // 3)))
    # 4e. Draw th right handle.
    setheading(270 - 45) # Face south-west.
    pendown()
    fillcolor("gold")
    begin_fill()
    circle(handle_bottom_radius, 180)
    circle(handle_radius, 90)
    setheading(180 - 10) # Face north-west.
    forward(handle_top_face_length)
    setheading(270 + 47) # Face south-east.
    circle(-handle_radius, 90)
    end_fill()
    penup()

    # 5. Draw the left and right exposed handles (extra parts above handles).
    # 5a. Define measurements.
    exposed_handle_radius = 6 # Best kept between 6 and 8 pixels.
    exposed_handle_length = 5 # Length of the top face, best kept at 5 pixels.
    exposed_handle_offset = 1 # How many pixels to move inwards.
    # 5b. Move to the shape's starting location.
    goto(x_token_edge + (1.35 *(cell_size // 3)),\
         y_token_edge + (0.25 * (cell_size // 3)))
    # 5c. Follow the previous path in 4c.
    setheading(270 + 45) # Face south-east.
    fillcolor("dim gray")
    circle(-handle_bottom_radius, 180)
    circle(-handle_radius, 90)
    setheading(10) # Face north-east.
    # 5d. Draw the left exposed handle.
    forward(exposed_handle_offset)
    setheading(90 - 45) # Face north-east.
    begin_fill()
    pendown()
    circle(exposed_handle_radius, 90)
    setheading(0) # Face east.
    forward(exposed_handle_length)
    right(90 - 40)
    circle(-exposed_handle_radius, 90)
    end_fill()
    penup()
    # 5e. Move to the shape's starting location.
    goto(x_token_edge + (1.7 *(cell_size // 3)),\
         y_token_edge + (0.25 * (cell_size // 3)))
    # 5f. Follow the previous path in 4e.
    setheading(270 - 45) # Face south-east.
    fillcolor("dim gray")
    circle(handle_bottom_radius, 180)
    circle(handle_radius, 180 - 90)
    setheading(180 - 10) # Face north-west.
    # 5g. Draw the right exposed handle.
    forward(exposed_handle_offset)
    setheading(90 + 45) # Face north.
    begin_fill()
    pendown()
    circle(-exposed_handle_radius, 90)
    setheading(180) # Face west.
    forward(exposed_handle_length)
    right(45)
    left(90)
    circle(exposed_handle_radius, 90)
    end_fill()
    penup()

    # 6. Draw the jaws.
    # 6a. Define measurements.
    fulcrum_outer_radius = 6 # Pixels.
    jaw_offset = 1 # How many pixels the jaw should extend from the fulcrum.
    jaw_length = 35 # Pixels.
    jaw_top_face_length = jaw_offset * 2 # Pixels.
    # 6b. Move to the shape's starting location.
    goto(x_token_edge + (1.35 *(cell_size // 3)),\
         y_token_edge + (1.85 * (cell_size // 3)))
    # 6c. Move to the centre of the fulcrum.
    pendown()
    setheading(90)
    right(90)
    forward(fulcrum_outer_radius)
    penup()
    # 6d. Draw the left jaw.
    pendown()
    fillcolor("silver")
    begin_fill()
    setheading(180 - 10) # Face north-west.
    forward(fulcrum_outer_radius + jaw_offset)
    right(90)
    forward(jaw_length)
    # 6e. Draw the flat top of the jaws.
    setheading(0) # Face east.
    forward(jaw_top_face_length)
    # 6f. Draw the right jaw.
    right(90 - 10)
    forward(jaw_length)
    right(90)
    forward(fulcrum_outer_radius + jaw_offset)
    end_fill()
    penup()

    # 7. Draw the cutters and pipe grips.
    # 7a. Define measurements.
    cutters_length = 7 # Pixels.
    pipe_grips_length = 24 # Pixels.
    # 7b. Move to the shape's starting location.
    goto(x_token_edge + (1.35 *(cell_size // 3)),\
         y_token_edge + (1.85 * (cell_size // 3)))
    # 7c. Move the top-middle point on the falcrum.
    setheading(270) # Face south.
    left(90)
    forward(fulcrum_outer_radius)
    left(90)
    forward(fulcrum_outer_radius)
    # 7d. Draw the cutters.
    pensize(3)
    pendown()
    forward(cutters_length)
    pensize(1)
    forward(pipe_grips_length)
    penup()

    # 8. Draw the fulcrum.
    # 8a. Define measurements.
    fulcrum_inner_radius = 3 # Pixels.
    fulcrum_circle_gap = 3 # Pixel gap between the outter and inner circles.
    # 8b. Move to the shape's starting location.
    goto(x_token_edge + (1.35 *(cell_size // 3)),\
         y_token_edge + (1.85 * (cell_size // 3)))
    # 8c. Draw the outer circle.
    setheading(90) # Face north.
    fillcolor("silver")
    begin_fill()
    pendown()
    circle(-fulcrum_outer_radius)
    end_fill()
    penup()
    # 8d. Draw the inner circle.
    right(90)
    forward(fulcrum_circle_gap)
    left(90)
    fillcolor("dark gray")
    begin_fill()
    pendown()
    circle(-fulcrum_inner_radius)
    penup()
    end_fill()

## Setup Screwdriver Drawing Template
# A screwdriver consists of a tip, shank, ferrule, and handle.
def draw_token_three(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)
    penup()

    # 2. Set the token's bottom-left corner as the central drawing position.
    x_token_edge = int(xcor())
    y_token_edge = int(ycor())
    
    # 3. Create the token box.
    setheading(90) # Face north.
    pensize(2) # Set token outline thickness.
    pencolor("black") # Set default token and pen outline colour.
    pendown()
    begin_fill()
    fillcolor("sandy brown")
    for square in range(4):
        forward(cell_size)
        right(90)
    end_fill()
    penup()
    pensize(1) # Set default pen outline thickness.

    # 4. Draw the tip.
    # 4a. Define measurements.
    tip_radius = 2 # Pixels, works best around 1 to 4.
    tip_length = 8 # Pixels.
    # 4b. Move to the shape's starting location.
    # In this drawing the length of each part is gradually added to the x-axis.
    # The 2 refers to a tiny margin.
    goto(x_token_edge + 2 + tip_radius,\
         y_token_edge + 50 + tip_radius)
    # 4c. Draw a rectangle with a curve on its left side.
    setheading(180) # Face west.
    pendown()
    fillcolor("black")
    begin_fill()
    circle(tip_radius, 180)
    forward(tip_length)
    left(90)
    forward(tip_radius * 2)
    left(90)
    forward(tip_length)
    end_fill()
    penup()
    
    # 5. Create the shank.
    # 5a. Define measurements.
    shank_length = 32 # Pixels.
    # 5b. Move to the shape's starting location.
    goto((x_token_edge + 2 + tip_radius + tip_length),\
         (y_token_edge + 50 + tip_radius))
    # 5c. Draw a rectangle.
    setheading(270) # Face south.
    pendown()
    fillcolor("dark grey")
    begin_fill()
    for rectangle in range(2):
        forward(tip_radius * 2)
        left(90)
        forward(shank_length)
        left(90)
    end_fill()
    penup()

    # 6. Draw the ferrule.
    # 6a. Define measurements.
    ferrule_length = 3 # Pixels.
    ferrule_offset = 1 # How many pixels the ferrule should extend from the shank.
    # 6b. Move to the shape's starting location.
    goto((x_token_edge + 2 + tip_radius + tip_length + shank_length),\
         (y_token_edge + 50 + tip_radius + (ferrule_offset * 2)))
    # 6c. Draw a rectangle.
    setheading(270) # Face south.
    pendown()
    fillcolor("dodger blue")
    begin_fill()
    for rectangle in range(2):
        forward((ferrule_offset * 4) + (tip_radius * 2))
        left(90)
        forward(ferrule_length)
        left(90)
    end_fill()
    penup()

    # 7. Draw the front handle.
    # 7a. Define measurements.
    front_handle_offset = 2 # How many pixels the front handle should extend from the ferrule.
    front_handle_indent_radius = tip_radius * 4 # The deepness of the indent.
    # 7b. Move to the shape's starting location.
    goto(x_token_edge + 2 + tip_radius + tip_length + shank_length + ferrule_length,\
         (y_token_edge + 50 + tip_radius + (front_handle_offset * 2)))
    # The shape is a rectangle with a slim center.
    # 7c. To the left of the indent draw the flat left and bottom faces.
    setheading(270) # Face south.
    pendown()
    fillcolor("dodger blue")
    begin_fill()
    forward((front_handle_indent_radius) + (front_handle_indent_radius / 2))
    left(90)
    forward(ferrule_length * 2)
    # 7d. Draw the bottom indent.
    setheading(90) # Face north.
    circle(-tip_radius * 1.75, 180)
    left(90)
    forward(ferrule_length)
    # 7e. To the right of the indent draw the flat bottom, right, and top faces.
    left(90)
    forward((front_handle_offset * 4) + (tip_radius * 2))
    left(90)
    forward(ferrule_length)
    # 7f. Draw the top indent.
    setheading(270) # Face south.
    circle(-tip_radius * 1.75, 180)
    # 7g. To the left of the indent draw the flat top face.
    left(90)
    forward(ferrule_length * 2)
    end_fill()
    penup()
    
    # 8. Draw the back handle
    # 8a. Define measurements.
    back_handle_length = 25 # Pixels.
    back_handle_offset = 3 # How many pixels the back handle should extend from the front handle.
    # 8b. Move to the shape's starting location.
    goto(x_token_edge + 2 + tip_radius + tip_length + shank_length + ferrule_length + 16,\
         (y_token_edge + 50 + tip_radius + (back_handle_offset * 2)))
    # 8c. Draw a rectangle with a curve on its right side.
    setheading(270) # Face south.
    pendown()
    fillcolor("dodger blue")
    begin_fill()
    forward((back_handle_offset * 4) + (tip_radius * 2))
    left(90)
    forward(back_handle_length)
    circle(((back_handle_offset * 2) + (tip_radius * 2) / 2), 180)
    forward(back_handle_length)
    end_fill()
    penup()

    # 9. Draw handle grip lines.
    # 9a. Define measurements.
    grip_line_length = 24
    # 9b. Set the initial direction, pensize, and pencolor.
    setheading(0) # Face east.
    pensize(2)
    pencolor("blue")
    for row in range(3):
        # 9c. Move to the line's starting location.
        goto(x_token_edge + 2 + tip_radius + tip_length + shank_length + ferrule_length + 16 + 3,\
             (y_token_edge + 50 + tip_radius + (back_handle_offset * 2) - 4 - (4 * row)))
        # 9d. Draw the line.
        pendown()
        forward(grip_line_length)
        penup()

## Setup Wrench Drawing Template
# A wrench consists of a handle, handle hole, handle indent, worm barrel pin,
# worm screw, adjustable jaw, and fixed jaw.
def draw_token_four(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)

    # 2. Set the token's bottom-left corner as the central drawing position.
    x_token_edge = int(xcor())
    y_token_edge = int(ycor())
    
    # 3. Create the token box.
    setheading(90) # Face north.
    pensize(2) # Set token outline thickness.
    pencolor("black") # Set default token and pen outline colour.
    pendown()
    begin_fill()
    fillcolor("indian red")
    for square in range(4):
        forward(cell_size)
        right(90)
    end_fill()
    penup()
    pensize(1) # Set default pen outline thickness.

    # 4. Draw the adjustable jaw and worm barrel pin.
    # 4a. Define measurements.
    indent_gap = 1 # Horizontal face length and gap between zigzags in pixels.
    indent_length = 4 # Vertical length of zigzags in pixels.
    protrusion_end_length = 3 # Pixels.
    protrusion_exit_length = 10 # Move to a level position in pixels.
    raise_jaws = 6 # Raise both jaws from a level position in pixels.
    adjustable_jaw_radius = 9 # Pixels.
    adjustable_jaw_length = 20 # Pixels.
    left_handle_length = 55 # Pixels.
    left_handle_bottom_radius = 10 # Pixels.
    upper_left_handle_radius = 18 # Pixels.
    # 4b. Move to the shape's starting location.
    goto(x_token_edge + (0.9 *(cell_size // 3)),\
         y_token_edge + (0.2 * (cell_size // 3)))
    # 4c. Follow the future path used in 5c and 5d for consistency.
    setheading(270 - 33) # Face south-west.
    circle(-left_handle_bottom_radius, 180)
    right(6)
    forward(left_handle_length)
    circle(upper_left_handle_radius, 55)
    setheading(180 - 33) # Face west.
    pendown()
    begin_fill()
    fillcolor("silver")
    # 4d. Draw the protrusion.
    for RightAngleZigzag in range(2):
        forward(indent_gap)
        left(90)
        forward(indent_length)
        right(90)
        forward(indent_length)
        right(90)
        forward(indent_gap)
        left(90)
        forward(indent_gap)
    right(90)
    forward(protrusion_end_length) 
    right(35)
    forward(protrusion_exit_length)
    # 4e. Draw the adjustable jaw.
    setheading(80) # Face north-east.
    forward(raise_jaws)
    circle(-adjustable_jaw_radius, 90)
    right(90)
    forward(adjustable_jaw_length)
    end_fill()
    penup()

    # 5. Draw the handle and fixed jaw.
    # 5a. Define measurements.
    right_handle_length = 70 # Pixels.
    fixed_jaw_length = 16 # Pixels.
    fixed_jaw_transition_radius = 6 # The pixel radius between the jaw length and height.
    fixed_jaw_radius = 14 # Pixels.
    # 5b. Move to the shape's starting location.
    goto(x_token_edge + (0.9 *(cell_size // 3)),\
         y_token_edge + (0.2 * (cell_size // 3)))
    # 5c. Draw the left side of the handle
    setheading(270 - 33) # Face south-west.
    pendown()
    begin_fill()
    fillcolor("silver")
    circle(-left_handle_bottom_radius, 180)
    right(5)
    forward(left_handle_length)
    # 5d. Draw the fixed jaw.
    circle(upper_left_handle_radius, 90)
    setheading(350) # Face south-east.
    forward(fixed_jaw_length)
    left(10)
    circle(fixed_jaw_transition_radius, 90)
    forward(raise_jaws)
    right(90)
    circle(-fixed_jaw_radius, 160)
    forward(8)
    setheading(270 - 33 + 3) # Face south-west.
    # 5e. Draw the right side of the handle.
    forward(right_handle_length)
    end_fill()
    penup()

    # 6. Draw the handle hole, handle indent, and worm screw.
    # 6a. Define measurements.
    handle_hole_radius = 6 # Pixels.
    handle_indent_gap = 7 # Pixels between the handle hole and indent.
    handle_indent_length = 50 # Pixels.
    handle_indent_top_radius = 2 # Pixels.
    hamdle_indent_bottom_radius = 5 # Pixels.
    rectangle_length = 7 # Pixels.
    rectangle_height = 9 # Pixels.
    screw_height_offset = 2 # Pixels.
    # 6b. Move to the shape's starting location.
    goto(x_token_edge + (0.9 *(cell_size // 3) -2.5),\
         y_token_edge + (0.2 * (cell_size // 3) +2.5))
    # 6c. Draw a circular hole and fill it with the token's background colour.
    setheading(270 - 33) # Face south-west.
    pendown()
    begin_fill()
    fillcolor("indian red")
    circle(-handle_hole_radius)
    end_fill()
    penup()
    # 6d. Get in position for the handle indent.
    circle(-handle_hole_radius, 180)
    # 6e. Draw the handle indent.
    setheading(270 - 33 - 180 - 4) # Face north-east.
    fillcolor("dark gray")
    begin_fill()
    forward(handle_indent_gap)
    pendown()
    forward(handle_indent_length)
    circle(-handle_indent_top_radius, 180 - 7)
    forward(handle_indent_length)
    right(180)
    circle(hamdle_indent_bottom_radius, 180 - 7)
    end_fill()
    penup()
    # 6f. Get in position for the worm screw.
    right(180)
    forward(handle_indent_length + handle_indent_gap)
    left(90)
    forward(handle_indent_gap // 2)
    # 6g. Draw a rectangular hole and fill it with the token's background colour.
    setheading(80) # Face north-east.
    pendown()
    fillcolor("indian red")
    begin_fill()
    for rectangle in range(2):
        forward(rectangle_height)
        right(90)
        forward(rectangle_length)
        right(90)
    end_fill()
    # 6h. Draw the worm screw.
    forward(rectangle_height - screw_height_offset)
    right(90)
    fillcolor("dark grey")
    begin_fill()
    for rectangle in range(2):
        forward(rectangle_length)
        right(90)
        forward(rectangle_height - screw_height_offset * 2)
        right(90)
    end_fill()
    penup()

## Setup Text Writing Template
def draw_text(x_coordinate, y_coordinate, string, size, weight):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)
    # 2. Write text on the screen.
    pencolor("black")
    write(str(string), move = False, align = "center", font = ("Arial", size, weight))

## Setup Gold Star Drawing Template
# Winning tokens will be presented this badge.
def draw_gold_star(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)
    # 2. Define measurements.
    face_angle = 130 # Degrees.
    star_points = 5
    face_length = 20 # The pixel length of the left and right sides of a point.
    # 3. Draw multiple points.
    setheading(0) # Face east.
    pendown()
    pensize(2)
    pencolor("dark goldenrod")
    fillcolor("gold")
    begin_fill()
    for point in range(star_points):
        forward(face_length)
        right(face_angle)
        forward(face_length)
        right((360 / star_points) - face_angle)
    end_fill()
    penup()

## Setup Silver Star Drawing Template
# Tied tokens will be presented this badge.
def draw_silver_star(x_coordinate, y_coordinate):
    # 1. Move to the relevant location.
    goto(x_coordinate, y_coordinate)
    # 2. Define measurements.
    face_angle = 130 # Degrees.
    star_points = 5
    face_length = 20 # Pixels.
    # 3. Draw multiple points.
    setheading(0) # Face east.
    pendown()
    pensize(2)
    pencolor("dim gray")
    fillcolor("gainsboro")
    begin_fill()
    for point in range(star_points):
        forward(face_length)
        right(face_angle)
        forward(face_length)
        right((360 / star_points) - face_angle)
    end_fill()
    penup()

## Setup Game Function To Analyse Moves And Declare A Victory.
def play_game(gamemode):
    # 1. Determine if the results of each move should be printed.
    output_results = False

    # 2. Initialize variables.
    # 2a. Setup a variable to declare if the game has been won.
    winner = False
    # 2b. Setup a variable to count each move.
    move_count = 0
    # 2c. Setup lists to remember homw many tokens are placed in each column.
    a_column_tokens = [] # Referred to as column 0.
    b_column_tokens = [] # Referred to as column 1.
    c_column_tokens = [] # Referred to as column 2.
    d_column_tokens = [] # Referred to as column 3.
    e_column_tokens = [] # Referred to as column 4.
    f_column_tokens = [] # Referred to as column 5.
    g_column_tokens = [] # Referred to as column 6.
    # 2d. Setup a list to remember the highest tokens from every column.
    highest_tokens = []
    # 2e. Setup a counter to remember how many tokens are atop each column.
    token_one_atop_count = 0
    token_two_atop_count = 0
    token_three_atop_count = 0
    token_four_atop_count = 0
    # 2f. Set the central drawing position as the bottom-left corner of the grid.
    x_grid_edge = ((num_columns * cell_size) // 2)
    y_grid_edge = (((num_columns - 1) * cell_size) // 2)

    # 3. Display and label replica tokens at the left and right side of the grid.
    # 3a. Display and label token one at the top-left corner of the screen.
    draw_token_one((-x_grid_edge - (cell_size * 2)),\
                   (-y_grid_edge + (cell_size * 3.75)))
    draw_text((-x_grid_edge - (cell_size * 1.5)),\
              (-y_grid_edge + (cell_size * 3.45)), "Token 1", 14, "bold")
    draw_text((-x_grid_edge - (cell_size * 1.5)),\
              (-y_grid_edge + (cell_size * 3.2)), "Hammer", 14, "normal")
    # 3b. Display and label token two at the top-right corner of the screen.
    draw_token_two((-x_grid_edge + (cell_size * 8)),\
                   (-y_grid_edge + (cell_size * 3.75)))
    draw_text((-x_grid_edge + (cell_size * 8.5)),\
              (-y_grid_edge + (cell_size * 3.45)), "Token 2", 14, "bold")
    draw_text((-x_grid_edge + (cell_size * 8.5)),\
              (-y_grid_edge + (cell_size * 3.2)), "Pliers", 14, "normal")
    # 3c. Display and label token three at the bottom-left corner of the screen.
    draw_token_three((-x_grid_edge - (cell_size * 2)),\
                     (-y_grid_edge + (cell_size * 1.25)))
    draw_text((-x_grid_edge - (cell_size * 1.5)),\
              (-y_grid_edge + (cell_size * 0.95)), "Token 3", 14, "bold")
    draw_text((-x_grid_edge - (cell_size * 1.5)),\
              (-y_grid_edge + (cell_size * 0.7)), "Screwdriver", 14, "normal")
    # 3d. Display and label token four at the bottom-right corner of the screen.
    draw_token_four((-x_grid_edge + (cell_size * 8)),\
                    (-y_grid_edge + (cell_size * 1.25)))
    draw_text((-x_grid_edge + (cell_size * 8.5)),\
              (-y_grid_edge + (cell_size * 0.95)), "Token 4", 14, "bold")
    draw_text((-x_grid_edge + (cell_size * 8.5)),\
              (-y_grid_edge + (cell_size * 0.7)), "Wrench", 14, "normal")

    # 4. Extract the letters and tokens of each move.
    for column, token in gamemode:
        # 4a. Convert each column letter into an integer, increment move counter.
        # subtract 97 to make the letters start at 0 (aligned to the y-axis).
        column = ord(column) - 97
        move_count += 1
        
        # 5. Calculate the x and y coordinates.
        # 5a. Generate the x coordinate.
        if column >= 0 and column <= 6:
            x_position = -x_grid_edge + (cell_size * column)
        else:
            print("Error: cannot set the x coordinate!")
            break
        # 5b. Generate the y coordinate.
        # For every existing token in a column move the new token upwards.
        if column == 0:
            y_position = -y_grid_edge + (cell_size * len(a_column_tokens))
        elif column == 1:
            y_position = -y_grid_edge + (cell_size * len(b_column_tokens))
        elif column == 2:
            y_position = -y_grid_edge + (cell_size * len(c_column_tokens))
        elif column == 3:
            y_position = -y_grid_edge + (cell_size * len(d_column_tokens))
        elif column == 4:
            y_position = -y_grid_edge + (cell_size * len(e_column_tokens))
        elif column == 5:
            y_position = -y_grid_edge + (cell_size * len(f_column_tokens))
        elif column == 6:
            y_position = -y_grid_edge + (cell_size * len(g_column_tokens))
        else:
            print("Error: cannot set the y coordinate!")
            break
        
        # 6. Check which token to draw and travel to the assigned coordinates.
        if token == 1:
            draw_token_one(x_position, y_position)
        elif token == 2:
            draw_token_two(x_position, y_position)
        elif token == 3:
            draw_token_three(x_position, y_position)
        elif token == 4:
            draw_token_four(x_position, y_position)
        else:
            print("Error: cannot draw the token!")
            break

        # 7. Record each token placed inside a column.
        if column == 0:
            a_column_tokens.append(token) # Add the token to the column list.
        elif column == 1:
            b_column_tokens.append(token)
        elif column == 2:
            c_column_tokens.append(token)
        elif column == 3:
            d_column_tokens.append(token)
        elif column == 4:
            e_column_tokens.append(token)
        elif column == 5:
            f_column_tokens.append(token)
        elif column == 6:
            g_column_tokens.append(token)
        else:
            print("Error: cannot reference the column count!")
            break

        # 8. Add the highest (last) tokens from each column to a single list.
        if a_column_tokens != []: # Check if the column is not empty.
            highest_tokens.append(a_column_tokens[-1]) # Add last item to a list.
        if b_column_tokens != []:
            highest_tokens.append(b_column_tokens[-1])
        if c_column_tokens != []:
            highest_tokens.append(c_column_tokens[-1])
        if d_column_tokens != []:
            highest_tokens.append(d_column_tokens[-1])
        if e_column_tokens != []:
            highest_tokens.append(e_column_tokens[-1])
        if f_column_tokens != []:
            highest_tokens.append(f_column_tokens[-1])
        if g_column_tokens != []:
            highest_tokens.append(g_column_tokens[-1])

        # 9. Count how many times each token is atop a column.
        for token in highest_tokens:
            if token == 1:
                token_one_atop_count += 1
            elif token == 2:
                token_two_atop_count += 1
            elif token == 3:
                token_three_atop_count += 1
            elif token == 4:
                token_four_atop_count += 1
            else:
                print("Error: cannot extract the highest tokens!")

        # 10. Output the results for each move.
        if output_results == True:
            print("Move:", move_count)
            print("Column:", column)
            print("Token:", token)
            print("x position:", x_position)
            print("y positon:", y_position)
            print("First token atop:", token_one_atop_count)
            print("Second token atop:", token_two_atop_count)
            print("Third token atop:", token_three_atop_count)
            print("Fourth token atop:", token_four_atop_count)
            print("") # Skip a line.
                
        # 11. Check if a player has won the game.
        # The objective of the game is to have 4 tokens atop of columns.
        if token_one_atop_count > 3:
            # Draw a gold star in the top-left corner of the screen.
            draw_gold_star((-x_grid_edge - (cell_size * 1)),\
                (-y_grid_edge + (cell_size * 4.75)))
            winner = True
            break
        if token_two_atop_count > 3:
            # Draw a gold star in the top-right corner of the screen.
            draw_gold_star((-x_grid_edge + (cell_size * 9)),\
                (-y_grid_edge + (cell_size * 4.75)))
            winner = True
            break
        if token_three_atop_count > 3:
            # Draw a gold star in the bottom-left corner of the screen.
            draw_gold_star((-x_grid_edge - (cell_size * 1)),\
                (-y_grid_edge + (cell_size * 2.25)))
            winner = True
            break
        if token_four_atop_count > 3:
            # Draw a gold star in the bottom-right corner of the screen.
            draw_gold_star((-x_grid_edge + (cell_size * 9)),\
                (-y_grid_edge + (cell_size * 2.25)))
            winner = True
            break

        # 12. Reset the highest token count and list to stop numbers from stacking.
        token_one_atop_count = 0
        token_two_atop_count = 0
        token_three_atop_count = 0
        token_four_atop_count = 0
        highest_tokens = []

    # 13. If nobody has won award silver stars to all players.
    if winner == False:
        # 13a. Display a silver star at the top-left corner of the screen.
        draw_silver_star((-x_grid_edge - (cell_size * 1)),\
            (-y_grid_edge + (cell_size * 4.75)))
        # 13b. Display a silver star at the top-right corner of the screen.
        draw_silver_star((-x_grid_edge + (cell_size * 9)),\
            (-y_grid_edge + (cell_size * 4.75)))
        # 13c. Display a silver star at the bottom-left corner of the screen.
        draw_silver_star((-x_grid_edge - (cell_size * 1)),\
            (-y_grid_edge + (cell_size * 2.25)))
        # 13d. Display a silver star at the bottom-right corner of the screen.
        draw_silver_star((-x_grid_edge + (cell_size * 9)),\
            (-y_grid_edge + (cell_size * 2.25)))
        
#
#--------------------------------------------------------------------#



#-----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing your solution.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#

# Set up the drawing canvas
# ***** You can change the background and line colours, and choose
# ***** whether or not to label the axes and mark the places for the
# ***** legend, by providing arguments to this function call
create_drawing_canvas()

# Control the drawing speed
# ***** Change the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** forever while the cursor moves slowly around the screen
tracer(False)

# Give the drawing canvas a title
# ***** Replace this title with a description of your solution's
# ***** theme and its tokens
title('The chosen theme was hand tools, featuring a hammer, pliers, screwdriver, and wrench.')

### Call the student's function to play the game
### ***** While developing your program you can call the "play_game"
### ***** function with one of the "fixed" data sets, but your
### ***** final solution must work with "random_game()" as the
### ***** argument.  Your "play_game" function must work for any data
### ***** set that can be returned by the "random_game" function.
##play_game(fixed_game_b4_2) # <-- use this for code development only
play_game(random_game()) # <-- this will be used for assessment

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()

#
#--------------------------------------------------------------------#
