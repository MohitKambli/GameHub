import pygame
import random

def game():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 600, 400
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Paddle Constants
    PADDLE_WIDTH, PADDLE_HEIGHT = 15, 80
    PADDLE_SPEED = 5

    # Ball Constants
    BALL_SIZE = 15
    BALL_SPEED = 5

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Function to draw paddles, ball, and scores
    def draw_objects(player_paddle, ai_paddle, ball, player_score, ai_score):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, ai_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        font = pygame.font.Font(None, 36)
        player_score_text = font.render(str(player_score), True, WHITE)
        ai_score_text = font.render(str(ai_score), True, WHITE)

        screen.blit(player_score_text, (WIDTH // 4, 20))
        screen.blit(ai_score_text, (3 * WIDTH // 4 - ai_score_text.get_width(), 20))

    # Function to update the AI paddle position to follow the ball closely
    def update_ai_paddle(ai_paddle, ball):
        # Add randomness to the AI paddle's movement
        random_factor = random.uniform(0.0, 2.0)  # Adjust the range as needed
        if ai_paddle.centery < ball.centery:
            ai_paddle.centery += int(PADDLE_SPEED * random_factor)
        elif ai_paddle.centery > ball.centery:
            ai_paddle.centery -= int(PADDLE_SPEED * random_factor)

    # Function to reset the ball position
    def reset_ball():
        return pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    # Main game loop
    def main():
        player_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ai_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = reset_ball()

        ball_speed_x = random.choice([BALL_SPEED, -BALL_SPEED])
        ball_speed_y = random.choice([BALL_SPEED, -BALL_SPEED])

        player_score = 0
        ai_score = 0

        game_running = False  # Variable to track game state

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_running = not game_running  # Toggle game state on Spacebar press

            if game_running:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and player_paddle.top > 0:
                    player_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
                    player_paddle.y += PADDLE_SPEED

                # Update AI paddle position
                update_ai_paddle(ai_paddle, ball)

                # Move the ball
                ball.x += ball_speed_x
                ball.y += ball_speed_y

                # Ball collision with walls
                if ball.top <= 0 or ball.bottom >= HEIGHT:
                    ball_speed_y = -ball_speed_y

                # Ball collision with paddles
                if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
                    ball_speed_x = -ball_speed_x

                # Ball out of bounds
                if ball.left <= 0:
                    ai_score += 1
                    ball = reset_ball()
                elif ball.right >= WIDTH:
                    player_score += 1
                    ball = reset_ball()

            # Draw paddles, ball, and scores
            draw_objects(player_paddle, ai_paddle, ball, player_score, ai_score)

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(FPS)

    main()

# Call the game function
if __name__ == "__main__":
    game()
