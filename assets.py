import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (230, 230, 230)
LIGHT_BLUE = (205, 205, 255)
LIGHT_RED = (255, 205, 205)
BLUE = (0, 0, 255)

pygame.font.init()


class Button:
    """Button go brr"""
    def __init__(self, window, pos, width, height, text, font, colors, hover):
        self.fg, self.bg = colors
        self.hover_fg, self.hover_bg = hover

        self.title = str(text)

        self.width = width
        self.height = height

        self.font = pygame.font.SysFont(str(font), int(height) * 3 // 4)
        self.hover_text = self.font.render(str(text), True, self.hover_fg)
        self.text = self.font.render(str(text), True, self.fg)

        self.bg_rect = pygame.Surface((self.width, self.height))
        self.bg_rect.fill(self.bg)
        
        self.hover_bg_rect = pygame.Surface((self.width, self.height))
        self.hover_bg_rect.fill(self.hover_bg)

        self.window = window
        self.pos = (window.get_width() // 2 - self.width // 2 if pos[0] == "centered" else pos[0],
                    window.get_height() // 2 - self.height // 2 if pos[1] == "centered" else pos[1])
        # Allows "centered" option in pos parameter.

        self.past_clicked = False
        self.current_clicked = False

        self.first_click_pos = False

    def hovered(self, pos=()):
        """Returns if the player's mouse is hovering over the button.
        Checks for the mouse's past and current position and clicks to see if the player clicks on the button.
        pos parameter checks if a specific pos counts as hovering the button."""
        self.past_clicked = self.current_clicked
        self.current_clicked = pygame.mouse.get_pressed(3)[0]
        self.first_click_pos = pygame.mouse.get_pos() if self.current_clicked and not self.first_click_pos else False

        mouse_pos = pygame.mouse.get_pos()

        if pos:
            return self.pos[0] < pos[0] < self.pos[0] + self.width \
                   and self.pos[1] < pos[1] < self.pos[1] + self.height

        return self.pos[0] < mouse_pos[0] < self.pos[0] + self.width \
               and self.pos[1] < mouse_pos[1] < self.pos[1] + self.height

    def was_clicked(self):
        """Returns if the player is clicking the button."""
        return self.past_clicked and not self.current_clicked and self.hovered(self.first_click_pos)
    
    def display(self):
        """Displays the button on the window."""
        if self.hovered():
            self.window.blit(self.hover_bg_rect, self.pos)
            self.window.blit(self.hover_text, (self.pos[0] + self.width // 2 - self.hover_text.get_width() // 2,
                                               self.pos[1] + self.height // 2 - self.hover_text.get_height() // 2))
        else: 
            self.window.blit(self.bg_rect, self.pos)
            self.window.blit(self.text, (self.pos[0] + self.width // 2 - self.text.get_width() // 2,
                                         self.pos[1] + self.height // 2 - self.text.get_height() // 2))
