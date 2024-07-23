from PIL import ImageGrab, ImageDraw
import pyautogui
from matplotlib import pyplot as plt
import subprocess
import time
import numpy as np
import random
import pyautogui

'''

def get_pixel_color_and_position():
    # Pobranie aktualnej pozycji kursora
    x, y = pyautogui.position()

    # Zrobienie zrzutu ekranu wokół kursora
    screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))

    # Pobranie koloru piksela
    pixel_color = screenshot.getpixel((0, 0))

    return x, y, pixel_color


# Sprawdzenie koloru piksela pod kursorem
while True:
    x, y, color = get_pixel_color_and_position()
    print(f"Koordynaty piksela: ({x}, {y})")
    print(f"Kolor piksela: {color}")'''

# Close existing Minesweeper windows
windows = pyautogui.getWindowsWithTitle('Minesweeper')
if windows:
    for win in windows:
        win.close()

# Launch a new instance of Minesweeper
subprocess.Popen(["C:\\Users\\alexx\\Desktop\\Minesweeper-Windows-XP\\WINMINE.exe"])
time.sleep(0.2)
win = pyautogui.getWindowsWithTitle('Minesweeper')[0]
time.sleep(0.2)
win.activate()
time.sleep(1)
win.moveTo(0, 0)

# Define the field size
global first_loop
first_loop = 1
field = [['' for i in range(30)] for i in range(16)]
buttons = [['' for i in range(30)] for i in range(16)]
final_field = [['' for i in range(30)] for i in range(16)]
number_pos = []
exclude_list = []


def closest_color(pixel_color, colors):
    colors = np.array(colors)
    pixel_color = np.array(pixel_color)
    distances = np.sqrt(np.sum((colors - pixel_color) ** 2, axis=1))
    closest_index = np.argmin(distances)
    return closest_index


def B_to_M(field, position_array, number_array):
    start_x = 15
    start_y = 100
    numb = []
    for pos in position_array:
        field[pos[0]][pos[1]] = 'M'
    for pos in number_array:
        bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < pos[0] + i < 30 and -1 < pos[1] + j < 16:
                    if field[pos[1] + j][pos[0] + i] == 'M':
                        bombs += 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < pos[0] + i < 30 and -1 < pos[1] + j < 16:
                    if bombs == int(field[pos[1]][pos[0]]):
                        if field[pos[1] + j][pos[0] + i] == 'B':
                            field[pos[1] + j][pos[0] + i] = 'E'
                            move = (pos[0] + i, pos[1] + j)
                            numb.append(move)
    print(numb)
    for pos in numb:
        pyautogui.click(start_x + 7 + (pos[0]) * 16, start_y + 7 + (pos[1]) * 16)
        print(f'pressing button {pos[1]} {pos[0]}')
    return field

def nums_to_blank(field,pos):
    for p in pos:
        field[p[0]][p[1]] = ' '
    return field

def divide_in_groups(positions):
    groups = []
    for pos in positions:
        added_to_group = False
        for group in groups:
            for group_pos in group:
                if abs(pos[0] - group_pos[0]) <= 2 and abs(pos[1] - group_pos[1]) <= 2:
                    group.append(pos)
                    added_to_group = True
                    break
            if added_to_group:
                break
        if not added_to_group:
            groups.append([pos])
    print(f' groups: {groups}')
    return groups

def pos_of_numbers(field):
    pos = []
    for i in range(16):
        for j in range(30):
            if field[i][j] == '1' or field[i][j] == '2' or field[i][j] == '3' or field[i][j] == '4' or field[i][j] == '5' or field[i][j] == '6' or field[i][j] == '7':
                move = (j, i)
                pos.append(move)
    return pos

def find_mines(field, pos_array):
    print('find_mines field:')
    pos = []
    full_nums = []
    for row in field:
        print(' '.join(row))
    for position in pos_array:
        numb_of_bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < position[0] + i < 30 and -1 < position[1] + j < 16:
                    if field[position[1] + j][position[0] + i] == 'B':
                        numb_of_bombs += 1
        if numb_of_bombs == int(field[position[1]][position[0]]):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if -1 < position[0] + i < 30 and -1 < position[1] + j < 16:
                        if field[position[1] + j][position[0] + i] == 'B':
                            move = ((position[1] + j), (position[0] + i))
                            pos.append(move)
                            move2 = ((position[1]), (position[0]))
                            full_nums.append(move2)
    ne_board = B_to_M(field, pos, pos_array)
    new_board = nums_to_blank(ne_board, full_nums)
    print('new board ')
    for row in new_board:
        print(' '.join(row))
    numbs = pos_of_numbers(field)
    group_array = divide_in_groups(numbs)

    return new_board


