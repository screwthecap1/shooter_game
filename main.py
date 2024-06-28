import sys
import pygame
from random import randint

pygame.init()

game_font = pygame.font.SysFont('Arial', 50)

screen_width, screen_height = 800, 600
screen_fill_color = (32, 52, 71)
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Paw-Paw Shooter Game")

FIGHTER_STEP = 0.3
fighter_image = pygame.image.load('./images/fighter.png')
fighter_width, fighter_height = fighter_image.get_size()
fighter_x, fighter_y = screen_width / 2 - fighter_width / 2, screen_height - fighter_height
fighter_is_moving_left, fighter_is_moving_right = False, False

BALL_STEP = 0.08
ball_image = pygame.image.load('./images/ball.png')
ball_width, ball_height = ball_image.get_size()
ball_x, ball_y = 0, 0
ball_was_fired = False

ALIEN_STEP = 0.03
alien_speed = ALIEN_STEP
alien_image = pygame.image.load('./images/alien.png')
alien_width, alien_height = alien_image.get_size()
alien_x, alien_y = randint(0, screen_width - alien_width), 0

game_is_running = True
game_score = 0

while game_is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = True
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = True
            if event.key == pygame.K_SPACE:
                ball_was_fired = True
                ball_x = fighter_x + fighter_width / 2 - ball_width / 2
                ball_y = fighter_y - ball_height
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                fighter_is_moving_left = False
                fighter_is_moving_right = False

    if fighter_is_moving_left and fighter_x >= FIGHTER_STEP:
        fighter_x -= FIGHTER_STEP
    if fighter_is_moving_right and fighter_x <= screen_width - fighter_width - FIGHTER_STEP:
        fighter_x += FIGHTER_STEP

    alien_y += alien_speed
    if ball_was_fired and ball_y + ball_height < 0:
        ball_was_fired = False

    if ball_was_fired:
        ball_y -= BALL_STEP

    screen.fill(screen_fill_color)
    screen.blit(fighter_image, (fighter_x, fighter_y))
    screen.blit(alien_image, (alien_x, alien_y))
    if ball_was_fired:
        screen.blit(ball_image, (ball_x, ball_y))

    game_score_text = game_font.render(f"Score: {game_score}", True, 'orange')
    screen.blit(game_score_text, (640, 10))

    pygame.display.update()

    if alien_y + alien_height > fighter_y:
        game_is_running = False

    if (ball_was_fired and
            alien_x < ball_x < alien_x + alien_width - ball_width and
            alien_y < ball_y < alien_y + alien_height - ball_height):
        ball_was_fired = False
        alien_x, alien_y = randint(0, screen_width - alien_width), 0
        alien_speed += ALIEN_STEP / 2
        game_score += 1

game_over_text = game_font.render("GAME OVER", True, 'orange')
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (screen_width / 2, screen_height / 2)
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(3000)

pygame.quit()
