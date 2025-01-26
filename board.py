import random


class Board:
    def __init__(self, difficulty):
        # Sudoku
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.zero_count = 81 - difficulty * 10
        self.generate()
        self.original_board = [list(number) for number in self.board]

    def generate(self):
        self.solve()
        # Solves the board randomly
        zeroes = [(random.randint(0, 8), random.randint(0, 8)) for _ in range(self.zero_count)]
        # Random empty square coordinates
        for coordinate in zeroes:
            self.board[coordinate[0]][coordinate[1]] = 0

    def __str__(self):
        result = ""

        for ri, row in enumerate(self.board):
            if ri % 3 == 0 and ri != 0:
                result += "- - - - - - - - - - -\n"
            for ci, num in enumerate(row):
                if ci % 3 == 0 and ci != 0:
                    result += "| "
                result += f"{str(num)} "
            result += "\n"
        return result
            
    def __repr__(self):
        return f"Board({self.zero_count})"

    def __iter__(self):
        return self.board.__iter__()

    def reset(self):
        """Resets the board. Makes the board the original board."""
        self.board = [list(number) for number in self.original_board]

    def free_box(self, row, column):
        """Checks if a Sudoku box wasn't filled with a permanent number."""
        return self.original_board[row][column] == 0

    def valid_move(self, row, column, number):
        """Returns True if placing a number in a position in the Sudoku board is a valid move.
        Otherwise, returns False."""
        if number in self.board[row]:
            return False
        # Checks if the number is in the row.

        for r in self.board:
            if r[column] == number:
                return False
        # Checks if the number is in the column.

        box_pos = (row // 3, column // 3)
        for r in range(box_pos[0] * 3, box_pos[0] * 3 + 3):
            for c in range(box_pos[1] * 3, box_pos[1] * 3 + 3):
                if self.board[r][c] == number:
                    return False
        return True
        # Checks if the number is in the square section.

    def find_empty(self):
        for ri, row in enumerate(self.board):
            try: 
                return ri, row.index(0)
            except ValueError:
                pass
        return False

    def find_all_empty_squares(self) -> list:
        empty_squares = []

        for ri, row in enumerate(self.board):
            for ci, square in enumerate(row):
                if square == 0:
                    empty_squares.append((ri, ci))
        return empty_squares

    def get_empty(self, row, column):
        """Returns True if a spot in the Sudoku board is empty."""
        return not self.board[row][column]

    def solve(self):
        """Solves the Sudoku board."""
        if not (find := self.find_empty()):
            return True
        row, column = find

        for n in random.sample(range(1, 10), 9):
            if self.valid_move(row, column, n):
                self.board[row][column] = n

                if self.solve():
                    return True

                self.board[row][column] = 0
        return False
                
    def change_number(self, row, column, number):
        """Changes the Sudoku board's number in a specific position."""
        self.board[row][column] = number

    def check(self) -> list:
        """check() -> [error boxes, ...]
        Checks for mistakes in the Sudoku board.
        Returns a tuple where the mistake is.
        Returns False otherwise."""
        error_squares = self.find_all_empty_squares()

        for row_index, row in enumerate(self):
            for column_index, number in enumerate(row):
                index = row_index, column_index

                if self.board[row_index].count(number) > 1:
                    error_squares.append(index)
                # Checks if the number is in the row.

                if [r[column_index] for r in self.board].count(number) > 1:
                    error_squares.append(index)
                # Checks if the number is in the column.

                box_pos = (row_index // 3, column_index // 3)
                square = []
                for ri in range(3):
                    for ci in range(3):
                        square.append(self.board[ri][ci])
                if square.count(number) > 1:
                    error_squares.append(index)
                # Checks if the number is in the square section.
        return error_squares
