import pygame
import sys
import os


class Sprite:
    def __init__(self, image, coords, size):
        self.image = image
        self.coords = coords
        self.size = size
        self.rect = pygame.Rect(self.coords, self.size)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = size[1]

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 2528, 1728
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    background = pygame.transform.scale(load_image('background.jpg'), size)
    screen.blit(background, (0, 0))
    file = open('data/map.txt')
    text = file.read()
    for i, row in enumerate(text.split('\n')):
        for j, block in enumerate(row):
            block_name = 'something_wrong.png'
            block_size = ['?', '?']
            current_object = -1
            print(block)
            if block in ['0', 'c', 'k']:
                continue
            elif block == '1':
                block_name = 'down_blue_block.png'
                block_size = [32, 32]
            elif block == '2':
                block_name = 'left_blue_block.png'
                block_size = [32, 32]
            elif block == '3':
                block_name = 'right_blue_block.png'
                block_size = [32, 32]
            elif block == '4':
                block_name = 'up_blue_block.png'
                block_size = [32, 32]
            elif block == '5':
                block_name = 'white-blue_block.png'
                block_size = [32, 32]
            elif block == '6':
                block_name = 'down_spikes_block.png'
                block_size = [32, 34]
            elif block == '7':
                block_name = 'up_spikes_block.png'
                block_size = [32, 34]
            elif block == '8':
                block_name = 'right_spikes_block.png'
                block_size = [34, 32]
            elif block == '9':
                block_name = 'left_spikes_block.png'
                block_size = [34, 32]
            elif block == '#':
                block_name = 'strange_splited_blue_block.png'
                block_size = [32, 32]
            elif block == 'f':
                block_name = 'flag.png'
                block_size = [28, 28]
            elif block == 's':
                block_name = 'gray_brick_block.png'
                block_size = [32, 32]
            elif block == 'l':
                block_name = 'left_spikes_block_2.png'
                block_size = [34, 32]
            elif block == 'r':
                block_name = 'right_spikes_block_2.png'
                block_size = [34, 32]
            elif block == 'u':
                block_name = 'up_spikes_block_2.png'
                block_size = [32, 34]
            elif block == 'd':
                block_name = 'down_spikes_block_2.png'
                block_size = [32, 34]
            block_pic = pygame.transform.scale(load_image('blocks\\' + block_name), block_size)
            all_sprites.add(Sprite(block_pic, (j * 32, i * 32), block_size))
    camera = Camera()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
