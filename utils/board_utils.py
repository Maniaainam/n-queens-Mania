def display_board(solution):
    if not solution:
        return "No solution to display."
    n = len(solution)
    board_str = ""
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[col] == row:
                line += "Q "
            else:
                line += ". "
        board_str += line + "\n"
    return board_str