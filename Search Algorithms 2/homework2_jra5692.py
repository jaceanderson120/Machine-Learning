
############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import queue


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    returnLst = []
    length = 1
    for i in range(rows):
        helperLst = []
        for j in range(cols):
            helperLst.append(length)
            length += 1
        returnLst.append(helperLst)
    returnLst[rows - 1][cols - 1] = 0
    return TilePuzzle(returnLst)



class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if not (direction in ["up", "down", "left", "right"]):
            return False
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    if direction == "up":
                        if i > 0:
                            self.board[i][j], self.board[i - 1][j] = self.board[i - 1][j], self.board[i][j]
                            return True
                        return False
                    elif direction == "down":
                        if i < (len(self.board) - 1):
                            self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
                            return True
                        return False
                    elif direction == "right":
                        if j < (len(self.board[i]) - 1):
                            self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
                            return True
                        return False
                    elif direction == "left":
                        if j > 0:
                            self.board[i][j], self.board[i][j - 1] = self.board[i][j - 1], self.board[i][j]
                            return True
                        return False
        return False

    def scramble(self, num_moves):
        for i in range(num_moves):
            self.perform_move(random.choice(["up", "down", "left", "right"]))

    def is_solved(self):
        counter = 1
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if counter != self.board[i][j]:
                    if i == len(self.board) - 1 and j == len(self.board[i]) - 1 and self.board[i][j] == 0:
                        return True
                    return False
                counter += 1
        return True

    def copy(self):
        board = self.board
        returnLst = []
        for i in range(len(board)):
            lst = []
            for j in range(len(board[i])):
                lst.append(board[i][j])
            returnLst.append(lst)
        return TilePuzzle(returnLst)

    def successors(self):
        returnArray = []
        for i in ["up", "down", "left", "right"]:
            new_board = self.copy()
            if new_board.perform_move(i):
                returnArray.append((i, new_board))
        return returnArray

    def find_solutions_iddfs(self):
        counter = 0
        finished = False
        while not finished:
            for moves in self.iddfs_helper(counter, [], self):
                yield moves
                finished = True
            counter += 1
        return
            


    def iddfs_helper(self, limit, moves, board):
        if (limit == 0):
            if board.is_solved():
                yield moves
            return
        for move, new_board in board.successors():
            new_moves = moves + [move]
            if (new_board.is_solved()):
                yield new_moves
            else:
                yield from self.iddfs_helper(limit - 1, new_moves, new_board)

    def getManhattan(self, board):
        manhattan = 0
        counter = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if not (board[i][j] == counter) and board[i][j] != 0:
                    currNum = board[i][j]
                    row = abs((currNum // len(board[i])) - i)
                    col = abs((currNum % len(board[i])) - j)
                    manhattan += (row + col)
                counter += 1
        return manhattan
    
    def listToTuple(self, board):
        return tuple(tuple (lst) for lst in board)

    def find_solution_a_star(self):
        priorityQueue = queue.PriorityQueue()
        priorityQueue.put((self.getManhattan(self.board), [], self.board))
        visited = {}
        visited[self.listToTuple(self.board)] = self.getManhattan(self.board)

        while not (priorityQueue.empty()):
            data = priorityQueue.get()
            moves = data[1]
            board = data[2]
            self.board = board
            
            if self.is_solved():
                return moves
            for move, currentBoard in self.successors():
                if self.listToTuple(currentBoard.get_board()) in visited:
                    manhattan = self.getManhattan(currentBoard.get_board()) + len(moves) + 1
                    if manhattan < visited[self.listToTuple(currentBoard.get_board())]:
                        visited[self.listToTuple(currentBoard.get_board())] = manhattan
                        priorityQueue.put((manhattan + len(moves) + 1, moves + [move], currentBoard.get_board()))
                else:
                    visited[self.listToTuple(currentBoard.get_board())] = self.getManhattan(currentBoard.get_board())
                    priorityQueue.put((self.getManhattan(currentBoard.get_board()) + len(moves) + 1, moves + [move], currentBoard.get_board()))
        return None


############################################################
# Section 2: Grid Navigation
############################################################

def getAllMoves(path, scene):
    row = path[0]
    col = path[1]
    returnLst = []
    if row < len(scene) - 1:
        if not scene[row + 1][col]:
            returnLst.append((row + 1, col))
    if row > 0:
        if not scene[row - 1][col]:
            returnLst.append((row - 1, col))
    if col > 0:
        if not scene[row][col - 1]:
            returnLst.append((row, col - 1))
    if col < len(scene[0]) - 1:
        if not scene[row][col + 1]:
            returnLst.append((row, col + 1))
    if col > 0 and row > 0:
        if not scene[row - 1][col - 1]:
            returnLst.append((row - 1, col - 1))
    if col > 0 and row < len(scene) - 1:
        if not scene[row + 1][col - 1]:
            returnLst.append((row + 1, col - 1))
    if row > 0 and col < len(scene[0]) - 1:
        if not scene[row - 1][col + 1]:
            returnLst.append((row - 1, col + 1))
    if row < len(scene) - 1 and col < len(scene[0]) - 1:
        if not scene[row + 1][col + 1]:
            returnLst.append((row + 1, col + 1))
    return returnLst

def getManhattan(path, goal):
    row = abs(path[0] - goal[0])
    col = abs(path[1] - goal[1])
    return max(row, col)

def find_path(start, goal, scene):
    if (start == goal):
        return []
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((getManhattan(start, goal), [start], start))
    visited = {}
    visited[start] = getManhattan(start, goal)
    while not priorityQueue.empty():
        data = priorityQueue.get()
        moves = data[1]
        path = data[2]

        if path == goal:
            return moves
        else:
            for new_path in getAllMoves(path, scene):
                if new_path in visited:
                    value = getManhattan(new_path, goal) + len(moves) + 1
                    if value < visited[new_path]:
                        visited[new_path] = value
                        priorityQueue.put((value, moves + [new_path], new_path))
                else:
                    visited[new_path] = getManhattan(new_path, goal) + len(moves) + 1
                    priorityQueue.put((getManhattan(new_path, goal) + len(moves) + 1, moves + [new_path], new_path))
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def createDisk(length, n):
    row = [0] * length
    for i in range(0, n):
        row[i] = i + 1
    return row

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

def manhattan(row, n, length):
    manhattanNum = 0
    for i in range(len(row)):
        if row[i] != 0:
            num = row[i]
            index = length - 1 - (n - num)
            manhattanNum += abs(i - index)
    return manhattanNum

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
    
    row = createDisk(length, n)

    priorityQueue = queue.PriorityQueue()
    visited = {}
    priorityQueue.put((manhattan(row, n, length), [], row))
    visited[tuple(row)] = manhattan(row, n, length)

    while not priorityQueue.empty():
        data = priorityQueue.get()
        moves = data[1]
        currentRow = data[2]

        if checkDoneDistinct(currentRow, n):
            print(currentRow)
            return moves
        else:
            for move in getAllMovesDistinct(currentRow):
                newRow = currentRow[:]

                move1 = move[0]
                move2 = move[1]
                tempMove = newRow[move1]

                newRow[move1] = newRow[move2]
                newRow[move2] = tempMove

                if (tuple(newRow) in visited):
                    cost = manhattan(newRow, n, length) + len(moves) + 1
                    if visited[tuple(newRow)] > cost:
                        visited[tuple(newRow)] = cost
                        priorityQueue.put((cost, moves + [move], newRow))
                else:
                    cost = manhattan(newRow, n, length) + len(moves) + 1
                    visited[tuple(newRow)] = cost
                    priorityQueue.put((cost, moves + [move], newRow))
    return None


############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    returnLst = []
    for i in range(rows):
        helperLst = []
        for j in range(cols):
            helperLst.append(False)
        returnLst.append(helperLst)
    return DominoesGame(returnLst)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]:
                    self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if not self.board[row][col] and len(self.board) > row + 1 and not self.board[row + 1][col]:
                return True
        else:
            if not self.board[row][col] and len(self.board[row]) > col + 1 and not self.board[row][col + 1]:
                return True
        return False

    def legal_moves(self, vertical):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        if vertical:
            self.board[row][col] = True
            self.board[row + 1][col] = True
        else:
            self.board[row][col] = True
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        else:
            return False

    def copy(self):
        returnLst = []
        for i in range(len(self.board)):
            helperLst = []
            for j in range(len(self.board[i])):
                helperLst.append(self.board[i][j])
            returnLst.append(helperLst)
        return DominoesGame(returnLst)

    def successors(self, vertical):
        returnLst = []
        for move in self.legal_moves(vertical):
            new_board = self.copy()
            new_board.perform_move(move[0], move[1], vertical)
            returnLst.append((move, new_board))
        return returnLst

    def get_random_move(self, vertical):
        pass

    def getScore(self, vertical, board):
        if vertical:
            return len(list(board.legal_moves(vertical))) - len(list(board.legal_moves(not vertical)))
        else:
            return len(list(board.legal_moves(not vertical))) - len(list(board.legal_moves(vertical)))

    def miniMax(self, vertical, limit, leaf_nodes, board, alpha, beta):
        if limit == 0 or board.game_over(vertical):
            leaf_nodes[0] += 1
            return self.getScore(vertical, board)

        if vertical:
            maxVal = float('-inf')
            for response in board.successors(vertical):
                new_board = response[1]
                score = self.miniMax(not vertical, limit - 1, leaf_nodes, new_board, alpha, beta)
                maxVal = max(maxVal, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return maxVal
        else:
            minVal = float('inf')
            for response in board.successors(vertical):
                new_board = response[1]
                score = self.miniMax(not vertical, limit - 1, leaf_nodes, new_board, alpha, beta)
                minVal = min(minVal, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return minVal

    def get_best_move(self, vertical, limit):
        bestMove = None
        if vertical:
            highestVal = float('-inf')
        else:
            highestVal = float('inf')


        alpha = float('-inf')
        beta = float('inf')

        leaf_nodes = [0]


        for move, new_board in self.successors(vertical):
            value = self.miniMax(not vertical, limit - 1, leaf_nodes, new_board, alpha, beta)

            if vertical:
                if value > highestVal:
                    highestVal = value
                    bestMove = move
                alpha = max(alpha, value)
            else:
                if value < highestVal:
                    highestVal = value
                    bestMove = move
                beta = min(beta, value)

            if beta <= alpha:
                break

        if vertical == False:
            highestVal *= -1

        return (bestMove, highestVal, leaf_nodes[0])