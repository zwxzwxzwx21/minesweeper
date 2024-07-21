from PIL import ImageGrab, ImageDraw
import pyautogui
from matplotlib import pyplot as plt
import subprocess
import time
import numpy as np
import cProfile
# Zamknięcie istniejących okien Minesweeper
windows = pyautogui.getWindowsWithTitle('Minesweeper')
if windows:
    for win in windows:
        win.close()

# Uruchomienie nowej instancji Minesweeper
subprocess.Popen(["C:\\Users\\alexx\\Desktop\\Minesweeper-Windows-XP\\WINMINE.exe"])
time.sleep(0.2)
win = pyautogui.getWindowsWithTitle('Minesweeper')[0]
time.sleep(0.2)
win.activate()
time.sleep(0.2)
win.moveTo(0, 0)

# Definiowanie rozmiaru pola
global first_loop
first_loop = 1
field = [['' for i in range(9)] for i in range(9)]
buttons = [['' for i in range(9)] for i in range(9)] # this one checks if button is blank or not pressed
final_field = [['' for i in range(9)] for i in range(9)]
number_pos = []
exclude_list = [] #list that excludes certain field from checking, basically position of all blanks
def closest_color(pixel_color, colors):
    colors = np.array(colors)
    pixel_color = np.array(pixel_color)
    distances = np.sqrt(np.sum((colors - pixel_color) ** 2, axis=1))
    closest_index = np.argmin(distances)
    return closest_index

def B_to_M(field,position_array,number_array):#changed b to mines
    numb = []  # this array have position of numbers that should be doubleclicked, meaning that there is enough mines around them and buttons that dont have mine
    for pos in position_array:
        field[pos[0]][pos[1]] = 'M'
    #check for obvious free spaces and make a button press if
    for pos in number_array:
        bombs = 0 # how many mines are around number
        for i in range(-1, 2):
            for j in range(-1, 2):
                # print(f'testtest {position[0]+i } {position[1]+j }')
                if -1 < pos[0] + i < 9 and -1 < pos[1] + j < 9:
                    # print(f'testinside {position[0] + i} {position[1] + j}')

                    if field[pos[1] + j][pos[0] + i] == 'M':
                        bombs += 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < pos[0] + i < 9 and -1 < pos[1] + j < 9:
                    if bombs == int(field[pos[1]][pos[0]]):
                        if field[pos[1]+j][pos[0]+i] == 'B':
                            field[pos[1]+j][pos[0]+i] = 'E'
                            move = (pos[1]+j,pos[0]+i)
                            numb.append(move)
    return field,numb
def find_mines(field,pos_array):
    print('find_mines field:')
    pos = [] # array that will show position of buttons that have mines 100%

    for row in field:
        print(' '.join(row))
    for position in pos_array:
        numb_of_bombs = 0 # number of bombs surrounding certain number
        #print(pos_array, 'cur pos', position)
        #number_of_buttons = 0 #number of bombs around current number
        for i in range(-1,2):
            for j in range(-1,2):
                #print(f'testtest {position[0]+i } {position[1]+j }')
                if -1 < position[0]+i < 9 and -1 < position[1]+j < 9:
                    #print(f'testinside {position[0] + i} {position[1] + j}')

                    if field[position[1]+j][position[0]+i] == 'B':
                        numb_of_bombs += 1
        #print(type(field[position[1]][position[0]],'int test'))
        #print(int(field[position[1]][position[0]]),'int test')
        print(f'numb of bombs = {numb_of_bombs}  for pos {position} int = {int(field[position[1]][position[0]])}')
        if numb_of_bombs == int(field[position[1]][position[0]]):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # print(f'testtest {position[0]+i } {position[1]+j }')
                    if -1 < position[0] + i < 9 and -1 < position[1] + j < 9:
                        # print(f'testinside {position[0] + i} {position[1] + j}')

                        if field[position[1] + j][position[0] + i] == 'B':
                            print(f' changing bomb to mine at position: {(position[1] + j)},{(position[0] + i)}')
                            move = ((position[1] + j),(position[0] + i))
                            pos.append(move)
    new_board,pos_to_click = B_to_M(field,pos,pos_array)

    for row in new_board:
        print(' '.join(row))
    import pyautogui

    for pos in pos_to_click:
        x = start_x + 7 + pos[1] * 14
        y = start_y + 7 + pos[0] * 14

        # Press both left and right buttons down
        pyautogui.mouseDown(x, y, button='left')
        pyautogui.mouseDown(x, y, button='right')

        # Release both buttons
        pyautogui.mouseUp(x, y, button='left')
        pyautogui.mouseUp(x, y, button='right')

    '''for i in range(9):
        for j in range(9):
            if field[i][j].isdigit():'''


    '''print(f'buttons around {position} {number_of_buttons}')'''
    for row in field:
        print(' '.join(row))



