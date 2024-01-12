import pygame
import random
import sys

def game():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    # Car Constants
    CAR_WIDTH, CAR_HEIGHT = 50, 80
    BASE_CAR_SPEED = 5

    # Obstacle Constants
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
    OBSTACLE_SPEED = 5

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dodge Obstacles")

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Car class
    class Car(pygame.sprite.Sprite):
        def __init__(self, x, y, color):
            super().__init__()
            self.original_x = x  # Store the original x position
            self.original_y = y  # Store the original y position
            self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = BASE_CAR_SPEED

        def move(self, dx, dy):
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            # Boundary check to prevent the car from going beyond the window boundaries
            self.rect.x = max(0, min(self.rect.x, WIDTH - CAR_WIDTH))
            self.rect.y = max(0, min(self.rect.y, HEIGHT - CAR_HEIGHT))

        def reset_position(self):
            # Reset the car's position to the original location
            self.rect.x = self.original_x
            self.rect.y = self.original_y

    # Obstacle class
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def move(self):
            self.rect.y += OBSTACLE_SPEED

    # Function to draw cars and obstacles
    def draw_objects(user_car, ai_car, obstacles, winner_text=None):
        screen.fill(BLACK)
        screen.blit(user_car.image, user_car.rect)
        screen.blit(ai_car.image, ai_car.rect)
        for obstacle in obstacles:
            screen.blit(obstacle.image, obstacle.rect)
        if winner_text:
            font = pygame.font.SysFont(None, 55)
            text = font.render(winner_text, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    # Function to handle collisions
    def check_collisions(user_car, ai_car, obstacles):
        if pygame.sprite.spritecollide(user_car, obstacles, True):
            return "User Car"
        # Check collisions with AI car
        ai_collisions = pygame.sprite.spritecollide(ai_car, obstacles, False)
        if ai_collisions:
            return "AI Car"
        return None

    # Main game loop
    def main():
        user_car = Car(int(WIDTH * 0.25) - CAR_WIDTH // 2, HEIGHT - 2 * CAR_HEIGHT, BLUE)
        ai_car = Car(int(WIDTH * 0.75) - CAR_WIDTH // 2, HEIGHT - 2 * CAR_HEIGHT, GREEN)  # Align AI car with user car

        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()

        all_sprites.add(user_car)
        all_sprites.add(ai_car)

        game_running = False
        winner = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not game_running:
                            game_running = True
                            winner = None
                            obstacles.empty()
                            all_sprites.empty()
                            # Reset the cars' positions when restarting the game
                            user_car.reset_position()
                            ai_car.reset_position()

            if game_running:
                keys = pygame.key.get_pressed()
                user_car.move(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])

                # AI car movement (avoid obstacles and move opposite to boundaries)
                for obstacle in obstacles:
                    # Calculate vector from AI car to the obstacle
                    to_obstacle = pygame.Vector2(obstacle.rect.x - ai_car.rect.x, obstacle.rect.y - ai_car.rect.y)
                    distance = to_obstacle.length()

                    # Define a radius for obstacle avoidance
                    avoidance_radius = 100

                    # If the obstacle is within the avoidance radius and not too close to avoid division by zero
                    if 0 < distance < avoidance_radius:
                        # Normalize the vector to get the direction
                        to_obstacle /= distance

                        # Calculate a steering force to avoid the obstacle only in the x-direction
                        steering_force = pygame.Vector2(to_obstacle.x * (avoidance_radius - distance), 0)

                        # Update AI car's position based on the steering force
                        new_x = ai_car.rect.x - int(steering_force.x)

                        # Allow AI car to move towards the opposite direction of the obstacle when near boundaries
                        if new_x < 0 or new_x > WIDTH - CAR_WIDTH:
                            new_x = ai_car.rect.x + int(steering_force.x)

                        # Boundary check for AI car
                        new_x = max(0, min(new_x, WIDTH - CAR_WIDTH))
                        ai_car.rect.x = new_x

                # Create obstacles randomly
                if random.randint(0, 100) < 5:
                    obstacle = Obstacle(random.randint(0, WIDTH - OBSTACLE_WIDTH), 0)
                    obstacles.add(obstacle)
                    all_sprites.add(obstacle)

                # Move obstacles
                for obstacle in obstacles:
                    obstacle.move()
                    if obstacle.rect.y > HEIGHT:
                        obstacles.remove(obstacle)
                        all_sprites.remove(obstacle)

                # Check collisions
                collision_result = check_collisions(user_car, ai_car, obstacles)
                if collision_result:
                    game_running = False
                    winner = collision_result
            else:
                winner_text = f"Winner: {winner}" if winner else "Press SPACE to start"
                draw_objects(user_car, ai_car, obstacles, winner_text)
                font = pygame.font.SysFont(None, 55)
                text = font.render(winner_text, True, WHITE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            # Draw cars and obstacles
            draw_objects(user_car, ai_car, obstacles)

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            clock.tick(FPS)
            
    main()        

# Call the game function
if __name__ == "__main__":
    game()
