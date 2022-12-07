import pygame
import random
 
# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
class Piece:
    """
    Each piece object are each block in the game
    """

    def __init__(self, column, row, shape):
        """
        initializer to generate each piece class.
        ### (Hopefully add more details on parameters later) ###
        """
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
 
def create_grid(locked_positions={}):
    """
    Parameters
    ----------
    locked_positions : Dictionary
        - keeping track of pieces in the game using a grid data structure. 
        - create a multidimensional list that contains lists of elements in each list
        - uses a dictionary of key value pairs where:
            - each key is a position of the piece
            - each value: color of the piece

    Return
    -------
    grid : (dictionary)
        - grid would be of a dicitionary type data
    """
    grid = [[(0,0,0) for x in range(10)]for y in range(20)] # make (0,0,0)(color) to every row and col
    for i in range(len(grid)):                                # row loop
        for j in range(len(grid[i])):                            # col lo
            if(j, i) in locked_positions:
                grid[i][j] = locked_positions[(j,i)]        #?

    return grid
 
def convert_shape_format(shape):
    """
    Parameters
    ----------
    shape : (type)
        - given a shape format, need to convert and return a list of positions
        - input: shape  

    Return
    -------
    positions : (list)
        - list type of (x,y) position of the given shape in the parameter
    """
    pos = []
    form = shape.shape[shape.rotation % len(shape.shape)]

    for i, each_line in enumerate(form):
        row = list(each_line)
        for j, each_col in enumerate(row):
            if each_col == '0':
                pos.append((shape.x + j, shape.y + i))

    for i, positions in enumerate(pos):
        pos[i] = (positions[0] - 2, positions[1] - 4)

    return pos
 
def valid_space(shape, grid):
    """
    - checking to see if position to move from the current position of the shape selected is valid
    - check if the shape nearby has colors.
    - if color is black, good to move into
    - otherwise, that space is not valid to move

    Parameters
    ----------
    shape : (piece)
        - 
    grid : (list)
        - x,y position of the shape

    Return
    -------
    (True/False) : (boolean)
        - return True if valid position to move into
        - return False otherwise
    """
    accepted_range = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_range = [j for sub in accepted_range for j in sub]
    
    formatted_shape = convert_shape_format(shape)
    
    for each_pos in formatted_shape:
        if each_pos not in accepted_range:
            if each_pos[1] > -1:
                return False
    return True
 
def check_lost(positions):
    """
    Parameters
    ----------
    positions : (list)
        - checks if user lost the game based on the position of the shape in the grid
        - if position reached top, game lost

    Return
    -------
    (True or False) : (boolean)
        - checking for the y part of the position of the shape
        - return True if game lost
        - return False if game won 
    """
    for each_pos in positions:
        x, y = each_pos
        if y < 1:
            return True

    return False
 
def get_shape():
    """
    Generate a random shape for new dropping block.

    Parameters
    ----------
    none : 
        - based on shapes and shape_colors, generate a random shape

    Return
    -------
     : Piece-class object.shape
        - return the following of the piece-class object:
            - column (int-type)
            - row (int-type)
            - shape (a random selection of shape)
    """
    global shapes, shape_colors
    return Piece(5,0,random.choice(shapes))
 
def draw_text_middle(text, size, color, surface):
    """
    - helps display text to middle of the screen
    - useful for creating UIs:
        - Main Menu
        - end screen

    Parameters
    ----------
    text : (type)
        - the text to display in the middle
    
    size : (type)
        - size of text to display
    
    color : (type)
        - color of the given text in the parameter to set

    surface : (type)
        - which text to fill colors into

    Return
    -------
    (name) : (none)
        - outputs a text to display in the middle of the screen
    """
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
    """
    Draw a new shape of block on the screen.
    - update the display
    - make two for loops for row and col to draw a line(pygame.draw_line())
    
    font: \'comicsans\', 60
    label: \'TETRIS\', 1, (255,255,255)
    
    Parameters
    ----------
    surface : (display)
        - display where we will update the gride
    
    grid : list[list[]]
        - grid
    
    Return
    -------
    None
    """
    start_x = top_left_x
    start_y = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (start_x, start_y + i*block_size), (start_x + play_width, start_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (start_x + j * block_size, start_y), (start_x + j * block_size, start_y + play_height))
    
 