def testing():
    global first_loop
    image_taken = 0 #check how many images button scrpit taken
    start_time = time.time()
    print('start')
    colors = [(192, 192, 192), (0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (0, 0, 128), (0, 128, 128)]
    numbers = ['B', '1', '2', '3', '4', '5', '6',]
    test_image_grab = False
    start_x = 15
    start_y = 100

    pyautogui.PAUSE = 0
    pyautogui.click(start_x + 72, start_y + 72)

    if test_image_grab:
        screenshot = ImageGrab.grab(bbox=(start_x, start_y, start_x + 144, start_y + 144))  # 14,4px
        draw = ImageDraw.Draw(screenshot)
        for i in range(9):
            for j in range(9):
                draw.point((7 + i * 16, 9 + j * 16), fill='black')
        plt.imshow(screenshot)
        plt.axis('on')
        plt.show()
        #screenshot to sdistinguish buttons froms blanks
        screenshot2 = ImageGrab.grab(bbox=(start_x, start_y, start_x + 144, start_y + 144))  # 14,4px
        draw = ImageDraw.Draw(screenshot2)
        for i in range(9):
            for j in range(9):
                draw.point((1 + i * 16, 3 + j * 16), fill='black')
        plt.imshow(screenshot2)
        plt.axis('on')
        plt.show()

    screen = ImageGrab.grab()


    for j in range(9):
        for i in range(9):
            color = screen.getpixel((start_x + 7 + i * 16, start_y + 9 + j * 16))
            closest_index = closest_color(color, colors)
            field[j][i] = numbers[closest_index]
            final_field[j][i] = numbers[closest_index]
            if numbers[closest_index] != 'B':
                print(f'position of number = {i,j}', numbers[closest_index])
                move = (i,j)
                if move not in number_pos:
                    number_pos.append(move)
            if field[j][i] == 'B':
                #print( (i,j),exclude_list,'testexclude')
                if (i,j) not in exclude_list:
                    color_B = screen.getpixel((start_x + 1 + i * 16, start_y + 3 + j * 16)) #button or blank

                if color_B == (192, 192, 192):
                    buttons[j][i] = ' ' # blank space
                else:
                    buttons[j][i] = 'B' #white - button
                if buttons[j][i] == ' ' and field[j][i] == 'B':
                    final_field[j][i] = ' '
                    move = (i, j)
                    exclude_list.append(move)
                image_taken += 1
    for row in final_field:
        print('|'.join(row))
    print(final_field)
    print('images taken:', image_taken)
    if first_loop == 1:
        if image_taken == 80:
            print('bad seed, reset')
            return
    first_loop = 0
    print('done')
    end_time = time.time()
    elapsed = end_time - start_time
    print(f'time: {elapsed:.4f}')
    sieved_field = find_mines(final_field,number_pos)

#cProfile.run("testing()")
testing()
'''arr = [(5, 0), (7, 0), (0, 1), (1, 1), (5, 1), (6, 1), (7, 1), (1, 2), (2, 2), (2, 3), (6, 3), (7, 3), (8, 3), (0, 4), (1, 4), (2, 4), (6, 4), (4, 5), (5, 5), (6, 5), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6)]
fld = [[' ', ' ', ' ', ' ', ' ', '1', 'B', '1', ' '],
       ['1', '1', ' ', ' ', ' ', '1', '1', '1', ' '],
       ['B', '2', '1', ' ', ' ', ' ', ' ', ' ', ' '],
       ['B', 'B', '1', ' ', ' ', ' ', '1', '1', '1'],
       ['1', '1', '1', ' ', ' ', ' ', '1', 'B', 'B'],
       [' ', ' ', ' ', ' ', '1', '2', '3', 'B', 'B'],
       ['1', '1', '1', '1', '3', 'B', 'B', 'B', 'B'],
       ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
       ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]
find_mines(fld,arr)
'''