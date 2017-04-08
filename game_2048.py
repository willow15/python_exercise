import time
import random

class game_2048():

    def __init__(self):
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],]
        random.seed(a = time.mktime(time.localtime()))
        index1 = random.randint(0, 15)
        index2 = random.randint(0, 15)
        while index1 == index2:
            index2 = random.randint(0, 15)
        self.matrix[index1 / 4][index1 % 4] = 2
        self.matrix[index2 / 4][index2 % 4] = 2

    def insert_two(self):
        zero_index_list = list()
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    zero_index_list.append((i, j))

        i, j = random.choice(zero_index_list)
        self.matrix[i][j] = 2

    def print_matrix(self):
        for row in self.matrix:
            print row

    def move_left(self):
        for row in self.matrix:
            # move nonzero numbers to left
            nonzero_list = list()
            for i in range(4):
                if row[i] != 0:
                    nonzero_list.append(row[i])
            for i in range(len(nonzero_list)):
                row[i] = nonzero_list[i]
            if len(nonzero_list) < 4:
                for i in range(len(nonzero_list), 4, 1):
                    row[i] = 0

            # calculate
            for i in range(3):
                if row[i] == row[i + 1]:
                    row[i] += row[i + 1]
                    for j in range(i + 1, 3, 1):
                        row[j] = row[j + 1]
                    row[3] = 0



    def move_right(self):
        # reverse
        for row in self.matrix:
            row.reverse()
        # calculate by move_left function
        self.move_left()
        # reverse back
        for row in self.matrix:
            row.reverse()

    def move_up(self):
        # transpose
        transposed_matrix = [[row[i] for row in self.matrix] for i in range(4)]
        self.matrix = transposed_matrix
        # calculate by move_left function
        self.move_left()
        # transpose back
        transposed_matrix = [[row[i] for row in self.matrix] for i in range(4)]
        self.matrix = transposed_matrix

    def move_down(self):
        # transpose
        transposed_matrix = [[row[i] for row in self.matrix] for i in range(4)]
        self.matrix = transposed_matrix
        # calculate by move_right function
        self.move_right()
        # transpose back
        transposed_matrix = [[row[i] for row in self.matrix] for i in range(4)]
        self.matrix = transposed_matrix

    def is_not_end(self):
        for row in self.matrix:
            if row.count(0) > 0:
                return True

        for row in self.matrix:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return True

        transposed_matrix = zip(*self.matrix)
        for row in transposed_matrix:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return True

        return False



if __name__ == '__main__':
    new_game = game_2048()
    new_game.print_matrix()

    while new_game.is_not_end():
        
        option = raw_input("please choose 'left' or 'right' or 'up' or 'down' or 'quit':")
        if option in ['left', 'l']:
            new_game.move_left()
        elif option in ['right', 'r']:
            new_game.move_right()
        elif option in ['up', 'u']:
            new_game.move_up()
        elif option in ['down', 'd']:
            new_game.move_down()
        elif option in ['quit', 'q']:
            exit()
        else:
            continue

        new_game.insert_two()
        new_game.print_matrix()

    print "game is end!"
