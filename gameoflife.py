#!/usr/bin/python3

# gameoflife.py
# Implementation of Conway's Game of Life

# By Ernold McPuvlist
# 2021

try:
    from sys import exit
    import configparser
    import pygame
except ImportError as err:
    print("Module not found: ", err)
    exit()

# ====================================================
# Define classes
# ====================================================

class CellArray:
    """Class to store an array of Game of Life cells"""
    
    # class variables, fixed values for all instances
    grid_width = grid_height = 63
    cell_size = 6

    def __init__(self):
        # The _internal_array variable stores the grid of cells
        # as a list of lists (columns x rows).
        # Initialise with all cells set to False

        self._internal_array = [[False for row in range(CellArray.grid_height)] for col in range(CellArray.grid_width)]
        
    def get_cell(self, col_row): # col_row is a (col,row) tuple
        return (self._internal_array[col_row[0]][col_row[1]])

    def set_cell(self, col_row):
        self._internal_array[col_row[0]][col_row[1]] = True

    def unset_cell(self, col_row):
        self._internal_array[col_row[0]][col_row[1]] = False

    def get_all_live_cells(self):
        """Generate a list of all live cells (col,row tuples)"""
        for row in range(CellArray.grid_height):
            for col in range(CellArray.grid_width):
                if self._internal_array[col][row]:
                    yield (col, row)

    def get_neighbours(self, col_row):
        """Return a list of coordinates (as tuples) of the cells
        that surround this one, allowing for screen wraparound."""

        # unpack local variables for column and row from the tuple
        col, row  = col_row

        # Determine what row is above
        row_above = row - 1 if row > 0 else CellArray.grid_height - 1

        # Determine what row is below
        row_below = row + 1 if row < CellArray.grid_height - 1 else 0

        # Determine what column is to the left
        col_toleft = col - 1 if col > 0 else CellArray.grid_width - 1

        # Determine what column is to the right
        col_toright = col + 1 if col < CellArray.grid_width - 1 else 0

        return [(col_toleft, row_above), (col, row_above), (col_toright, row_above), \
               (col_toleft, row), (col_toright, row), \
               (col_toleft, row_below), (col, row_below), (col_toright, row_below)]

    def count_live_neighbours(self, col_row):
        """Count how many of the neighbouring cells are live"""
        return list(map(self.get_cell, self.get_neighbours(col_row))).count(True)

    def draw(self):
        """Draw the grid on the screen"""
        global WIN, FG_COLOUR, BG_COLOUR
        row_pos = col_pos = 0 # initialise local row and column positions

        # draw row by row
        for row in range(CellArray.grid_height):
            for col in range(CellArray.grid_width):
                if self._internal_array[col][row]:
                    pygame.draw.rect(WIN,FG_COLOUR,(col_pos,row_pos,CellArray.cell_size,CellArray.cell_size))
                else:
                    pygame.draw.rect(WIN,BG_COLOUR,(col_pos,row_pos,CellArray.cell_size,CellArray.cell_size))
                col_pos += CellArray.cell_size
            col_pos = 0
            row_pos += CellArray.cell_size

        pygame.display.update()

    def clear(self):
        """Make all cells dead (False)"""

        for column in range(CellArray.grid_width):
            for row in range(CellArray.grid_height):
                self._internal_array[column][row] = False
        
    def save_data(self):
        """Save the game state to the config file"""
        global CFG

        # Build a string of cell coordinates of all live cells
        # separated by a pipe character, e.g. 0,0|2,3
        cell_save = '|'.join(map(lambda s:str(s[0]) + "," + str(s[1]), self.get_all_live_cells()))

        if len(cell_save) > 0:

            if not CFG.has_section('pattern'):
                CFG.add_section('pattern')

            CFG['pattern']['cells'] = cell_save

            # write config file to disk
            with open(CFG_FILENAME, 'w') as cfg_file:
                CFG.write(cfg_file)

    def load_save_data(self, save_data):
        """Load saved data back into the grid"""

        self.clear()

        for saved_cell in save_data:
            self.set_cell(saved_cell)

