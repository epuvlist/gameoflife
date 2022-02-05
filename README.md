# gameoflife
Conway's Game of Life, written in Python 3 using the Pygame module.

Written as an exercise to learn Pygame.

A simple simulation of Conway's Game of Life
(for an explanation see https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

## Menu options:

- F1 - Start or Stop the simulation
- F2 - Clear all cells from the screen
- F3 - Edit. Add a pixel with left mouse click, remove with right mouse click
- F4 - Save the current pattern
- F5 - Quit

## .ini file

The accompanying .ini file contains some configuration settings, and can be edited
using a text editor. It must be in the same directory as the program file when run.

The [display] group specifies foreground and background colours as R,G,B groups, e.g.:

[display]

fgcolour = 255, 127, 0

bgcolour = 0, 0, 80

The [timer] group specifies the interval between simulation iterations in milliseconds
(adjust for your local processor speed):

[timer]

interval = 200

The [pattern] group contains the last saved pattern. Pixels are specified using x,y pairs
and separated by a '|' character, e.g.:

[pattern]

cells = 16,1|22,1|16,2|22,2|16,3|22,3|18,5|19,5|20,5|7,31|8,31|6,32|8,32|7,33|0,34|62,34|
0,35|61,35|61,36|0,37|3,37|61,37|62,37|1,38|2,38|4,38|1,39|2,39|4,39|15,39|16,39|17,39|
48,39|49,39|50,39|3,40|15,40|16,40|18,40|19,40|49,40|52,40|15,41|16,41|50,41|51,41|52,41|
11,42|12,42|50,42|51,42|12,43|13,43|14,43|17,43|20,43|51,43|53,43|54,43|4,44|5,44|11,44|
12,44|14,44|18,44|45,44|46,44|51,44|4,45|5,45|13,45|14,45|50,45|51,45|54,45|5,46|6,46|
7,46|43,46|47,46|48,46|49,46|50,46|51,46|52,46|53,46|6,47|9,47|43,47|48,47|50,47|51,47|
52,47|9,48|10,48|43,48|49,48|50,48|53,48|7,49|50,49|11,50|49,50|51,50|52,50|53,50|10,51|
48,51|47,52|46,53|47,53|50,53|45,54|46,54|48,54|50,54|46,55|47,55|48,55|60,55|0,56|1,56|
47,56|59,56|61,56|62,56|0,57|1,57|57,57|61,57|62,57|59,59|55,60|57,60|58,60|54,61|57,61|
18,62|19,62|20,62|55,62|56,62

