import pygame
import random
import pygame_widgets
from pygame_widgets.button import Button

# Constants
Snakeblock = 30
Colore_body = ("#306850")
Colore_head = ("#071821")
Colore_apple = "red"
Startlengh = 3
Background = ("#86c06c")
FPS = 30
Window_x = Snakeblock * 17
Window_y = Snakeblock * 17

# Initialize Pygame
pygame.init()
pygame.font.init()
Window = pygame.display.set_mode((Window_x, Window_y))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Fonts
buttonfront = pygame.font.SysFont("arial", 20)
end_screen_font = pygame.font.SysFont("Arial", 40)

class Snake():
    def __init__(self):
        self.body = []
        self.lengh = 0
        self.direction = None
        self.gameover = False
        self.new()
        
    def new(self):
        # Initialize a new snake
        self.body = []
        for i in range(Startlengh):
            new_body = (Snakeblock, Snakeblock * i)
            self.body.append(new_body)
        self.gameover = False
        self.direction = "DOWN"
        self.lengh = len(self.body)
    
    def move(self):
        # Move the snake in the current direction
        head = self.body[-1]
        if self.direction == "DOWN":
            new_head = (head[0], head[1] + Snakeblock)
        if self.direction == "UP":
            new_head = (head[0], head[1] - Snakeblock)
        if self.direction == "RIGHT":
            new_head = (head[0] + Snakeblock, head[1])
        if self.direction == "LEFT":
            new_head = (head[0] - Snakeblock, head[1])
        self.body.append(new_head)
        if self.lengh < len(self.body):
            self.body.pop(0)
            
    def draw(self):
        # Draw the snake on the window
        pygame.draw.rect(Window, Colore_head, (self.body[-1][0], self.body[-1][1], Snakeblock, Snakeblock), border_radius=4)
        for i in range(len(self.body) - 1):
            pygame.draw.rect(Window, Colore_body, (self.body[i][0], self.body[i][1], Snakeblock, Snakeblock), border_radius=4)
            
    def collision(self):
        # Check for collisions
        head = self.body[-1]
        for i in range(len(self.body) - 1):
            if self.body[i] == head:
                self.gameover = True
            if head[0] == apple.x and head[1] == apple.y:
                apple.new()
                self.lengh += 1
            if head[0] >= Window_x or head[0] < 0:
                self.gameover = True
            if head[1] >= Window_y or head[1] < 0:
                self.gameover = True

class Apple():
    def __init__(self):
        self.new()
        
    def new(self):
        # Generate a new apple position
        block_in_x = int(Window_x / Snakeblock)
        block_in_y = int(Window_y / Snakeblock)
        while True:
            self.x = random.randint(0, block_in_x - 1) * Snakeblock
            self.y = random.randint(0, block_in_y - 1) * Snakeblock
            if (self.x, self.y) not in snake.body:
                break
    
    def draw(self):
        # Draw the apple on the window
        pygame.draw.rect(Window, Colore_apple, (self.x, self.y, Snakeblock, Snakeblock), border_radius=int(Snakeblock / 2))

# Initialize snake and apple
snake = Snake()
apple = Apple()

def newgame():
    # Start a new game
    apple.new()
    snake.new()

pause = False   
move_interval = 150
last_move_time = pygame.time.get_ticks()

def main_Snake():
    global last_move_time
    run = True
    while run:
        Window.fill(Background)
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                    break
            if keys[pygame.K_RIGHT]:
                if snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                    break
            if keys[pygame.K_UP]:
                if snake.direction != "DOWN":
                    snake.direction = "UP"
                    break
            if keys[pygame.K_DOWN]:
                if snake.direction != "UP":
                    snake.direction = "DOWN"
                    break
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_interval:
            if snake.gameover:
                bt_cover = Button(Window, (Window_x - 180) / 2, 50, 180, 40, radius=4, font=buttonfront, text="New Game", onClick=lambda: newgame())
                pygame_widgets.update(events)
                if keys[pygame.K_SPACE]:
                    newgame()
            elif snake.lengh == (Window_x // Snakeblock) * (Window_y // Snakeblock):
                bt_end = Button(Window, (Window_x - 200) / 2, 100, 200, 100, radius=4, font=end_screen_font, text="You Won", onClick=exit)
                pygame_widgets.update(events)
            else:
                apple.draw()
                snake.move()
                snake.collision()
            snake.draw()
            caption = f"The Snake   Score: {snake.lengh - 3}"
            pygame.display.set_caption(caption)
            pygame.display.update()
            last_move_time = current_time
        
if __name__ == "__main__":
    main_Snake()