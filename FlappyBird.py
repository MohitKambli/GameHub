import pygame
import sys
import random

def game():
    pygame.init()

    # Set up the window
    WIDTH, HEIGHT = 800, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    bird_x = 50
    bird_y = HEIGHT // 2
    bird_speed = 5
    bird_jump = 50
    jumping = False  # Flag to track if the bird is currently jumping

    pipe_width = 50
    pipe_gap = 150
    pipe_speed = 2

    pipes = []

    game_active = False  # Set game_active to False initially
    score = 0  # Initialize the score

    font = pygame.font.Font(None, 36)

    def draw_bird(x, y):
        pygame.draw.rect(window, (0, 128, 255), (x, y, 30, 30))  # Blue bird

    def draw_pipe(pipe):
        pygame.draw.rect(window, (0, 255, 0), pipe)  # Green pipes

    def draw_score(score):
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 10))

    def check_collision(bird_rect, pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return True
        return False

    def check_boundary_collision(y):
        # Check if the bird hits the top or bottom of the window
        return y < 0 or y + 30 > HEIGHT

    def restart_game():
        nonlocal bird_y, pipes, game_active, score
        bird_y = HEIGHT // 2
        pipes = []
        game_active = True
        score = 0  # Reset the score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_active:
                        restart_game()
                    else:
                        jumping = True

        if game_active:
            # Update bird position
            if jumping:
                bird_y -= bird_jump
                jumping = False
            else:
                bird_y += bird_speed

            # Check for boundary collisions
            if check_boundary_collision(bird_y):
                print("Game Over! Boundary Collision")
                game_active = False

            # Generate pipes
            if len(pipes) == 0 or pipes[-1].x <= WIDTH - pipe_width - pipe_gap:
                top_pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
                pipes.append(pygame.Rect(WIDTH, 0, pipe_width, top_pipe_height))
                pipes.append(pygame.Rect(WIDTH, top_pipe_height + pipe_gap, pipe_width, HEIGHT - top_pipe_height - pipe_gap))

            # Move pipes
            for pipe in pipes:
                pipe.x -= pipe_speed

                # Check for scoring (when the bird passes through the gap)
                if pipe.x + pipe.width == bird_x:
                    score += 1

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

            # Draw everything
            window.fill((255, 255, 255))  # White background

            bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)
            draw_bird(bird_x, bird_y)

            for pipe in pipes:
                draw_pipe(pipe)

            # Draw the score
            draw_score(score // 2)

            # Check for collisions
            if check_collision(bird_rect, pipes):
                print("Game Over! Pipe Collision")
                game_active = False

            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Adjust the frame rate
        else:
            # Display game over text
            game_over_text = font.render("Press SPACE to Begin!", True, (255, 0, 0))
            window.blit(game_over_text, (50, HEIGHT // 2 - 18))

            pygame.display.flip()
            pygame.time.Clock().tick(30)

if __name__ == "__main__":
    game()