class MenuLegend:
    """Class defining the menu buttons"""

    # class variables
    fg_colour_enabled = (255, 255, 255)
    fg_colour_disabled = (80, 80, 80)
    bg_colour = (0, 0, 139)
    y_position = 378
    height = 21
    offset = 2

    def __init__(self, text, x_position, width):
        self.text = text
        self.x_position = x_position
        self.width = width
        self.enabled = True

    def display(self, enabled):
        global WIN, LOCAL_FONT

        self.enabled = enabled

        # draw background rectangle for the legend
        pygame.draw.rect(WIN, (MenuLegend.bg_colour), (self.x_position, MenuLegend.y_position, self.width, MenuLegend.height))

        if self.enabled:
            render_text = LOCAL_FONT.render(self.text, True, MenuLegend.fg_colour_enabled)
        else:
            render_text = LOCAL_FONT.render(self.text, True, MenuLegend.fg_colour_disabled)

        WIN.blit(render_text, (self.x_position + MenuLegend.offset, MenuLegend.y_position + MenuLegend.offset))

# ====================================================
# Global functions
# ====================================================

def load_config(grid):
    """Load global constants and grid state from the config file"""
    global CFG, CFG_FILENAME, FG_COLOUR, BG_COLOUR, INTERVAL
    cfg_display = 'display'
    cfg_fgcolour = 'fgcolour'
    cfg_bgcolour = 'bgcolour'
    cfg_timer = 'timer'
    cfg_interval = 'interval'

    if CFG.read(CFG_FILENAME) == []: # empty list means failure to read config file
        # no config file - leave settings as defaults
        return

    try:
        tmp_r,tmp_g,tmp_b = CFG[cfg_display][cfg_fgcolour].split(',')
        FG_COLOUR = (int(tmp_r), int(tmp_g), int(tmp_b))
    except:
        if not CFG.has_section(cfg_display):
            CFG.add_section(cfg_display)
        CFG[cfg_display][cfg_fgcolour] = str(FG_COLOUR[0]) + ',' + str (FG_COLOUR[1]) + ',' + str(FG_COLOUR[2])

    try:
        tmp_r,tmp_g,tmp_b = CFG[cfg_display][cfg_bgcolour].split(',')
        BG_COLOUR = (int(tmp_r), int(tmp_g), int(tmp_b))
    except:
        if not CFG.has_section(cfg_display):
            CFG.add_section(cfg_display)
        CFG[cfg_display][cfg_bgcolour] = str(BG_COLOUR[0]) +',' + str(BG_COLOUR[1]) + ',' + str(BG_COLOUR[2])

    try:
        INTERVAL = int(CFG[cfg_timer][cfg_interval])
    except:
        if not CFG.has_section(cfg_timer):
            CFG.add_section(cfg_timer)
        CFG[cfg_timer][cfg_interval] = str(INTERVAL)

    # load_pattern = []

    # Load the stored pattern
    try:
        load_pattern = CFG['pattern']['cells'].split('|')
    except ValueError:
        return # bad data - abandon attempt to load

    if load_pattern == []: # if nothing found
        return

    try:
        # ValueError will raise if wrong no. of assignments to left hand side
        load_list = []
        for elem in load_pattern:
            cl,rw = elem.split(',')
            int_cl = int(cl)
            int_rw = int(rw)
            if int_cl < 0 or int_cl > CellArray.grid_width or int_rw < 0 or int_rw > CellArray.grid_height:
                # if out of range
                raise IndexError
            load_list.append((int_cl, int_rw))
    except ValueError:
        print("Value error reached on load")
        return
    except IndexError:
        print("Index error reached")
        return

    grid.load_save_data(load_list)

def apply_game_rules(source_grid, dest_grid):
    """Apply 'Game of Life' rules"""
    # 1. Any live cell with <2 live neighbours dies
    # 2. Any live cell with 2 or 3 neighbours survives
    # 3. Any live cell with >3 neighbours dies
    # 4. Any dead cell with exactly 3 live neighbours becomes live

    for row in range(CellArray.grid_width):
        for col in range(CellArray.grid_height):
            count_neighbours = source_grid.count_live_neighbours((col, row))
            if source_grid.get_cell((col, row)): # if already live
                if count_neighbours < 2 or count_neighbours > 3:
                    dest_grid.unset_cell((col, row))
                else:
                    dest_grid.set_cell((col, row))
            else: # if already dead
                if count_neighbours == 3:
                    dest_grid.set_cell((col, row))
                else:
                    dest_grid.unset_cell((col, row))

