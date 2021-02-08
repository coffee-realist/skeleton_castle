import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    # size = 2528, 1728
    size = 100, 100
    pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        file = open('data/map.txt')
        text = file.read()
        for row in text.split('\n'):
            for block in row:
                current_object = -1
                if block == 1:
                    pass
                elif block == 2:
                    pass
                elif block == 3:
                    pass
                elif block == 4:
                    pass
                elif block == 5:
                    pass
                elif block == 6:
                    pass
                elif block == 7:
                    pass
                elif block == 8:
                    pass
                elif block == 9:
                    pass
                elif block == '#':
                    pass
                elif block == 'f':
                    pass
                elif block == 's':
                    pass
