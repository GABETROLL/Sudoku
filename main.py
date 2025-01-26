from board import Board
from assets import *


class Window:
    def __init__(self, width, height, board_w, board_pos, alt_board_w, alt_board_pos, bg, font, caption):
        self.width = width
        self.height = height

        # Placeholders
        self.board = Board(1)

        self.running = True
        self.difficulty_screen = True
        self.quit_screen = False
        self.finish_screen = False
        self.solution_screen = False
        self.won = False

        self.small_font = pygame.font.SysFont("NOTHING TO SEE HERE", 69)
        self.big_font = pygame.font.SysFont("NOTHING TO SEE HERE", 69)
        self.font = pygame.font.SysFont("NOTHING TO SEE HERE", 69)
        # Placeholders

        self.board_width = board_w
        self.board_x_pos = board_pos[0]
        self.board_y_pos = board_pos[1]
        self.board_block_width = board_w // 9
        # main board where user plays

        self.alt_board_width = alt_board_w
        self.alt_board_x_pos = width // 2 - alt_board_w // 2 if alt_board_pos[0] == "centered" else alt_board_pos[0]
        self.alt_board_y_pos = height // 2 - alt_board_w // 2 if alt_board_pos[1] == "centered" else alt_board_pos[1]
        self.alt_board_block_width = alt_board_w // 9
        # board displayed in quit and finish screen

        self.current_box = ()
        self.current_number = ()
        self.error_boxes = ()

        self.bg = bg

        self.WINDOW = pygame.display.set_mode((width, height))
        pygame.display.set_caption(str(caption))
        self.reset()

        self.font_name = font

        self.DIFFICULTY_BUTTONS = [Button(self.WINDOW, ("centered", 150 * n), 300, 100, n, font, (BLACK, LIGHT_GRAY), (BLACK, GRAY)) for n in range(1, 4)]

        self.QUIT_BUTTON = Button(self.WINDOW, (0, board_w), 300, 100, "Quit", font, (WHITE, BLUE), (BLACK, LIGHT_BLUE))
        self.FINISH_BUTTON = Button(self.WINDOW, (width * 2 // 3, board_w), 300, 100, "Finish", font, (WHITE, BLUE), (BLACK, LIGHT_BLUE))

        self.PLAY_AGAIN = Button(self.WINDOW, (width * 2 // 3, board_w), 300, 100, "Play Again", font, (WHITE, BLUE), (BLACK, LIGHT_BLUE))

        self.SOLUTION_BUTTON = Button(self.WINDOW, (width * 2 // 3, board_w), 300, 100, "Solution", font, (WHITE, BLUE), (BLACK, LIGHT_BLUE))

        self.EXIT_BUTTON = Button(self.WINDOW, ("centered", board_w), 300, 100, "Exit", font, (WHITE, BLUE), (BLACK, LIGHT_BLUE))
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            if self.difficulty_screen:
                self.difficulty()
            elif self.quit_screen:
                self.quit_playing("Would you like to see a solution?", 30, ("centered", 200), BLACK)
            elif self.finish_screen:
                self.finish(self.won, "Would you like to play again?", "You completed the board!", 30, ("centered", 200), BLACK)
            elif self.solution_screen:
                self.solution()
            else:
                self.main()
            # Checks what the player is doing: choosing the difficuly, quitting, finishing or playing.

            pygame.display.update()

        pygame.quit()

    def reset(self):
        """Resets the game."""
        self.running = True
        self.difficulty_screen = True
        self.quit_screen = False
        self.finish_screen = False
        self.solution_screen = False
        self.won = False
    
    def difficulty(self):
        """Player needs to choose the difficulty before starting the game."""
        self.WINDOW.fill(self.bg)
            
        for button in self.DIFFICULTY_BUTTONS:
            button.display()
            
        for button in self.DIFFICULTY_BUTTONS:
            if button.was_clicked():
                self.board = Board(int(button.title))
                self.difficulty_screen = False
                break
    
    def main(self):
        """Main game."""
        # Displaying all of the buttons first, then checking for clicks
        # In case the user lags.
        self.WINDOW.fill(self.bg)

        self.draw_sudoku(False)

        self.QUIT_BUTTON.display()
        self.FINISH_BUTTON.display()

        self.check_for_moves()
                
        if self.QUIT_BUTTON.was_clicked():
            self.quit_screen = True
            self.finish_screen = False

        if self.FINISH_BUTTON.was_clicked():
            self.error_boxes = self.board.check()
            if not self.error_boxes:
                self.finish_screen = True
                self.won = True
        
    def _draw_board(self, board_w, board_pos):
        """Draws Sudoku board's lines according to board's position and width."""
        if self.current_box:
            pygame.draw.rect(self.WINDOW,
                             LIGHT_BLUE,
                             pygame.Rect(self.current_box[1] * self.board_block_width + board_pos[0],
                                         self.current_box[0] * self.board_block_width + board_pos[1],
                                         self.board_block_width, self.board_block_width))
            # Draws light blue rectangle under the current used box.
        elif self.error_boxes:
            for error_box in self.error_boxes:
                pygame.draw.rect(self.WINDOW,
                                 LIGHT_RED,
                                 pygame.Rect(error_box[1] * self.board_block_width + board_pos[0],
                                             error_box[0] * self.board_block_width + board_pos[1],
                                             self.board_block_width, self.board_block_width))
            # Draws light red rectangle under the boxes with a wrong number.

        self.big_line_padding = 6
        self.small_line_padding = 3
            
        for x_pos in range(10):
            pygame.draw.line(self.WINDOW,
                             BLACK,
                             (x_pos * self.board_block_width + board_pos[0], board_pos[1]),
                             (x_pos * self.board_block_width + board_pos[0], board_pos[1] + board_w),
                             self.big_line_padding if x_pos % 3 == 0 else self.small_line_padding)

        for y_pos in range(10):
            pygame.draw.line(self.WINDOW,
                             BLACK,
                             (board_pos[0], y_pos * self.board_block_width + board_pos[1]),
                             (board_pos[0] + board_w, y_pos * self.board_block_width + board_pos[1]),
                             self.big_line_padding if y_pos % 3 == 0 else self.small_line_padding)
                         
    def _display_ints(self, board_w, board_pos):
        """Displays ints in Sudoku board according to board's width and position and game rules."""
        for row_index, row in enumerate(self.board):
            for column_index, num in enumerate(row):
                if not (row_index, column_index) == self.current_box:
                    # if the user isn't working on the box to not stack numbers.

                    num_text = self.font.render(str(num) if num != 0 else " ", True, GRAY if self.board.free_box(row_index, column_index) else BLACK)
                    # Black rendered text object if it's an original number, otherwise it's gray.

                    self.WINDOW.blit(num_text,
                                     (column_index * self.board_block_width + board_pos[0] + self.board_block_width // 2 - num_text.get_height() // 2,
                                      row_index * self.board_block_width + board_pos[1] + self.board_block_width // 2 - num_text.get_width() // 2))

        if self.current_number and self.current_box:
            # Displays ints that are being edited in a smaller font.
            num_text = self.small_font.render(str(self.current_number) if self.current_number != 0 else " ", True, GRAY)
            # small num go br
            self.WINDOW.blit(num_text,
                             (self.current_box[1] * self.board_block_width + board_pos[0] + self.board_block_width // 2 - num_text.get_width() // 2,
                              self.current_box[0] * self.board_block_width + board_pos[1] + self.board_block_width // 2 - num_text.get_height() // 2))

    def draw_sudoku(self, alt):
        """Draws Sudoku board with its size corresponding to it being the alt board or main board."""
        self.big_font = pygame.font.SysFont(self.font_name, self.alt_board_width // 9 if alt else self.board_width // 9)
        self.font = pygame.font.SysFont(self.font_name, self.alt_board_width // (9 * 2) if alt else self.board_width // (9 * 2))
        self.small_font = pygame.font.SysFont(self.font_name, self.alt_board_width // (9 * 3) if alt else self.board_width // (9 * 3))

        if alt:
            self.board_block_width = self.alt_board_width // 9
            self._draw_board(self.alt_board_width, (self.alt_board_x_pos, self.alt_board_y_pos))
            self._display_ints(self.alt_board_width, (self.alt_board_x_pos, self.alt_board_y_pos))
        else:
            self.board_block_width = self.board_width // 9
            self._draw_board(self.board_width, (self.board_x_pos, self.board_y_pos))
            self._display_ints(self.board_width, (self.board_x_pos, self.board_y_pos))

    def check_for_moves(self):
        """Checks where the player clicked in the Sudoku board. Changes the number if valid."""
        mouse_pos = pygame.mouse.get_pos()
        # mouse position in the window
        board_pos = ((mouse_pos[1] - self.board_y_pos) // self.board_block_width,
                     (mouse_pos[0] - self.board_x_pos) // self.board_block_width)
        # mouse position in the Sudoku board

        if self.current_box:
            # Checks for keys 1-9 being pressed with their alt number.
            keys = pygame.key.get_pressed()
            for key in range(1, 10):
                if keys[key + 48]:
                    self.current_number = key
                    # changes the number in the current working box in the interface.
            if keys[pygame.K_BACKSPACE]:
                self.current_number = 0

            if keys[pygame.K_RETURN]:
                # Exits process when finished deciding the number.
                self.board.change_number(self.current_box[0], self.current_box[1], self.current_number)
                self.current_box = ()
                self.current_number = ()
                self.error_boxes = ()
                    
        if pygame.mouse.get_pressed(3)[0]:
            # if the left mouse button is pressed
            try:
                if self.board.free_box(board_pos[0], board_pos[1]):
                    self.current_box = board_pos
            except IndexError:
                # Checks if the mouse is in the board.
                self.current_box = False

    def solution(self):
        self.WINDOW.fill(self.bg)

        self.draw_sudoku(True)

        self.EXIT_BUTTON.display()
        if self.EXIT_BUTTON.was_clicked():
            self.running = False

    def quit_playing(self, quit_message, quit_size, quit_pos, quit_color):
        self.WINDOW.fill(self.bg)

        self.draw_sudoku(True)

        quit_font = pygame.font.SysFont(self.font_name, quit_size)
        quit_text = quit_font.render(quit_message, True, quit_color)

        self.WINDOW.blit(quit_text, (self.width // 2 - quit_text.get_width() // 2 if quit_pos[0] == "centered" else quit_pos[0],
                                     self.height // 2 - quit_text.get_height() // 2 if quit_pos[1] == "centered" else quit_pos[1]))
        # blits centered in axis if the item in parameter quit_pos is "centered", otherwise uses the position (int).

        self.QUIT_BUTTON.display()
        self.SOLUTION_BUTTON.display()

        if self.QUIT_BUTTON.was_clicked():
            self.running = False
        if self.SOLUTION_BUTTON.was_clicked():
            self.quit_screen = False
            self.solution_screen = True

            self.board.reset()
            self.board.solve()
            self.won = False

    def finish(self, won, finish_message, won_message, message_size, won_pos, message_color):
        self.WINDOW.fill(self.bg)

        won_text = self.big_font.render(won_message, True, message_color)
        finish_text = self.big_font.render(finish_message, True, message_color)
        self.WINDOW.fill(LIGHT_GRAY)

        self.draw_sudoku(True)

        if won:
            self.WINDOW.blit(won_text,
                             (self.width // 2 - won_text.get_width() // 2 if won_pos[0] == "centered" else won_pos[0],
                              self.height // 2 - won_text.get_height() // 2 if won_pos[1] == "centered" else won_pos[1]))

        self.WINDOW.blit(finish_text,
                         (self.width // 2 - won_text.get_width() // 2 if won_pos[0] == "centered" else won_pos[0] + 30,
                          self.height // 2 - won_text.get_height() // 2 if won_pos[1] == "centered" else won_pos[1] + 30))

        self.PLAY_AGAIN.display()
        self.QUIT_BUTTON.display()

        if self.PLAY_AGAIN.was_clicked():
            self.reset()
        if self.QUIT_BUTTON.was_clicked():
            self.running = False


Window(900, 1000, 900, (0, 0), 450, ("centered", 300), (230, 230, 230), "Consolas", "Sudoku!")
