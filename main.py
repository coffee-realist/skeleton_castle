import pygame
import os
import sys

INTRO_WINDOW_SIZE = 1280, 720
ABOUT_WINDOW_SIZE = 1023, 649
GAME_WINDOW_SIZE = 1280, 720
WINDOW_STATE = 0
FPS = 50


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_color_key(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global screen, WINDOW_STATE
    background = pygame.transform.scale(load_image('intro.jpg'), INTRO_WINDOW_SIZE)
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WINDOW_STATE == 0:
                    if 1070 <= x <= 1230 and 225 <= y <= 260:
                        print('game started')
                    elif 1090 <= x <= 1205 and 450 <= y <= 485:
                        terminate()
                    elif 1050 <= x <= 1230 and 375 <= y <= 410:
                        screen = pygame.display.set_mode(ABOUT_WINDOW_SIZE)
                        background = pygame.transform.scale(load_image('about.jpg'), ABOUT_WINDOW_SIZE)
                        screen.blit(background, (0, 0))
                        WINDOW_STATE = 1
                elif WINDOW_STATE == 1:
                    if 25 <= x <= 160 and 25 <= y <= 165:
                        WINDOW_STATE = 0
                        screen = pygame.display.set_mode(INTRO_WINDOW_SIZE)
                        background = pygame.transform.scale(load_image('intro.jpg'), INTRO_WINDOW_SIZE)
                        screen.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(INTRO_WINDOW_SIZE)
    start_screen()
