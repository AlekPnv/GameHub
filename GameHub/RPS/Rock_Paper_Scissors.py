import pygame
from random import choice
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
_IMG = os.path.join(_DIR, "Images_RPS")

class Rock:
    def __init__(self, screen):
        self.screen   = screen
        self.position = (187, 392)
        self.image    = pygame.image.load(os.path.join(_IMG, "b1.png"))
        self.rect     = self.image.get_rect(topleft=self.position)

    def draw(self):
        self.screen.blit(self.image, self.position)

class Paper:
    def __init__(self, screen):
        self.screen   = screen
        self.position = (267, 392)
        self.image    = pygame.image.load(os.path.join(_IMG, "b2.png"))
        self.rect     = self.image.get_rect(topleft=self.position)

    def draw(self):
        self.screen.blit(self.image, self.position)

class Scissors:
    def __init__(self, screen):
        self.screen   = screen
        self.position = (347, 392)
        self.image    = pygame.image.load(os.path.join(_IMG, "b3.png"))
        self.rect     = self.image.get_rect(topleft=self.position)

    def draw(self):
        self.screen.blit(self.image, self.position)

class Player:
    def __init__(self, screen):
        self.screen   = screen
        self.position = (237, 250)

    def draw(self, choice):
        if choice:
            image = pygame.image.load(os.path.join(_IMG, f"hand{choice}.png"))
            image = pygame.transform.rotate(image, 100)
            self.screen.blit(image, self.position)

class Computer:
    def __init__(self, screen):
        self.screen   = screen
        self.position = (237, 87)

    def draw(self, choice):
        if choice:
            image = pygame.image.load(os.path.join(_IMG, f"hand{choice}.png"))
            image = pygame.transform.rotate(image, 100)
            self.screen.blit(image, self.position)

class Test:
    def __init__(self, player_choice, computer_choice):
        self.player_choice   = player_choice
        self.computer_choice = computer_choice

    def get_result(self):
        result = self.player_choice - self.computer_choice
        if result == 1 or result == -2:
            return "win"
        elif result == 0:
            return "draw"
        else:
            return "lose"

class Score:
    def __init__(self, screen):
        self.screen      = screen
        self.screen_rect = screen.get_rect()
        self.win  = 0
        self.draw = 0
        self.loss = 0
        self.font = pygame.font.SysFont("None", 24)

    def update(self, result):
        if result == "win":
            self.win  += 1
        elif result == "draw":
            self.draw += 1
        elif result == "lose":
            self.loss += 1

    def display(self):
        stats = [
            ("Win",  self.win,  (126, 223, 210), -75),
            ("Draw", self.draw, (159, 197,  77),   5),
            ("Loss", self.loss, (214, 108,  81),  85),
        ]
        for label, value, color, offset in stats:
            text = f"{label}: {value}"
            img  = self.font.render(text, True, color)
            rect = img.get_rect(center=(self.screen_rect.center[0] + offset, 375))
            rect.y += 6
            self.screen.blit(img, rect)

class ImgText:
    def __init__(self, screen):
        self.screen = screen

    def draw_message(self, message):
        if message:
            image = pygame.image.load(os.path.join(_IMG, f"{message}.png"))
            rect  = image.get_rect(center=self.screen.get_rect().center)
            rect.y -= 18
            rect.x += 7
            self.screen.blit(image, rect)

    def draw_label(self):
        font  = pygame.font.SysFont("Arial", 20)
        img   = font.render("Click your choice", True, (105, 105, 105))
        rect  = img.get_rect(center=(self.screen.get_rect().center[0], 475))
        self.screen.blit(img, rect)

def main_RPS():
    pygame.init()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Rock Paper Scissors")
    clock  = pygame.time.Clock()

    background = pygame.image.load(os.path.join(_IMG, "bg.jpg"))

    score    = Score(screen)
    player   = Player(screen)
    computer = Computer(screen)
    img_text = ImgText(screen)

    rock     = Rock(screen)
    paper    = Paper(screen)
    scissors = Scissors(screen)

    player_choice   = 0
    computer_choice = 0
    message         = "start"
    game_active     = True

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rock.rect.collidepoint(mouse_x, mouse_y):
                    player_choice = 1
                elif paper.rect.collidepoint(mouse_x, mouse_y):
                    player_choice = 2
                elif scissors.rect.collidepoint(mouse_x, mouse_y):
                    player_choice = 3
                else:
                    player_choice = 0
                game_active = True

        if game_active and player_choice:
            computer_choice = choice([1, 2, 3])
            test    = Test(player_choice, computer_choice)
            message = test.get_result()
            score.update(message)
            game_active = False

        player.draw(player_choice)
        computer.draw(computer_choice)
        rock.draw()
        paper.draw()
        scissors.draw()
        img_text.draw_message(message)
        img_text.draw_label()
        score.display()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_RPS()
