import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import *
from asteroid import *
from asteroidfield import *
from shot import *
from logger import log_event

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    white = (255, 255, 255)
    black = (0, 0, 0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boot.dev - Asteroids")

    clock = pygame.time.Clock()
    dt = 0

    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidfield = AsteroidField()

    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f"SCORE: {score}", True, white)
    textRect = text.get_rect()
    textRect.center = ((SCREEN_WIDTH / 2), (25))

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        updatable.update(dt)

        for object in asteroids:
            if object.collides_with(player):
                log_event("player_hit")
                print(f"Game over!      FINAL SCORE: {score}")
                sys.exit()

        for object in asteroids:
            for shot in shots:
                if object.collides_with(shot):
                    log_event("asteroid_shot")
                    object.split()
                    shot.kill()
                    score +=1
                    text = font.render(f"SCORE: {score}", True, white)

        for thing in drawable:
            thing.draw(screen)
        
        screen.blit(text, textRect)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
