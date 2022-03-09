import random
import string
import pyttsx3
import time
from colorama import Fore
import pyjokes
import pygame

pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)
COLOR_INACTIVE = pygame.Color('green4')
COLOR_ACTIVE = pygame.Color('green')


def pygame_create(width ,height, color):
    first_window = pygame.display.set_mode((width, height))
    first_window.fill(color)
    pygame.display.update()
    return first_window

class pygame_InputBox:
    def __init__(self, x, y, width=100, height=21, text='', text_color=GREEN):
        self.color = COLOR_INACTIVE
        self.text = text
        self.textColor = text_color
        self.textSize = int(height * 0.8)
        self.FONT = pygame.font.Font(None, self.textSize)
        self.txt_surface = self.FONT.render(text, True, text_color)
        self.minWidth = width
        self.rect = self.txt_surface.get_rect()
        self.rect.w = width
        self.rect.h = height
        self.rect.center = (x, y)
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.textColor)
        self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.minWidth, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        self.text = ""
        self.txt_surface = self.FONT.render(self.text, True, self.textColor)


class pygame_Button:
    def __init__(self, x, y, width=82, height=23, text='Button', color=GRAY, outline_color=None):
        self.color = color
        self.x = x-(width/2)
        self.y = y+(height/2)
        self.width = width
        self.height = height
        self.text = text
        self.outlineColor = outline_color
        self.regColor = self.color
        self.overColor = self.create_over_color(self.color)
        self.clickedColor = ()

    def draw(self, win):
        # Call this method to draw the button on the win
        if self.outlineColor:
            pygame.draw.rect(win, self.outlineColor, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', int(self.height*0.75))
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
        if self.is_over():
            self.color = self.overColor
            if True in pygame.mouse.get_pressed():
                self.color = self.regColor
        else:
            self.color = self.regColor

    def is_over(self):
        pos = pygame.mouse.get_pos()
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if (pos[0] > self.x) and (pos[0] < self.x + self.width):
            if (pos[1] > self.y) and (pos[1] < self.y + self.height):
                return True
        return False

    def is_clicked(self):
        if self.is_over():
            return True in pygame.mouse.get_pressed()

    @staticmethod
    def create_over_color(color):
        out_put_color = []
        if 255 in color:
            adder = 70
        else:
            adder = 15
        for num in color:
            if num + adder > 255:
                out_put_color.append(255)
            else:
                out_put_color.append(num + adder)
        return tuple(out_put_color)


class pygame_Label:
    def __init__(self, x, y, text='Label', color=BLACK, size=32, font=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.font = font
        self.FONT = pygame.font.Font(font, self.size)
        self.textSurface = self.FONT.render(text, True, color)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (x, y)
    def draw(self, win):
        win.blit(self.textSurface, self.textRect)

    def set_text(self, text):
        self.text = text
        self.textSurface = self.FONT.render(text, True, self.color)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (self.x, self.y)

    def set_color(self, color):
        self.color = color
        self.textSurface = self.FONT.render(self.text, True, self.color)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (self.x, self.y)

    def set_size(self, new_size):
        self.size = new_size
        self.FONT = pygame.font.Font(self.font, self.size)
        self.textSurface = self.FONT.render(self.text, True, self.color)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = (self.x, self.y)
class RandomInput:

    def Normal(number):
        number = random.randint(0, int(number))
        return number
    def Seed(seed_number):
        random.seed(seed_number)
        seedl = [random.randint(0,9) for i in range(seed_number)]

        seed = [str(int) for int in seedl]
        seed = int(''.join(seed))

        return seed
    def Leters(range_):
        leters = ''.join([random.choice(string.ascii_letters + string.digits  ) for i in range(range_)])
        return leters

class Spack:

    def Male(text):
        engine=pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.getProperty('voices')
        engine.setProperty('voice',voices[0].id)
        engine.say(text)
        engine.runAndWait()



    def Female(text):
        engine=pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

class Counter:

    def Up(time):
        countUp = [i for i in range(time)]
        countUp = [str(i) for i in countUp]
        time = str('\n'.join(countUp))
        return time

    def Clock(time_, red_number=None):
        while time_:
            if red_number != None:
                mins, seconds = divmod(time_, 60)
                Rmins, Rseconds = divmod(red_number, 60)
                Rtimer = "{:02d}:{:02d}".format(Rmins,Rseconds)
                timer = "{:02d}:{:02d}".format(mins,seconds)
                if timer <= Rtimer:
                    timer = "{:02d}:{:02d}".format(mins,seconds)
                    print(Fore.RED+timer, end="\r")
                else:
                    timer = "{:02d}:{:02d}".format(mins,seconds)
                    print(timer, end="\r")
                time.sleep(1)
                time_ -= 1
            else:
                mins, seconds = divmod(time_, 60)
                timer = "{:02d}:{:02d}".format(mins,seconds)
                print(timer, end="\r")
                time.sleep(1)
                time_ -= 1
        print(Fore.WHITE+'00:00')

class Fun:

    def Joke():
        return pyjokes.get_joke()

    def Jokes():
        return pyjokes.get_joke()
