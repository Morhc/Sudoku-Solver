import matplotlib.pyplot as plt
from PIL import Image
import os, copy

def set_board(boardstate, instructions = 'easy'):

    new_boardstate = boardstate

    if instructions == 'easy':
        instructions = [(1,8,6), (3,8,3), (6,8,8), (8,8,4),
                        (0,7,5), (1,7,3), (2,7,7), (4,7,9),
                        (1,6,4), (5,6,6), (6,6,3), (8,6,7),
                        (1,5,9), (4,5,5), (5,5,1), (6,5,2), (7,5,3), (8,5,8),

                        (0,3,7), (1,3,1), (2,3,3), (3,3,6), (4,3,2), (7,3,4),
                        (0,2,3), (2,2,6), (3,2,4), (7,2,1),
                        (4,1,6), (6,1,5), (7,1,2), (8,1,3),
                        (0,0,1), (2,0,2), (5,0,9), (7,0,8)]

    if instructions == 'medium':
        instructions = [(0,8,6), (1,8,4), (3,8,9),
                        (5,7,1), (6,7,3),
                        (8,6,2),
                        (1,5,3), (6,5,9), (8,5,6),
                        (0,4,1), (6,4,7), (7,4,5),
                        (1,3,2), (4,3,8), (5,3,5), (8,3,1),
                        (5,2,8),
                        (7,1,9), (8,1,7),
                        (0,0,2), (1,0,7), (2,0,9), (7,0,6),(8,0,4)]

    if instructions == 'hard':
        instructions = [(0,8,5), (6,8,4), (7,8,2),
                        (3,7,6), (5,7,7), (7,7,1),
                        (8,6,3),
                        (2,5,4), (5,5,2), (8,5,8),
                        (4,4,7), (5,4,9),
                        (1,3,1), (3,3,5),
                        (3,2,3), (4,2,4), (6,2,8),
                        (1,1,5), (2,1,1), (4,1,2),
                        (1,0,7), (8,0,6)]

    #(x, y, number)
    for instruction in instructions:
        x, y, num = instruction
        new_boardstate[x][y] = [num, 'PUZZLE']

    return new_boardstate

def counter(boxes, focus = 1):
    tracker = [0 for i in range(9)]

    for box in boxes:
        for val in box:
            if type(val) != str: tracker[val-1] += 1

    valid = [k+1 for k in range(9) if tracker[k] == focus]

    if valid == [1,2,3,4,5,6,7,8,9]: valid = []

    return valid

def xwing(boardstate):
    pass
    #TO-DO

    #https://www.learn-sudoku.com/x-wing.html

def swordfish(boardstate):
    pass
    #TO-DO

    #https://www.learn-sudoku.com/swordfish.html

    #536*

    #53      54
                            #you can remove *
    #        52      52

    #54              53

    #549*    145*    539*

def unique_rectangle(boardstate):
    pass
    #TO-DO

    #https://www.learn-sudoku.com/unique-rectangle.html

    #53     537
                 #you can remove 53 from 537
    #53     53

