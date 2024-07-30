from PIL import ImageGrab, ImageDraw
import pyautogui
from matplotlib import pyplot as plt
import subprocess
import time
import numpy as np
import random
import pyautogui
import itertools
import copy
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
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
# Close existing Minesweeper windows
windows = pyautogui.getWindowsWithTitle('Minesweeper')
if windows:
    for win in windows:
        win.close()

# Launch a new instance of Minesweeper
mouse_track = True
subprocess.Popen(["C:\\Users\\alexx\\Desktop\\Minesweeper-Windows-XP\\WINMINE.exe"])
time.sleep(0.2)
win = pyautogui.getWindowsWithTitle('Minesweeper')[0]
time.sleep(0.2)
win.activate()
time.sleep(1)
win.moveTo(0, 0)

# Define the field size

field = [['' for i in range(30)] for i in range(16)]
buttons = [['' for i in range(30)] for i in range(16)]
final_field = [['' for i in range(30)] for i in range(16)]
number_pos = []
exclude_list = []
#makes move
def make_move(pos):
    win.activate()
    time.sleep(0.5)
    if pos != (15,8):
        a = input(f'trying to press at {pos}, continue?')
        if a == 'y':
            print('pressing at ',(15+pos[0]*16+8,100+pos[1]*16+8))
            pyautogui.click(15+pos[0]*16+8,100+pos[1]*16+8)

    pyautogui.click(15 + pos[0] * 16 + 8, 100 + pos[1] * 16 + 8)
def make_move_no_delay(pos):
    win.activate()

    if pos != (15,8):

            print('pressing at ',(15+pos[0]*16+8,100+pos[1]*16+8))
            pyautogui.click(15+pos[0]*16+8,100+pos[1]*16+8)

    pyautogui.click(15 + pos[0] * 16 + 8, 100 + pos[1] * 16 + 8)
#using image recognition it determines where what should be
def closest_color(pixel_color, colors):
    colors = np.array(colors)
    pixel_color = np.array(pixel_color)
    distances = np.sqrt(np.sum((colors - pixel_color) ** 2, axis=1))
    closest_index = np.argmin(distances)
    return closest_index
# field, position of 100% bombs , position of ALL numbers
def B_to_M(field, position_array, number_array):
    print('called B_to_M')
    start_x = 15
    start_y = 100
    numb = []   # this array have position of numbers that should be doubleclicked, meaning that there is enough mines around them and buttons that dont have mine
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
                            #pyautogui.click(start_x + pos[1]+j*16+8, start_y + pos[0]+i*16+8)
                            field[pos[1] + j][pos[0] + i] = 'E'
                            move = (pos[0] + i, pos[1] + j)
                            numb.append(move)
    print(numb)
    print('b_to_m board')
    for row in field:
        print(' '.join(row))
    for pos in numb:
        make_move_no_delay((pos[0],pos[1]))
        #pyautogui.click(start_x + 7 + (pos[0]) * 16, start_y + 7 + (pos[1]) * 16)
        print(f'pressing button {pos[1]} {pos[0]}')
    updated_field = update_board()
    return updated_field
#given an array it makes all numbs into ' '
def nums_to_blank(field, pos):
    for p in pos:
        print(p)
        print(p[0])
        print(p[1])
        field[p[0]][p[1]] = ' '
        print('numbs to blank')
        for row in field:
            print(' '.join(row))
    return field
#creates groups from positions that are not further tha n2 from each other
#todo: add so they need to have sharing mine
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
    print(f' (d_i_n) groups: {groups}')
    return groups
#returns positions of numbers on the field
def pos_of_numbers(field):
    pos = []
    for i in range(16):
        for j in range(30):
            if field[i][j] == '1' or field[i][j] == '2' or field[i][j] == '3' or field[i][j] == '4' or field[i][j] == '5' or field[i][j] == '6' or field[i][j] == '7':
                move = (j, i)
                pos.append(move)
    return pos
