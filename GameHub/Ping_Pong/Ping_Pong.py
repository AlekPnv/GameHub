from pygame import *
import random
import sys

# Draw paddle
def draw_paddle(pos):
    draw.rect(screen, WHITE, (pos[0], pos[1], paddle_width, paddle_height))

# Draw ball
def draw_ball(pos):
    draw.circle(screen, WHITE, pos, ball_radius)

# Update ball position and handle collisions
def update_ball():
    global ball_pos, ball_speed, player1_score, player2_score

    # Update ball position
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Ball bounces off top and bottom walls
    if ball_pos[1] <= 10 or ball_pos[1] >= HEIGHT - 10:
        ball_speed[1] = -ball_speed[1]

    # Ball bounces off player 1's paddle
    if ball_pos[0] <= player1_pos[0] + paddle_width and player1_pos[1] <= ball_pos[1] <= player1_pos[1] + paddle_height:
        ball_speed[0] = -(ball_speed[0] + 1)  # Reverse direction and increase speed
        ball_speed[1] += 0.5 if ball_speed[1] > 0 else -0.5  # Adjust vertical speed slightly

    # Ball bounces off player 2's paddle
    elif ball_pos[0] >= player2_pos[0] and player2_pos[1] <= ball_pos[1] <= player2_pos[1] + paddle_height:
        ball_speed[0] = -(ball_speed[0] - 1) if ball_speed[0] < 0 else -(ball_speed[0] + 1)
        ball_speed[1] += 0.5 if ball_speed[1] > 0 else -0.5
    
    # Scoring conditions
    if ball_pos[0] <= 0:
        player2_score += 1
        reset()
    
    if ball_pos[0] >= WIDTH:
        player1_score += 1
        reset()

# Reset ball position and speed
def reset():
    global ball_pos, ball_speed
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_speed = [7 if random.choice([True, False]) else -7, 7 if random.choice([True, False]) else -7]

def main_Ping_Pong():
    global WIDTH, HEIGHT, screen, WHITE, paddle_height, paddle_width, player2_score, player1_score, player1_pos, player2_pos, ball_radius, ball_pos, ball_speed
    WIDTH = 800
    HEIGHT = 600
    screen = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    FPS = 50
    display.set_caption("Ping Pong")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    paddle_width = 7
    paddle_height = 100
    paddle_speed = 14

    ball_radius = 9

    player1_pos = [15, (HEIGHT - paddle_height) / 2]
    player2_pos = [WIDTH - 15 - paddle_width, (HEIGHT - paddle_height) / 2]

    player1_score = 0
    player2_score = 0

    ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
    ball_speed = [7 if random.choice([True, False]) else -7, 7 if random.choice([True, False]) else -7]

    font.init()
    score_font = font.Font(None, 45) 
    running = True
    while running:
        screen.fill(BLACK)
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
                running = False
        keys = key.get_pressed()
        if keys[K_w] and player1_pos[1] > 0:
            player1_pos = (player1_pos[0], player1_pos[1] - paddle_speed)
        elif keys[K_s] and player1_pos[1] < HEIGHT - paddle_height:
            player1_pos = (player1_pos[0], player1_pos[1] + paddle_speed)
        
        if keys[K_UP] and player2_pos[1] > 0:
            player2_pos = (player2_pos[0], player2_pos[1] - paddle_speed)
        elif keys[K_DOWN] and player2_pos[1] < HEIGHT - paddle_height:
            player2_pos = (player2_pos[0], player2_pos[1] + paddle_speed)

        update_ball()
        screen.fill(BLACK)

        draw_paddle(player1_pos)
        draw_paddle(player2_pos)
        draw_ball(ball_pos)

        player1_text = score_font.render(str(player1_score), True, WHITE)
        player2_text = score_font.render(str(player2_score), True, WHITE)
        screen.blit(player1_text, (WIDTH / 4, 20))
        screen.blit(player2_text, (WIDTH * 3 / 4, 20))

        player1_winner = score_font.render("Player1 wins", True, WHITE)
        player2_winner = score_font.render("Player2 wins", True, WHITE)

        if player1_score >= 5:
            screen.fill(BLACK)
            text_rect = player1_winner.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(player1_winner, text_rect)
            display.update()
            time.delay(2750)
            running = False

        elif player2_score >= 5:
            screen.fill(BLACK)
            text_rect = player2_winner.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(player2_winner, text_rect)
            display.update()
            time.delay(2000)
            running = False

        while not running:
            screen.fill(BLACK)
            play_again_text = score_font.render("Play Again? (Y/N)", True, WHITE)
            screen.blit(play_again_text, (WIDTH / 3, HEIGHT / 2))
            display.update()
            for e in event.get():
                if e.type == QUIT:
                    quit()
                    sys.exit()
                elif e.type == KEYDOWN:
                    if e.key == K_y:  # Restart game
                        player1_score = 0
                        player2_score = 0
                        reset()
                        running = True
                    elif e.key == K_n:  # Quit game
                        quit()
                        sys.exit()

        display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main_Ping_Pong()