def animate():
    """Start the Game of Life animation. Menu choice F1"""
    global grid_alpha, grid_beta
    global FG_COLOUR, BG_COLOUR

    # grey out unavailable menu items
    legend[1].display(False)
    legend[2].display(False)
    legend[3].display(False)

    return_state = True
    local_run = True

    # the 'cycle' variable will store which of the two cycles
    # we are in, i.e.
    # A - Alpha is main display, Beta is reserve
    # B - Beta is main display, Alpha is reserve
    cycle = 'A'

    while local_run:
        for local_event in pygame.event.get():
            if local_event.type == pygame.QUIT:
                local_run = False
                return_state = False
            if local_event.type == pygame.KEYDOWN:
                if local_event.key == pygame.K_F1 or local_event.key == pygame.K_ESCAPE: # F1 or Esc = stop
                    local_run = False
                if local_event.key == pygame.K_F5:
                    local_run = False
                    return_state = False

        if cycle  == 'A':
            apply_game_rules(grid_alpha, grid_beta)
            grid_beta.draw()
            cycle = 'B'
        else:
            apply_game_rules(grid_beta, grid_alpha)
            grid_alpha.draw()
            cycle = 'A'

        pygame.time.delay(INTERVAL)

    # re-enable menu items
    legend[1].display(True)
    legend[2].display(True)
    legend[3].display(True)
    pygame.display.update()

    return return_state

def clear_grid():
    """Clear the grid. Menu choice F2"""
    grid_alpha.clear()
    grid_alpha.draw()

def draw_cells(grid):
    """Draw on the grid. Menu choice F3"""

    # grey out unavailable menu items
    legend[0].display(False)
    legend[1].display(False)
    legend[3].display(False)
    pygame.display.update()

    return_state = True

    def convert_mousepos_to_cellpos(mouse_pos):
        """Map the mouse position on screen to the game cell that it points to"""
        return (int(mouse_pos[0] / CellArray.cell_size), int(mouse_pos[1] / CellArray.cell_size))

    local_run = True
    while local_run:
        for local_event in pygame.event.get():
            if local_event.type == pygame.QUIT:
                local_run = False
                return_state = False
            if local_event.type == pygame.KEYDOWN:
                if local_event.key == pygame.K_F3 or local_event.key == pygame.K_ESCAPE: # F3 or Esc - stop
                    local_run = False
                if local_event.key == pygame.K_F5:
                    local_run = False
                    return_state = False
            if local_event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]: # left button clicked
                    grid.set_cell(convert_mousepos_to_cellpos(pygame.mouse.get_pos()))
                    grid.draw()
                elif pygame.mouse.get_pressed()[2]: # right button clicked
                    grid.unset_cell(convert_mousepos_to_cellpos(pygame.mouse.get_pos()))
                    grid.draw()

    # re-enable menu items
    legend[0].display(True)
    legend[1].display(True)
    legend[3].display(True)
    pygame.display.update()

    return return_state

# ====================================================
# Main code
# ====================================================

pygame_error = pygame.init()
# pygame.init() does not raise an exception but returns a tuple: (no. of successes, no. of failures)
if pygame_error[1]:
    print('Pygame failed to initialise: ',pygame_error[1],' error(s)')
    exit()
del pygame_error

if not pygame.font.get_init():
    pygame.font.init()

LOCAL_FONT = pygame.font.Font(None, 22)

WIN = pygame.display.set_mode((378, 399))
pygame.display.set_caption("Conway's Game of Life")

CFG = configparser.ConfigParser()
CFG_FILENAME = 'gameoflife.ini'

# Set up legend buttons
legend = [MenuLegend('F1 Start/Stop', 5, 95), \
          MenuLegend('F2 Clear', 105, 64),\
          MenuLegend('F3 Edit', 174, 64), \
          MenuLegend('F4 Save', 243, 64), \
          MenuLegend('F5 Quit', 312, 64)]

legend[0].display(True)
legend[1].display(True)
legend[2].display(True)
legend[3].display(True)
legend[4].display(True)

# Set up CellArrays to store game elements
# Alpha and Beta CellArray objects will be used alternately to store the
# displayed grid and the reserve grid for building the next display

# globals for colours
FG_COLOUR = (255, 255, 255)
BG_COLOUR = (0, 0, 0)

# initialise interval timer
INTERVAL = 500 # 500 ms

# Set up the two grids
grid_alpha = CellArray()
grid_beta = CellArray()

load_config(grid_alpha)

grid_alpha.draw()

pygame.time.delay(INTERVAL)

# ===============================================
# MAIN LOOP
# ===============================================
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_F5: # q or F5 = quit
                run = False
            if event.key == pygame.K_F1:
                if not animate():
                    run = False # called function returns False if Quit was pressed
            if event.key == pygame.K_F2:
                clear_grid()
            if event.key == pygame.K_F3:
                if not draw_cells(grid_alpha): # called function returns False if Quit was pressed
                    run = False
            if event.key == pygame.K_F4:
                grid_alpha.save_data()

pygame.quit()