def naked_pair(boardstate):
    """
    Find a pair of possibilities (ex: [5, 9], [5, 9]) in a row --> those numbers have to be in
    that location, so you can clear all hrow, vrow, and box alternatives
    """
    new_boardstate = boardstate


    for hiddens in range(2,10):

        #vertical
        for i in range(9):
            positions = [[i,j] for j in range(9) if len(new_boardstate[i][j]) == hiddens+1]
            values = [new_boardstate[i][j] for j in range(9) if len(new_boardstate[i][j]) == hiddens+1]

            pair_loc = []
            for p in range(len(values)):
                temp = [p]
                for q in range(p+1, len(values)):
                    if (values[p] == values[q]) * (positions[p] != positions[q]): temp.append(q)

                if (sorted(temp) not in pair_loc) * (len(temp) == hiddens): pair_loc.append(temp)



            for k in range(len(pair_loc)):
                posits1, posits2, vals = [positions[pair_loc[k][i]][0] for i in range(hiddens)], [positions[pair_loc[k][i]][1] for i in range(hiddens)], values[pair_loc[k][0]]

                for val in vals:

                    if type(val) == str: continue

                    for i in posits1:
                        for j in range(9):
                            if (len(new_boardstate[i][j]) > 2) * (val in new_boardstate[i][j]) * (j not in posits2):
                                for flan in new_boardstate[i][j]:
                                    if flan == val: new_boardstate[i][j].remove(flan)

        #horizontal
        for j in range(9):
            positions = [[i,j] for i in range(9) if len(new_boardstate[i][j]) == hiddens+1]
            values = [new_boardstate[i][j] for i in range(9) if len(new_boardstate[i][j]) == hiddens+1]

            pair_loc = []
            for p in range(len(values)):
                temp = [p]
                for q in range(p+1, len(values)):
                    if (values[p] == values[q]) * (positions[p] != positions[q]): temp.append(q)

                if (sorted(temp) not in pair_loc) * (len(temp) == hiddens): pair_loc.append(temp)


            for k in range(len(pair_loc)):
                posits1, posits2, vals = [positions[pair_loc[k][i]][0] for i in range(hiddens)], [positions[pair_loc[k][i]][1] for i in range(hiddens)], values[pair_loc[k][0]]

                for val in vals:

                    if type(val) == str: continue

                    for j in posits2:
                        for i in range(9):
                            if (len(new_boardstate[i][j]) > 2) * (val in new_boardstate[i][j]) * (i not in posits1):
                                for flan in new_boardstate[i][j]:
                                    if flan == val: new_boardstate[i][j].remove(flan)

        #in box
        for box_n in range(9):

            if box_n in [2,5,8]: vcor = 6
            elif box_n in [1,4,7]: vcor = 3
            else: vcor = 0

            if box_n in [6,7,8]: hcor = 6
            elif box_n in [3,4,5]: hcor = 3
            else: hcor = 0

            positions, values = [], []
            for i in range(hcor, hcor+3):
                for j in range(vcor, vcor+3):
                    if len(new_boardstate[i][j]) == hiddens+1:
                        positions.append([i,j])
                        values.append(new_boardstate[i][j])

            pair_loc = []
            for p in range(len(values)):
                temp = [p]
                for q in range(p+1, len(values)):
                    if (values[p] == values[q]) * (positions[p] != positions[q]): temp.append(q)

                if (sorted(temp) not in pair_loc) * (len(temp) == hiddens): pair_loc.append(temp)


            for k in range(len(pair_loc)):

                posits, vals = [positions[pair_loc[k][i]] for i in range(hiddens)], values[pair_loc[k][0]]

                for val in vals:

                    if type(val) == str: continue

                    for i in range(hcor, hcor+3):
                        for j in range(vcor, vcor+3):
                            if (len(new_boardstate[i][j]) > 2) * (val in new_boardstate[i][j]) * ([i,j] not in posits):
                                for flan in new_boardstate[i][j]:
                                    if flan == val: new_boardstate[i][j].remove(flan)



    return new_boardstate

