import os

# find file in folder structure
input_file_path = "/Users/emanuelalexandi/PycharmProjects/DataWranglingSandbox/InputData/Day4Input.txt"


# read bingo boards from input file
with open(input_file_path) as file:
    list_of_rows = []
    for index, line in enumerate(file):
        # skip first two lines
        if index > 1:
            if line != "\n":
                line = line.replace("\n", "")
                row = line.split(" ")       #split line, which is a string, and create a list containing the elements
                while("" in row):
                    # remove empty strings which are generated because sometimes there are two spaces between two numbers
                    row.remove("")
                list_of_rows.append(row)



def divide_chunks(list, n):
    # Split 5-sized chunks from list_of_rows to get a list of boards (which are 5x5)
    for i in range(0, len(list), n):
        yield list[i:i + n]


list_of_boards = list(divide_chunks(list_of_rows, 5))
list_of_boards_initial= [[[i for i in row] for row in board] for board in list_of_boards]      # save the initial state of list_of_boards in an extra list


def mark_number_as_drawn(str_number, list):
    # function to drop drawn numbers from all boards until a board is empty
    for board in list:
        for row in board:
            for index, num in enumerate(row):
                if num == str_number:
                    row[index] = "drawn"


def check_for_winner(list):
    # function to check for the first board to have an empty row or column
    for index, board in enumerate(list):
        # check for an empty row
        for row in board:
            if all(value == "drawn" for value in row):
                # print(row)
                return index
            else:
                # print(row)
                pass
        # transform columns into lists and check for an empty column
        transformed_board = []
        number_of_columns = 5
        for column_index in range(number_of_columns):
            column = []
            for row_index, row in enumerate(board):
                column.append(row[column_index])
            transformed_board.append(column)
            for column in transformed_board:
                if all(value == "drawn" for value in column):
                    return index
                else:
                    pass




# read drawing order from input file, drop numbers and check for winners sequentially
file = open(input_file_path, "r")
drawing_order = file.readline().strip("\n").split(",")
for str_number in drawing_order:
    mark_number_as_drawn(str_number, list_of_boards)
    winner = check_for_winner(list_of_boards)
    if winner != None:
        # save last drawn winning number for final calculation of score
        winning_number = int(str_number)
        break

# get sums of all unmarked numbers for winner
winning_board = list_of_boards[winner]
for row in winning_board:
    while("drawn" in row):
        row.remove("drawn")
flattened_winning_board = [int(cell) for row in winning_board for cell in row]
sum_of_unmarked_numbers = sum(flattened_winning_board)

# calculate score for winner
score = sum_of_unmarked_numbers * winning_number
print(score)





# PART 2 - find the board that wins last


def check_for_all_winners(list):
    all_winners_list = []
    # function to check for the boards which have a completely drawn row or column
    for index, board in enumerate(list):
        winning_board_by_row_found = False
        # check for a drawn row
        for row in board:
            if all(value == "drawn" for value in row):
                all_winners_list.append(index)
                winning_board_by_row_found = True
                break
            else:
                pass
        if winning_board_by_row_found: pass
        else:
            # transform columns into lists and check for a winning column in the current board
            transformed_board = []
            number_of_columns = 5
            winning_board_by_column_found = False
            for column_index in range(number_of_columns):
                column = []
                for row_index, row in enumerate(board):
                    column.append(row[column_index])
                transformed_board.append(column)
                for column in transformed_board:
                    if all(value == "drawn" for value in column):
                        all_winners_list.append(index)
                        winning_board_by_column_found = True
                        break
                    else:
                        pass
                if winning_board_by_column_found: break
    return all_winners_list



#re-initialize list_of_boards
list_of_boards = list_of_boards_initial


# check for last winner
counter = 0
for str_number in drawing_order:
    current_list_of_winners = []
    mark_number_as_drawn(str_number, list_of_boards)
    counter += 1
    current_list_of_winners = check_for_all_winners(list_of_boards)
    if len(current_list_of_winners) == 99:       # find last board that is not a winner
        for i in range(0, 100):
            if i in current_list_of_winners:
                pass
            else:
                last_winner = i
    if len(current_list_of_winners) == 100:     # find last number for the last board to win
        last_winning_number = int(drawing_order[counter-1])
        break



# get sums of all unmarked numbers for last_winner
last_winning_board = list_of_boards[last_winner]
for row in last_winning_board:
    while("drawn" in row):
        row.remove("drawn")
flattened_last_winning_board = [int(cell) for row in last_winning_board for cell in row]
sum_of_unmarked_numbers = sum(flattened_last_winning_board)

# calculate score for last_winner
score = sum_of_unmarked_numbers * last_winning_number
print(score)