def clear_rows(grid, locked):
    """
    Clear the row if the row is filled with blocks and shift it down.
    Updates the locked.

    Parameters
    ----------
    grid : grids in the block
        - check every grid (0,0,0) is in the row of each grid
    
    locked : Dictionary
        - keeping track of pieces in the game using a grid data structure. 
        - create a multidimensional list that contains lists of elements in each list
        - uses a dictionary of key value pairs where:
            - each key is a position of the piece
            - each value: color of the piece
        - delete the specific rows that we check in the locked
        - update the new locked.

    Return
    -------
    inc : int
        - number of rows completed and deleted
    """
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid [i]
        if (0,0,0) not in row :
            inc += 1
            ind = i
            for j in range (len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)
    return inc

 
def draw_next_shape(shape, surface):
    """
    Draw the next block's shape on the right side of the screen.

    Parameters
    ----------
    shape : (piece of class)
        - column (int-type)
        - row (int-type)
        - shape (a random selection of shape)

    surface : (display)
        - display where we will update the gride

    Return
    -------
    Nothing:
        - update the display
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    x_start = top_left_x + play_width + 50
    y_start = top_left_y + play_height/2 - 200
    form = shape.shape[shape.rotation % len(shape.shape)]

    for i, each_line in enumerate(form):
        row = list(each_line)
        for j, each_col in enumerate(row):
            if each_col == '0':
                pygame.draw.rect(surface, shape.color, (x_start + j * 30, y_start + i * 30, 30, 30), 0)
                
    surface.blit(label, (x_start + 10, y_start - 30))
 
def draw_window(surface, grid, score=0, last_score = 0):
    """
    Parameters
    ----------
    surface : (display)
        - display where we will update the gride
    
    Return
    -------
    None
    """
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    
    # current game score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))
    
    x_start = top_left_x + play_width + 50
    y_start = top_left_y + 200

    surface.blit(label, (x_start + 20, y_start + 160))

    # last score 
    label = font.render('High Score: ' + last_score, 1, (255,255,255))
    
    x_start = top_left_x - 250
    y_start = top_left_y + 200

    surface.blit(label, (x_start + 20, y_start + 160))
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size))
    
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)

def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score

def get_next_piece(curr_piece):
    """
    Generate next piece and return. Next piece should be different piece.

    Parameters
    ----------
    curr_piece : Piece
        - current piece
    
    Return
    -------
    next_piece : Piece
        - next piece
    """
    next_piece = get_shape()
    while next_piece.shape == curr_piece.shape:
        next_piece = get_shape()
    return next_piece

def paused(surface, pause):
    """
    https://pythonprogramming.net/pause-game-pygame/
    """
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
 
def main(win):
    last_score = max_score()                    #max_score function  필요할것같아요. # DONE
    locked_positions ={}
    grid = create_grid(locked_positions)

    change_piece =False
    run =True
    current_piece = get_shape()
    next_piece = get_next_piece(current_piece)
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -+ 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid))and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -=1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y -= 1
                    current_piece.y += 1
                    if not(valid_space(current_piece,grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_p:
                    pause = True
                    paused(win, pause)
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y>-1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_next_piece(current_piece)
            change_piece = False
            score += 2**(clear_rows(grid, locked_positions)) * 5
            # no row: 5, 1 row: 10, 2 row: 20, 3 row: 40, 4 row: 80, ...
        
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("GAME OVER!", 80, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run =False
            update_score(score) #  need to create update_score function

    pass
 
def main_menu(win):
    run =True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press Any Key To Play', 60, (255,255,255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()
    quit()