#takes field and pos of ALL the number position
def find_mines(field, pos_array):

    print('find_mines field:')
    pos = [] # array that will show position of buttons that have mines 100%
    full_nums = []
    for row in field:
        print(' '.join(row))
    for position in pos_array:
        numb_of_bombs = 0 # number of bombs surrounding certain number
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < position[0] + i < 30 and -1 < position[1] + j < 16:
                    if field[position[1] + j][position[0] + i] == 'B':
                        numb_of_bombs += 1
        # if numbs of bombs is the same as number, the number is full and everything surrounding it is not a bomb
        if numb_of_bombs == int(field[position[1]][position[0]]):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if -1 < position[0] + i < 30 and -1 < position[1] + j < 16:
                        if field[position[1] + j][position[0] + i] == 'B':
                            move = ((position[1] + j), (position[0] + i))
                            #position of 100% bomb
                            pos.append(move)
                            #position of full number
                            move2 = ((position[1]), (position[0]))
                            full_nums.append(move2)

    ne_board = B_to_M(field, pos, pos_array)

    new_board = nums_to_blank(ne_board, full_nums)
    print('new board ')
    for row in new_board:
        print(' '.join(row))
    numbs = pos_of_numbers(field)
    group_array = divide_in_groups(numbs)

    return new_board,group_array,full_nums,field
#removes b that are not important for bruteforcing
def irrelevant_b(field):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    pos = []
    for i in range(16):
        for j in range(30):
            #print('irrelevant b field')

            if field[i][j] in numbers:
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if -1 < i + 2 < 16 and -1 < j + y < 30:
                            if field[i + x][j + y] == 'B':
                                p = (i + x, j + y)
                                pos.append(p)
    #print('positions of numbers',pos)
    for i in range(16):
        for j in range(30):
            if field[i][j] == 'B' and (i, j) not in pos:
                field[i][j] = ' '

    return field
#returns positions of fill numbers
def full_numbers(field):
    numbers = ['1', '2', '3', '4', '5', '6']
    pos = []
    for yy in range(16):
        for xx in range(30):
            numb = 0

            if field[yy][xx] in numbers:
                #print('found numbner at position ' + str(yy) + ',' + str(xx))
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if -1 < yy + y < 16 and -1 < xx + x < 30:
                            #print('past if statement 1')
                            if field[yy + y][xx + x] == 'M':
                                print(f'found bomb at position ' + str(xx+x) + ',' + str(yy+y), f'for x ={x}, y={y}, yy={yy} xx={xx}')
                                numb += 1
                if numb == int(field[yy][xx]):
                    p = (yy,xx)
                    pos.append(p)
    print(pos,'full number pos')
    return pos  ## WORKING
