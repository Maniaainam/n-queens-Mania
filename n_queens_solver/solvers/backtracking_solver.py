class BacktrackingSolver:
    def __init__(self, n):
        self.n = n
        self.solutions = []

    def is_safe(self, board, row, col):
 
        for i in range(col):
            if board[row][i] == 1:
                return False

 
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False


        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False

        return True

    def solve_util(self, board, col):
        if col >= self.n:
            solution = []
            for i in range(self.n):
                for j in range(self.n):
                    if board[i][j] == 1:
                        solution.append(i)  
            self.solutions.append(solution)
            return True

        res = False
        for i in range(self.n):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                res = self.solve_util(board, col + 1) or res
                board[i][col] = 0  
        return res

    def solve(self):
        board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solutions = []
        found = self.solve_util(board, 0)
        if found and self.solutions:
            return self.solutions[0]  
        return None