def check_singular(boardstate):


    new_boardstate = boardstate

    for i in range(9):
        vrow = new_boardstate[i][:]

        valid = counter(vrow)
        for val in valid:
            for m in range(9):
                if (len(new_boardstate[i][m]) > 2) * (val in new_boardstate[i][m]):
                    for flan in new_boardstate[i][m]:
                        if (flan != val)*(type(flan) != str):
                            new_boardstate[i][m].remove(flan)

    for k in range(9):
        hrow = [new_boardstate[i][k] for i in range(9)]

        valid = counter(hrow)
        for val in valid:
            for i in range(9):
                if (len(new_boardstate[i][k]) > 2) * (val in new_boardstate[i][k]):
                    for flan in new_boardstate[i][k]:
                        if (flan != val)*(type(flan) != str):
                            new_boardstate[i][k].remove(flan)


    for box_n in range(9):

        if box_n in [2,5,8]: vcor = 6
        elif box_n in [1,4,7]: vcor = 3
        else: vcor = 0

        if box_n in [6,7,8]: hcor = 6
        elif box_n in [3,4,5]: hcor = 3
        else: hcor = 0

        box = []
        for i in range(hcor, hcor+3):
            for j in range(vcor, vcor+3):
                box.append(new_boardstate[i][j])

        valid = counter(box)
        for val in valid:
            for i in range(hcor, hcor+3):
                for j in range(vcor, vcor+3):
                    if (len(new_boardstate[i][j]) > 2) * (val in new_boardstate[i][j]):
                        for flan in new_boardstate[i][j]:
                            if (flan != val)*(type(flan) != str):
                                new_boardstate[i][j].remove(flan)




    return new_boardstate

def check_vertical(boardstate):

    new_boardstate = boardstate

    for i in range(9):
        vrow = new_boardstate[i][:]

        singles = [square[0] for square in vrow if len(square) == 2]

        for val in singles:
            for j in range(9):
                if (len(new_boardstate[i][j]) > 2)*(val in new_boardstate[i][j]):
                    new_boardstate[i][j].remove(val)


    return new_boardstate

def check_horizontal(boardstate):

    new_boardstate = boardstate


    for k in range(9):
        hrow = [new_boardstate[i][k] for i in range(9)]
        singles = [square[0] for square in hrow if len(square) == 2]

        for val in singles:
            for i in range(9):
                if (len(new_boardstate[i][k]) > 2)*(val in new_boardstate[i][k]):
                    new_boardstate[i][k].remove(val)

    return new_boardstate

def check_box(boardstate):

    new_boardstate = boardstate

    for box_n in range(9):

        if box_n in [2,5,8]: vcor = 6
        elif box_n in [1,4,7]: vcor = 3
        else: vcor = 0

        if box_n in [6,7,8]: hcor = 6
        elif box_n in [3,4,5]: hcor = 3
        else: hcor = 0

        singles = []
        for i in range(hcor, hcor+3):
            for j in range(vcor, vcor+3):
                if len(new_boardstate[i][j]) == 2:
                    singles.append(new_boardstate[i][j][0])

        for val in singles:
            for i in range(hcor, hcor+3):
                for j in range(vcor, vcor+3):
                    if (len(new_boardstate[i][j]) > 2)*(val in new_boardstate[i][j]):
                        new_boardstate[i][j].remove(val)



    return new_boardstate

def animate(directory, files, output_fname):

    fp_out = os.path.join(directory, "{}.gif".format(output_fname))

    img, *imgs = [Image.open(file) for file in files]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
             save_all=True, duration=len(files)*70, loop=0)

    for file in files: os.remove(file)

