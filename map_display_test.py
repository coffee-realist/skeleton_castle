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
                    block_name = 'down_blue_block.png'
                elif block == 2:
                    block_name = 'left_blue_block.png'
                elif block == 3:
                    block_name = 'right_blue_block.png'
                elif block == 4:
                    block_name = 'up_blue_block.png'
                elif block == 5:
                    block_name = 'white-blue_block.png'
                elif block == 6:
                    block_name = 'down_spikes_block.png'
                elif block == 7:
                    block_name = 'up_spikes_block.png'
                elif block == 8:
                    block_name = 'right_spikes_block.png'
                elif block == 9:
                    block_name = 'left_spikes_block.png'
                elif block == '#':
                    block_name = 'strange_splited_block.png'
                elif block == 'f':
                    block_name = 'flag.png'
                elif block == 's':
                    block_name = 'gray_brick_block.png'
                elif block == 'l':
                    block_name = 'left_spikes_block_2.png'
                elif block == 'r':
                    block_name = 'right_spikes_block_2.png'
                elif block == 'u':
                    block_name = 'up_spikes_block_2.png'
                elif block == 'd':
                    block_name = 'down_spikes_block_2.png'
