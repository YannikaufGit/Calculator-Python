import pygame



class Button:
    def __init__(self, text, x_pos, y_pos, width, height, x_font, y_font):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.x_font = x_font
        self.y_font = y_font
        self.color_button = "#2A2A2A"
        self.color_text = "#D0D0D0"
        self.cooldown = 250
        self.last_click = 0

    def draw(self, screen, engine):
        font_button = pygame.font.SysFont("Roboto", 50)
        button_text = font_button.render(self.text, True, self.color_text)
        button_rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.color_button, button_rect, border_radius=5)
        pygame.draw.rect(screen, "black", button_rect, 2, border_radius=5)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        self._check_clicks(engine)

    def _check_clicks(self, engine):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect((self.x_pos, self.y_pos), (self.width, self.height))
        now = pygame.time.get_ticks()
        if left_click and button_rect.collidepoint(mouse_pos):
            if now - self.last_click >= self.cooldown:
                self.last_click = now
                engine.press(self.text)

        # to include hovering over the buttons:

        if button_rect.collidepoint(mouse_pos):
            self.color_button = "#353535"
        else:
            self.color_button = "#2A2A2A"

class Result:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.start_size = self.size
        self.color = "#F5F5F5"
    def draw(self, screen, engine):

        # Error handling to let the user know that there is a mistake with his calculation

        if engine.error == True:
            self.color = "#D64545"
        else:
            self.color= "#F5F5F5"

        # Depiction of the result / expression 
        
        anchor_x, anchor_y = 440, 115
        font_result = pygame.font.SysFont("Roboto", int(self.size))
        if engine.expression == "":
            result_text = font_result.render("0", True, self.color)
        else:
            result_text = font_result.render(engine.expression, True, self.color)
        result_text_rect = result_text.get_rect()
        result_text_rect.midright = (anchor_x, anchor_y)
        screen.blit(result_text, result_text_rect)

        # Length Handeling

        if len(engine.expression) > 14 and len(engine.expression) <=18:
            self.size = self.start_size*0.8
        elif len(engine.expression) <= 14:
            self.size = self.start_size
        elif len(engine.expression) > 18 and len(engine.expression) <= 24:
            self.size = self.start_size*0.6
        elif len(engine.expression) > 24:
            self.size = self.start_size*0.4
        if len(engine.expression) >38:
            print("Equation to long, try splitting the equation!")
            
