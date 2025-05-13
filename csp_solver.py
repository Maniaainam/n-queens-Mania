from constraint import Problem, AllDifferent

class CSPSolver:
    def __init__(self, n):
        self.n = n

    def solve(self):
        problem = Problem()
        cols = list(range(self.n))
        problem.addVariables(cols, list(range(self.n)))

         
        problem.addConstraint(AllDifferent())

 
        for i in range(self.n):
            for j in range(i + 1, self.n):
                problem.addConstraint(lambda c1, c2: abs(c1 - c2) != abs(i - j), (i, j))

        solutions = problem.getSolutions()
        if solutions:

            first_solution = solutions[0]
            return [first_solution[i] for i in range(self.n)]
        return None