def random_press(field):
    start_x = 15
    start_y = 100
    B_positions = [(j, i) for i in range(30) for j in range(16) if field[j][i] == 'B']
    if B_positions:
        pos = random.choice(B_positions)
        pyautogui.click(start_x + 7 + (pos[1]) * 16, start_y + 7 + (pos[0]) * 16)
        field[pos[0]][pos[1]] = 'E'  # Mark as explored
    return field


def testing(field):
    global first_loop
    image_taken = 0
    colors = [(192, 192, 192), (0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (128, 0, 0), (0, 128, 128)]
    numbers = ['B', '1', '2', '3', '4', '5', '6']
    test_image_grab = False
    start_x = 15
    start_y = 100

    pyautogui.PAUSE = 0
    pyautogui.click(start_x + 16 * 15 + 7, start_y + 8 * 16 + 7)

    screen = ImageGrab.grab()

    for j in range(16):
        for i in range(30):
            color = screen.getpixel((start_x + 7 + i * 16, start_y + 9 + j * 16))
            closest_index = closest_color(color, colors)
            field[j][i] = numbers[closest_index]
            final_field[j][i] = numbers[closest_index]
            if numbers[closest_index] != 'B':
                move = (i, j)
                if move not in number_pos:
                    number_pos.append(move)
            if field[j][i] == 'B':
                if (i, j) not in exclude_list:
                    color_B = screen.getpixel((start_x + 1 + i * 16, start_y + 3 + j * 16))
                    if color_B == (192, 192, 192):
                        buttons[j][i] = ' '
                elif buttons[j][i] != ' ':
                    buttons[j][i] = 'B'
                else:
                    buttons[j][i] = ' '
                if buttons[j][i] == ' ' and field[j][i] == 'B':
                    final_field[j][i] = ' '
                    move = (i, j)
                    exclude_list.append(move)
                image_taken += 1
    for row in final_field:
            print('|'.join(row))
    print(final_field)
    print('images taken:', image_taken)
    if first_loop == 1 and image_taken == 80:
        return
    first_loop = 0
    ###
    color = screen.getpixel((259, 78))
    if color == (0,0,0):
        reset()
    sieved_field = find_mines(final_field, number_pos)
    for row in sieved_field:
        print(' '.join(row))
    # Check if there are no more moves and make a random press
    if sieved_field == field:
        #sieved_field = random_press(sieved_field)
        all_loops = [0 for i in range(30) for i in range(16)]
        possible_mines = [0 for i in range(30) for i in range(16)]
        if image_taken < 479:
            pass


    testing(sieved_field)
def reset():
    pass
    '''pyautogui.moveTo(20, 700)
    pyautogui.click()
    pyautogui.hotkey('shift', 'f10')'''


'''import pyautogui
from PIL import ImageGrab


def get_pixel_color_and_position():
    # Pobranie aktualnej pozycji kursora
    x, y = pyautogui.position()

    # Zrobienie zrzutu ekranu wokół kursora
    screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))


    # Pobranie koloru piksela
    pixel_color = screenshot.getpixel((0, 0))

    return x, y, pixel_color


# Sprawdzenie koloru piksela pod kursorem
while True:
    x, y, color = get_pixel_color_and_position()
    print(f"Koordynaty piksela: ({x}, {y})")
    print(f"Kolor piksela: {color}")'''

testing(field)
'''[['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '2', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '2', 'B', 'B', '1', ' ', ' ', ' ', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', 'B', '2', '2', '4', '4', '4', '2', '1', '1', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '2', '2', '2', 'B', 'B', 'B', '2', 'B', '2', '2', 'B', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', 'B', '1', '1', '2', '3', '2', '2', '2', 'B', '2', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', ' ', ' ', ' ', ' ', ' ', '1', '2', '2', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', 'B', 'B', 'B', 'B', '3', 'B', '1', ' ', ' ', ' ', ' ', '1', '2', '2', '2', 'B', '3', '3', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '2', '4', '4', '3', '2', '1', '1', ' ', '1', '2', '2', '2', 'B', 'B', '2', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '1', ' ', '1', 'B', '2', '2', '2', '1', ' ', '1', 'B', 'B', '3', '3', '2', '2', '2', '4', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '1', ' ', '1', '2', '3', 'B', 'B', '1', '1', '2', '3', '3', 'B', '2', '1', '2', 'B', '3', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '1', '1', '2', 'B', '4', '2', '1', '1', 'B', '1', '1', '1', '3', 'B', '3', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', 'B', '1', '2', 'B', '2', ' ', ' ', '1', '1', '1', ' ', ' ', '2', 'B', '3', '2', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '1', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', 'B', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]'''
'''[['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '1', '1', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', ' ', ' ', ' ', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '1', ' ', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '4', '2', '2', 'B', '4', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]'''