#the
def fun_bruteforcer(field, array, groups):
    copy_field = copy.deepcopy(field)
    print(array, 'array in funbruteforcer')
    print('fun bruteforcer starts')

    numbs = full_numbers(field)
    field = nums_to_blank(field, numbs)
    # field = irrelevant_b(field)
    for row in field:
        print(' '.join(row))

    all_boards = []
    pos_of_b = []
    final_pos_of_b = []
    groups_of_b = []
    print(array, 'array')  # placement of all numbers

    for pos in array:
        positions = [
            (pos[0] + 1, pos[1] - 1),
            (pos[0] + 1, pos[1]),
            (pos[0] + 1, pos[1] + 1),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0] - 1, pos[1] - 1),
            (pos[0] - 1, pos[1] + 1)
        ]

        for move in positions:
            if move not in pos_of_b:
                pos_of_b.append(move)

        print(pos_of_b, 'pos of b bbb')
        for posit in pos_of_b:
            print(posit, 'current pos bruteforcing')
            if field[posit[1]][posit[0]] == 'B': # posit[1] out of range cuz no B generates?
                print('found b at pos ', posit[0], ' ', posit[1])
                if posit not in final_pos_of_b:
                    final_pos_of_b.append(posit)
                    print('appending', posit)

        print(final_pos_of_b, 'final pos b')
        test_field = copy.deepcopy(field)
        new_board = [[' ' for i in range(30)] for i in range(16)]
        # Fix the indexing and condition
        for pos in array:
            for x in range(-1,2):
                for y in range(-1,2):
                    if -1 < pos[0]+x < 30 and -1 < pos[1]+y < 16:
                        new_board[pos[1]+y][pos[0]+x] = test_field[pos[1]+y][pos[0]+x]
        for row in new_board:
            print(' '.join(row))
        print('end of test')

        print('edited field for group')
        for row in copy_field:
            print(' '.join(row))

        if len(final_pos_of_b) > 30:
            print('group too long, too much to compute, resetting')
            time.sleep(0.5)
            reset()

        groups_of_b.append([final_pos_of_b])

    print('positions in pos tosdjfgkljsfn')

    import sys
    combinations = list(itertools.product(['B', 'M'], repeat=len(final_pos_of_b)))
    total_combinations = len(combinations)
    # Starting time
    start_time = time.time()
    z = 0
    for combination in combinations:
        # Calculate percentage completed
        percentage_completed = (z / total_combinations) * 100
        # Calculate elapsed time and estimated time remaining
        elapsed_time = time.time() - start_time
        if z > 0:  # Ensure not dividing by zero
            time_per_combination = elapsed_time / z
            estimated_time_remaining = (total_combinations - z) * time_per_combination
        else:
            estimated_time_remaining = 0
        # Print progress details
        print(
            f'\r{z + 1}/{total_combinations} ({percentage_completed:.1f}%) - ETA: {estimated_time_remaining:.2f} seconds',
            end='', flush=True)
        z += 1
        #print(field,'field') this one good
        new_field = copy.deepcopy(new_board)
        #new_field = copy.deepcopy(field) ##might be bad decision commenting it out,


        for pos, value in zip(final_pos_of_b, combination):
                #print(pos, '|', value, '| pos and value')
                new_field[pos[1]][pos[0]] = value

        all_boards.append(new_field)
    print('validating',array)
    booard = validate_boards(all_boards,array)
    percentage_field  = check_percent(booard)
    min_percentage, min_pos = float('inf'), None
    for y in range(len(percentage_field)):
        for x in range(len(percentage_field[0])):
            if 0 < float(percentage_field[y][x]) < min_percentage:  # Ignore zeroes as they can't be valid moves
                print('stored perc ', percentage_field[y][x])
                min_percentage = float(percentage_field[y][x])
                pos_of_min = (x,y)
                #print('positions ',(x*16+8, y*16+8))


                #pyautogui.click(15 + x*16+8,100 + y*16+8)
    print('making button press after calculation on pos: ', pos_of_min)
    #time.sleep(1)
    return pos_of_min
#checks which move is the best, tied to bruteforcer
def check_percent(boards):
    print('num of boards:', len(boards))
    num_boards = len(boards)
    #num_rows = len(boards[0])
    #num_cols = len(boards[0][0])

    new_field = [[0 for _ in range(30)] for _ in range(16)]

    for i in range(30):
        for j in range(16):
            num_mines = sum(1 for board in boards if board[j][i] == 'M')

            percentage = (num_mines / num_boards) * 100
            # Format the percentage with leading zeros
            formatted_percentage = f"{percentage:.2f}"
            if len(formatted_percentage) < 5:
                formatted_percentage = formatted_percentage.zfill(5)
            new_field[j][i] = formatted_percentage

    for row in new_field:
        print(' '.join(f"{cell}%" for cell in row))
    #time.sleep(2)
    return new_field
