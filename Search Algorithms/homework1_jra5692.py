


############################################################
# Imports
############################################################


import random
import collections


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    return n ** (n * n)

def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    i = 0
    j = 0
    while i < len(board):
        j = i + 1
        while j < len(board):
            if board[j] == board[i]:
                return False
            if abs(board[j] - board[i]) == abs(j - i):
                return False
            j += 1
        i += 1
    return True

def n_queens_helper(n, board):
    #if we have a valid board send it back
    if n == len(board) and n_queens_valid(board):
        yield board

    #attempt to place a queen in every column
    for col in range(0, n):

        helperBoard = board[:]
        helperBoard.append(col)

        #recursively call this function with all of the valid boards
        if (n_queens_valid(helperBoard)):
            for validBoard in n_queens_helper(n, helperBoard):
                yield validBoard
    
#call the helper function and yield all results
def n_queens_solutions(n):
    for validBoard in n_queens_helper(n, []):
        yield validBoard


############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if row < len(self.board) and row >= 0 and col < len(self.board[0]) and col >= 0:
            self.board[row][col] = not self.board[row][col]
            if row > 0:
                self.board[row - 1][col] = not self.board[row - 1][col]
            if col > 0:
                self.board[row][col - 1] = not self.board[row][col - 1]
            if row + 1 < len(self.board):
                self.board[row + 1][col] = not self.board[row + 1][col]
            if col + 1 < len(self.board[0]):
                self.board[row][col + 1] = not self.board[row][col + 1]

    def scramble(self):
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in self.board:
            for col in row:
                if col:
                    return False
        return True

    def copy(self):
        lst = []
        for row in self.board:
            helperLst = []
            for col in row:
                helperLst.append(col)
            lst.append(helperLst)
        return LightsOutPuzzle(lst)

    def successors(self):
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                lst = self.copy()
                lst.perform_move(row, col)
                yield ((row, col), lst.board)


    def find_solution(self):
        #create queue
        queue = collections.deque([(self.get_board(), [])])

        #create set so we can not go over the same board state
        #tried to make self.board tuple like in the disk problems beneath but converting self.board to tuple wasn't working but str was (not sure why)
        trimNodes = set()
        trimNodes.add(str(self.get_board()))

        while queue:
            #get the queue using fifo queue
            data = queue.popleft()

            #assign the data
            currentState = data[0]
            stateTransitions = data[1]

            self.board = currentState

            #if the board is solved then return the state transitions
            if self.is_solved():
                return stateTransitions
            
            #get all successors and loop over them
            for successorData in self.successors():
                stateTransition = successorData[0]
                successor = successorData[1]

                #pass if successor state is in trimNodes
                if str(successor) in trimNodes:
                    pass
                else:
                    moveArr = stateTransitions + [stateTransition]
                    trimNodes.add(str(successor))
                    queue.append((successor, moveArr))
        return None

def create_puzzle(rows, cols):
    lst = []
    for i in range(0, rows):
        helperLst = []
        for j in range(0, cols):
            helperLst.append(False)
        lst.append(helperLst)
    return LightsOutPuzzle(lst)


############################################################
# Section 3: Linear Disk Movement
############################################################

#helper function for identical disks
def getAllMoves(row):
    i = 0
    while i < len(row):
        if i + 1 < len(row) and row[i] == 1 and row[i + 1] == 0:
            yield (i, i + 1)
        if i - 1 >= 0 and row[i] == 1 and row[i - 1] == 0:
            yield(i, i - 1)
        if i + 2 < len(row) and row[i] == 1 and row[i + 2] == 0 and row[i + 1] == 1:
            yield (i, i + 2)
        if i - 2 >= 0 and row[i] == 1 and row[i - 2] == 0 and row[i - 1] == 1:
            yield(i, i - 2)
        i += 1

#helper function for identical disks
def checkDone(row, n):
    length = len(row)
    for i in range(length - n, length):
        if row[i] == 0:
            return False
    for i in range(0, length - n):
        if row[i] == 1:
            return False
    return True

def solve_identical_disks(length, n):
    if n == 0 or n == length:
        return []

    #create row of disks = 1 and empty = 0
    row = [1] * n + [0] * (length - n)

    #create set of states that we don't want to repeat
    trimNodes = set()
    trimNodes.add(tuple(row))

    #create queue of state and moves
    queue = collections.deque([(row, [])])

    while queue:

        #get the queue data with fifo
        data = queue.popleft()
        currentRow = data[0]
        stateTransitions = data[1]

        #check if the row is done using the helper function
        if checkDone(currentRow, n):
            return stateTransitions

        #check for all state transitions and then append to the queue if not in the trimNodes
        for stateTransition in getAllMoves(currentRow):
            newRow = currentRow[:]

            move1 = stateTransition[0]
            move2 = stateTransition[1]

            tempMove = newRow[move1]

            newRow[move1] = newRow[move2]
            newRow[move2] = tempMove

            if tuple(newRow) in trimNodes:
                pass
            else:
                trimNodes.add(tuple(newRow))
                queue.append((newRow, stateTransitions + [stateTransition]))
    return None

#helper function for distinct disks
def checkDoneDistinct(row, n):
    counter = n
    length = len(row)

    for i in range(length - n, length):
        if row[i] != counter:
            return False
        counter -= 1
    for i in range(0, length - n):
        if row[i] != 0:
            return False
    return True

#helper function for distinct disks
def getAllMovesDistinct(row):
    i = 0
    while i < len(row):
        if i + 1 < len(row) and row[i] != 0 and row[i + 1] == 0:
            yield (i, i + 1)
        if i - 1 >= 0 and row[i] != 0 and row[i - 1] == 0:
            yield(i, i - 1)
        if i + 2 < len(row) and row[i] != 0 and row[i + 2] == 0 and row[i + 1] != 0:
            yield (i, i + 2)
        if i - 2 >= 0 and row[i] != 0 and row[i - 2] == 0 and row[i - 1] != 0:
            yield(i, i - 2)
        i += 1


def solve_distinct_disks(length, n):
    if n == 0 or n == length:
        return []
    

    #setup the row with the lowest ones being 1, ..., n-1, 0, ..., 0
    row = [0] * length
    for i in range(0, n):
        row[i] = i + 1

    #setup states to not repeat
    trimNodes = set()
    trimNodes.add(tuple(row))

    #setup queue with fifo
    queue = collections.deque([(row, [])])

    while queue:
        #get data from the queue
        data = queue.popleft()
        currentRow = data[0]
        stateTransitions = data[1]

        #if done return the state transitions to get done
        if checkDoneDistinct(currentRow, n):
            return stateTransitions

        #check for all possible state transitions and append to queue if it's not a repeat state
        for stateTransition in getAllMovesDistinct(currentRow):
            newRow = currentRow[:]

            move1 = stateTransition[0]
            move2 = stateTransition[1]

            tempMove = newRow[move1]

            newRow[move1] = newRow[move2]
            newRow[move2] = tempMove

            if tuple(newRow) in trimNodes:
                pass
            else:
                trimNodes.add(tuple(newRow))
                queue.append((newRow, stateTransitions + [stateTransition]))
    return None

