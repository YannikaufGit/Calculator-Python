import pygame
import sys
import os

from .engine import CalculatorEngine
from .button import Button
from .button import Result

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Application():
    def __init__(self, color_bg):
        self.color_bg = color_bg
        pygame.init()

        self.width, self.height = 450, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Calculator by Yannik Gottwald")

        self.icon = pygame.image.load(resource_path("pictures/taschenrechner.png"))
        self.icon = pygame.transform.scale(self.icon, (25,25))
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        self.engine = CalculatorEngine("", 0)
        self.result = Result(100, 100, 50)
            
        button0 = Button("0", 10, 690, 100, 100, 50, 720)
        button1 = Button("1", 10, 580, 100, 100, 50, 610)
        button2 = Button("2", 120, 580, 100, 100, 160, 610)
        button3 = Button("3", 230, 580, 100, 100, 270, 610)
        button4 = Button("4", 10, 470, 100, 100, 50, 500)
        button5 = Button("5", 120, 470, 100, 100, 160, 500)
        button6 = Button("6", 230, 470, 100, 100, 270, 500)
        button7 = Button("7", 10, 360, 100, 100, 50, 390)
        button8 = Button("8", 120, 360, 100, 100, 160, 390)
        button9 = Button("9", 230, 360, 100, 100, 270, 390)
        
        buttonpoint = Button(".", 120, 690, 100, 100, 160, 720)
        buttonbackspace = Button("d", 230, 690, 100, 100, 270, 720)
        buttonequals = Button("=", 340, 690, 100, 100, 380, 720)
        buttonplus = Button("+", 340, 580, 100, 100, 380, 610)
        buttonminus = Button("-", 340, 470, 100, 100, 380, 500)
        buttonmulti = Button("*", 340, 360, 100, 100, 380, 390)
        buttondiv = Button("/", 340, 250, 100, 100, 380, 280)
        buttonclear = Button("c", 10, 250, 100, 100, 50, 280)
        buttonparleft = Button("(", 120, 250, 100, 100, 160, 280)
        buttonparright = Button(")", 230, 250, 100, 100, 270, 280)

        self.buttons = [button0, button1, button2, button3, button4, button5, button6, button7, button8, button9, buttonpoint, buttonbackspace,
                buttonequals, buttonplus, buttonminus, buttonmulti, buttondiv, buttonclear, buttonparleft, buttonparright]

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                self.handle_events(event)
            self.draw()
        pygame.quit()
        sys.exit()
        
    def draw(self):
        self.screen.fill(self.color_bg)
        for button in self.buttons:
            button.draw(self.screen, self.engine)
        pygame.draw.rect(self.screen, "#161616", [5, 15, self.width -10, 200], border_radius=20)
        self.result.draw(self.screen, self.engine)
        pygame.display.flip()
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.unicode in "0123456789+-*/=.()":
                self.engine.press(event.unicode)
                self.engine.error = False
            elif event.key == pygame.K_BACKSPACE:
                self.engine.press("DELETE")
                self.engine.error = False
            elif event.key == pygame.K_RETURN:
                self.engine.press("=")



            