#checks if created by a bruteforcer board is valid or no
def validate_boards(board_array,pos): # position on numbers to check
    good_boards = []

    numbers = ['1', '2', '3', '4', '5', '6']
    print(len(board_array), 'boards')
    '''for board in board_array:
        for row in board:
            print(' '.join(row))
        print()'''
    for board in board_array:
        is_good = True
        # print(len(field),len(field[0]))
        for y in range(16):
            for x in range(30):

                if board[y][x] in numbers:
                    if (x,y) in pos:

                        bomb_numb = 0

                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if 0 <= y + i < len(board) and 0 <= x + j < len(board[0]):
                                    #print('step 3')
                                    if board[y + i][x + j] == 'M':
                                        bomb_numb += 1
                                        #print('bomb up +1')
                                        # print('bomb numb up: ', bomb_numb)
                        #print(bomb_numb,int(board[y][x]),'testwazne')
                        if bomb_numb != int(board[y][x]):
                            is_good = False
                            break

            if not is_good:
                break
        if is_good:
            good_boards.append(board)
    print(len(good_boards), ' valid')
    if len(good_boards) <30: #lenght groupp
        for numb,board in enumerate(good_boards):
            print(numb)
            for row in board:
                print(' '.join(row))
            print()
    # print(good_boards)
    return good_boards

