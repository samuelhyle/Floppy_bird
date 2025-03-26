import pygame
import random


pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Floppy Bird")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_WIDTH = 60
PIPE_HEIGHT = 400
PIPE_GAP = 150
BIRD_RADIUS = 20

clock = pygame.time.Clock()

bird_image = pygame.Surface((BIRD_RADIUS * 2, BIRD_RADIUS * 2), pygame.SRCALPHA)
pygame.draw.circle(bird_image, BLUE, (BIRD_RADIUS, BIRD_RADIUS), BIRD_RADIUS)


class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

    def jump(self):
        self.vel_y = BIRD_JUMP

    def draw(self):
        screen.blit(bird_image, (self.x - BIRD_RADIUS, self.y - BIRD_RADIUS))

    def get_rect(self):
        return pygame.Rect(self.x - BIRD_RADIUS, self.y - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)


class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN,
                         (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, PIPE_WIDTH, self.height),
            pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        ]


def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        bird.draw()

        for pipe in pipes:
            pipe.update()
            pipe.draw()

        for pipe in pipes:
            if bird.get_rect().collidelist(pipe.get_rects()) != -1:
                running = False

        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        for pipe in pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                score += 1
                pipe.passed = True

        if bird.y - BIRD_RADIUS < 0 or bird.y + BIRD_RADIUS > SCREEN_HEIGHT:
            running = False

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__ma in__":
    main()