def frame(boardstate, directory, frame_num):

    fig, ax = plt.subplots(facecolor = 'papayawhip')

    ax.axis('equal')
    ax.axis('off')

    #grid
    ax.vlines(x = [p-0.5 for p in range(0,10,3)], ymin = [-0.5 for k in range(0,10,3)], ymax = [8.5 for k in range(0,10,3)], colors = 'saddlebrown', linewidth = 3)
    ax.hlines(y = [p-0.5 for p in range(0,10,3)], xmin = [-0.5 for k in range(0,10,3)], xmax = [8.5 for k in range(0,10,3)], colors = 'saddlebrown', linewidth = 3)
    ax.vlines(x = [p-0.5 for p in [1,2,4,5,7,8]], ymin = [-0.5 for k in [1,2,4,5,7,8]], ymax = [8.5 for k in [1,2,4,5,7,8]], colors = 'saddlebrown', linewidth = 1)
    ax.hlines(y = [p-0.5 for p in [1,2,4,5,7,8]], xmin = [-0.5 for k in [1,2,4,5,7,8]], xmax = [8.5 for k in [1,2,4,5,7,8]], colors = 'saddlebrown', linewidth = 1)

    #decoration :)
    ax.text(-3, -0.25, 'S\nU\nD\nO\nK\nU', size = 30)
    ax.text(10, -0.25, 'S\nO\nL\nV\nE\nR', size = 30)

    for i in range(9):
        for j in range(9):
            if len(boardstate[i][j]) == 2:
                if boardstate[i][j][1] == 'PUZZLE': ax.text(i-0.25, j-0.3, '{}'.format(boardstate[i][j][0]), size = 18, color = 'mediumblue')
                elif boardstate[i][j][1] == 'SOLVE': ax.text(i-0.25, j-0.3, '{}'.format(boardstate[i][j][0]), size = 18, color = 'black')
                else: print('PLOT TYPE ERROR at x: {}, y: {}.'.format(i,j))
            elif len(boardstate[i][j]) < 2: print('SHORT ERROR at x: {}, y: {}.'.format(i,j))
            else:
                formatted = boardstate[i][j][::-1][1:][::-1]
                outstr, c = '', 0
                for nums in [formatted[:3],formatted[3:6],formatted[6:]]:
                    if nums == []: continue
                    if c == 1: outstr += '\n'
                    string = '{}'.format(nums).replace(' ', '').replace('[', '').replace(']', '').replace(',','')
                    outstr += string
                    c+=1
                ax.text(i-0.4, j-c/5, outstr, size = 8, color = 'black')


    filepath = os.path.join(directory,'{}.png'.format(frame_num))
    plt.savefig(filepath)
    plt.close('all')

    return filepath

def equal(state1, state2):
    eq = True

    for s1, s2 in zip(state1, state2):
        for i,j in zip(s1,s2):
            if i != j:
                eq = False
                break
    return eq

def main():
    #boardstate [i][row] get column
    #boardstate[col][j] get row
    #bottom left is [0][0]       bottom right is [8][0]
    #top right is [8][8]         top left is [0][8]
    boardstate = [[ [k if k < 10 else 'SOLVE' for k in range(1,11)] for j in range(9)] for i in range(9)]

    boardstate = set_board(boardstate, 'hard')

    files, directory = [], 'wz'

    solved, q = False, 0
    files.append(frame(boardstate, directory, q))
    while not solved:


        prev_boardstate1 = copy.deepcopy(boardstate)

        boardstate = check_horizontal(boardstate)
        boardstate = check_vertical(boardstate)
        boardstate = check_box(boardstate)


        if not equal(prev_boardstate1, boardstate):
            q+=1
            files.append(frame(boardstate, directory, '{}_checks'.format(q)))

            """print('Checks', q)
            for k in range(9)[::-1]:
                hrow = [boardstate[i][k] for i in range(9)]
                print(k, hrow)
            print('\n')"""

        prev_boardstate2 = copy.deepcopy(boardstate)
        boardstate = check_singular(boardstate)
        if not equal(prev_boardstate2, boardstate):
            q+=1
            files.append(frame(boardstate, directory, '{}_singular'.format(q)))

            """print('Singular', q)
            for k in range(9)[::-1]:
                hrow = [boardstate[i][k] for i in range(9)]
                print(k, hrow)
            print('\n')"""

        prev_boardstate3 = copy.deepcopy(boardstate)
        boardstate = naked_pair(boardstate)
        if not equal(prev_boardstate3, boardstate):
            q+=1
            files.append(frame(boardstate, directory, '{}_pair'.format(q)))

            """print('Pairs', q)
            for k in range(9)[::-1]:
                hrow = [boardstate[i][k] for i in range(9)]
                print(k, hrow)
            print('\n')"""


        if equal(prev_boardstate1, boardstate): solved = True

    q+=1
    files.append(frame(boardstate, directory, q))

    for k in range(9)[::-1]:
        hrow = [boardstate[i][k] for i in range(9)]
        print(k+1, hrow)


    animate(directory, files, 'HARD')

if __name__ == '__main__':
    main()