def testing(field):
    global mouse_track

    image_taken = 0
    colors = [(192, 192, 192), (0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (128, 0, 0), (0, 128, 128)]
    numbers = ['B', '1', '2', '3', '4', '5', '6']
    test_image_grab = False
    start_x = 15
    start_y = 100

    pyautogui.PAUSE = 0
    #pyautogui.click(start_x + 16 * 15 + 7, start_y + 8 * 16 + 7)
    if mouse_track == True:
        make_move((15,8))
    screen = ImageGrab.grab()   #image grav one pixel insteead of entire screen
    #image recognition that checks the board state
#region
    for j in range(16):
        for i in range(30):
            color = screen.getpixel((start_x + 7 + i * 16, start_y + 9 + j * 16))
            closest_index = closest_color(color, colors)
            #create 2 boards
            field[j][i] = numbers[closest_index]
            final_field[j][i] = numbers[closest_index]
            #check if this is number and append as number position
            if numbers[closest_index] != 'B' and numbers[closest_index] != ' ':
                move = (i, j)
                if move not in number_pos:
                    number_pos.append(move)
            if field[j][i] == 'B':
                #tis one to prevent having a lot of same positions in one array
                if (i, j) not in exclude_list:
                    #checks for border color to determine if its b or empty
                    color_B = screen.getpixel((start_x + 1 + i * 16, start_y + 3 + j * 16))
                    if color_B == (192, 192, 192):
                        buttons[j][i] = ' '
                elif buttons[j][i] != ' ':
                    buttons[j][i] = 'B'
                else:
                    buttons[j][i] = ' '
                    #check if board place is empty or not by comparing buttons board and field (its good dont bother yourself with it)
                    # if youre ,looking for errors it might be with the else statement im writing it in
                if buttons[j][i] == ' ' and field[j][i] == 'B':
                    final_field[j][i] = ' '
                    move = (i, j)
                    exclude_list.append(move)
                image_taken += 1
#endregion
    for row in final_field:
            print('|'.join(row))
    print(final_field)
    print('images taken:', image_taken)


    ###check if player is still alive
    color = screen.getpixel((259, 78))
    if color == (0,0,0):
        print('lost, reseting')
        time.sleep(0.4)
        reset()
    #find mines from given board and position of all numbers on the feald
    sieved_field,group_array,full_n,field = find_mines(final_field, number_pos)
    #sieved_field = update_board()
    #sieved_no_B = irrelevant_b(sieved_field)
    #print('sieved_no_B')
    #for row in sieved_no_B:
    #    print(' '.join(row))
    #sieved_full = full_numbers(sieved_no_B)

    for row in sieved_field:
        print(' '.join(row))
    '''for i in range(16):
        for j in range(30):
            if field[i][j] == 'E':
                make_move((j,i))'''
    ##bruteforcing##




    #edit field board to look closer to sieved

    full_numbs = full_numbers(field)
    f_no_numbs = nums_to_blank(field,full_numbs)
    position_of_mines = [] #(x,y)
    #this is last
    for i in range(16):
        for j in range(30):
            if f_no_numbs[i][j] == 'M':
                f_no_numbs[i][j] = 'B'
                pos = (j,i)
                position_of_mines.append(pos)
    field = copy.deepcopy(f_no_numbs)
    # Check if there are no more moves and make a random press
    print('###check if need to bruteforce###')
    print('sieved field')
    for row in sieved_field:
        print(' '.join(row))
    print('field')
    for row in field:
        print(' '.join(row))

    if sieved_field == field:
        print('they are the same')
        #print('cant do much more')
        pos_of_numbs = pos_of_numbers(field)
        print('pos of numbers:', pos_of_numbs)
        groups = divide_in_groups(pos_of_numbs)
        print('groupps:', groups)
        full_num = full_numbers(field)
        print('full_num:', full_num)
        field_no_numbs = nums_to_blank(field, full_num)
        print('field_no_numbs:')
        for row in field_no_numbs:
            print(' '.join(row))
        field_no_B = irrelevant_b(field_no_numbs)
        print('field_no_B:')
        for row in field_no_B:
            print(' '.join(row))
        print(group_array, 'group array')
        print(groups,',groups')
        '''if len(groups) == 1 and len(groups[0]) == 2:
            
            print('too short groups, resetting')
            time.sleep(0.5)
            reset()
        else:
            '''
        for group in groups:
            print((field_no_B, group, groups), 'stuff to copy')

            bruteforced_move = fun_bruteforcer(field_no_B, group,groups)
            make_move(bruteforced_move)
        #sieved_field = random_press(sieved_field)

        if image_taken < 479:
            pass

        field_recursive = update_board()
        testing(field_recursive)
    else:
        print('they are not the same working on this board now:')
        for row in sieved_field:
            print(' '.join(row))
        testing(sieved_field)
        mouse_track  = False
#uses image regocnition, returns updated board from image recognition | tested
def update_board():
    field = [['' for i in range(30)] for i in range(16)]
    final_field = [['' for i in range(30)] for i in range(16)]
    colors = [(192, 192, 192), (0, 0, 255), (0, 128, 0), (255, 0, 0), (0, 0, 128), (128, 0, 0), (0, 128, 128)]
    numbers = ['B', '1', '2', '3', '4', '5', '6']
    start_x = 15
    start_y = 100
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
    return final_field

def reset():
    a = input('reset? y/n')
    if a == 'y':
        print('resetting')

        pyautogui.moveTo(20, 700)
        pyautogui.click()
        pyautogui.hotkey('shift', 'f10')


testing(field)
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


'''[['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '2', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '2', 'B', 'B', '1', ' ', ' ', ' ', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', 'B', '2', '2', '4', '4', '4', '2', '1', '1', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '2', '2', '2', 'B', 'B', 'B', '2', 'B', '2', '2', 'B', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', 'B', '1', '1', '2', '3', '2', '2', '2', 'B', '2', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', ' ', ' ', ' ', ' ', ' ', '1', '2', '2', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', 'B', 'B', 'B', 'B', '3', 'B', '1', ' ', ' ', ' ', ' ', '1', '2', '2', '2', 'B', '3', '3', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '2', '4', '4', '3', '2', '1', '1', ' ', '1', '2', '2', '2', 'B', 'B', '2', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '1', ' ', '1', 'B', '2', '2', '2', '1', ' ', '1', 'B', 'B', '3', '3', '2', '2', '2', '4', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '1', ' ', '1', '2', '3', 'B', 'B', '1', '1', '2', '3', '3', 'B', '2', '1', '2', 'B', '3', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '1', '1', '2', 'B', '4', '2', '1', '1', 'B', '1', '1', '1', '3', 'B', '3', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', 'B', '1', '2', 'B', '2', ' ', ' ', '1', '1', '1', ' ', ' ', '2', 'B', '3', '2', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', '2', '1', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', '2', 'B', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]'''
'''[['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '1', '1', '1', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', ' ', ' ', ' ', '1', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '1', ' ', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', '1', '2', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '4', '2', '2', 'B', '4', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']]'''
'''[['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', ' ', ' ', ' ', '1', 'B', '2', 'B', '2', '2', 'B', '1', ' ', '1', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', 'B', 'B', '2', ' ', ' ', ' ', '1', '1', '2', '2', 'B', '2', '1', '1', ' ', '2', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '2', '2', '1', ' ', ' ', ' ', ' ', ' ', ' ', '1', '1', '1', ' ', '1', '2', '3', 'B', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', ' ', '1', '1', '1', '1', '1', '1', ' ', ' ', ' ', ' ', ' ', ' ', '2', 'B', 'B', '2', '2', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', ' ', '1', 'B', '1', '1', 'B', '1', ' ', ' ', ' ', '1', '1', '1', '3', 'B', '4', '1', '1', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', '1', '2', '1', '1', '1', '2', '2', '1', ' ', ' ', '1', 'B', '1', '2', 'B', '2', '1', '2', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '4', 'B', '3', '2', '2', '1', '1', 'B', '1', ' ', '1', '2', '2', '1', '1', '1', '1', '2', 'B', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '5', 'B', 'B', '1', '1', '1', '1', '1', '3', 'B', '2', '1', '2', '2', '1', '2', 'B', '4', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '1', ' ', ' ', ' ', '2', 'B', 'B', '2', '2', 'B', 'B', '2', '2', '1', '2', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', ' ', ' ', ' ', ' ', '2', 'B', '3', '1', '2', 'B', '5', 'B', '3', '2', '3', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', ' ', ' ', '1', '1', '2', '2', '3', '2', '2', '1', '3', 'B', 'B', '2', 'B', 'B'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '2', ' ', ' ', '1', 'B', '1', '2', 'B', 'B', '2', '1', '3', '3', '3', '2', '2', '2'], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '2', '1', '1', '2', 'B', '3', '2', 'B', '2', 'B', '1', ' ', ' ', ' '], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', 'B', '1', ' ', ' ', '2', '2', '2', '1', '2', '3', '2', '1', ' ', ' ', ' '], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '3', '2', '1', '1', '3', 'B', '3', '1', '1', 'B', '1', ' ', ' ', ' ', ' '], ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', '1', '1', '1', '1', ' ', ' ', ' ', ' ']]'''
''' groups: [[(25, 0), (25, 1), (25, 2), (26, 3), (27, 3), (27, 4), (27, 5), (28, 7), (28, 8), (28, 9)], [(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (11, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (14, 13), (15, 14), (16, 14), (17, 14), (18, 14), (19, 14)]]
B B B B B B B B B B B M           M   M     M     1 B B B B
B B B B B B B B B 2 M M                 M         2 B B B B
B B B B B B B B B 2                               3 B B B B
B B B B B B B B B 1                             M M 2 2 B B
B B B B B B B B B 2     M     M                 M     1 B B
B B B B B B B B B 2                       M     M     2 B B
B B B B B B B B B 4 M           M                     M B B
B B B B B B B B B B M 5 M M             M             M 4 B
B B B B B B B B B B B B B 3           M M     M M       2 B
B B B B B B B B B B B B B 1           M       M   M     3 B
B B B B B B B B B B B B B 1                       M M   M M
B B B B B B B B B B B B B 2       M     M M                
B B B B B B B B B B B B B 3             M     M   M        
B B B B B B B B B B B B B M 3 M                            
B B B B B B B B B B B B B B B 3 2 1 1 3 M       M          
B B B B B B B B B B B B B B B B B B B B M M       '''


'''
todo:
zrobic cos takiego ze jest licznik min kory wyklucza rozwiazania ktore np maja wiecej min niz jest aktualnie,
jesli min jest 99max, wiadoma jest pozycja 90, a sa rozwiazania ktore maja 10 min w sobie, od razu mozna je skreslic

#make full_nums and nums to blank be callled be fore fun)_brutreforcer, so bruteforcer works on edited field and on smaller groups
#bruteforcer cannot be recursive functrion, it needs to be called once and go back to normalm way of searching mines
# you can make it return move so it just calls function like 'make move' and then moves forward with testing function
'''

