import pygame
import sys
import os

all_sprites = pygame.sprite.Group()
FPS = 100
INTRO_WINDOW_SIZE = 1280, 720
ABOUT_WINDOW_SIZE = 1023, 649
GAME_WINDOW_SIZE = 1280, 720
WINDOW_STATE = 0


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Block(pygame.sprite.Sprite):
    def __init__(self, image, default_coords, size):
        super(Block, self).__init__(blocks)
        self.image = image
        self.default_coords = default_coords
        self.size = size
        self.rect = pygame.Rect(self.default_coords, self.size)


class Background(pygame.sprite.Sprite):
    def __init__(self, image, default_coords, size):
        super(Background, self).__init__()
        self.image = image
        self.default_coords = default_coords
        self.size = size
        self.rect = pygame.Rect(self.default_coords, self.size)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.default_coords[0] + self.dx // 2
        obj.rect.y = obj.default_coords[1] + self.dy // 2
        return obj.rect.x, obj.rect.y

    def update(self, target):
        self.dx = -target.rect.x - display_size[0] // 96
        self.dy = -target.rect.y - field_size[1] // 4.5 + 2


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


def start_screen():
    global screen, WINDOW_STATE
    background = pygame.transform.scale(load_image('intro.jpg'), INTRO_WINDOW_SIZE)
    screen = pygame.display.set_mode(INTRO_WINDOW_SIZE)
    screen.blit(background, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WINDOW_STATE == 0:
                    if 1070 <= x <= 1230 and 225 <= y <= 260:
                        screen = pygame.display.set_mode(display_size)
                        return
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


if __name__ == '__main__':
    pygame.init()
    display_size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    print(display_size)
    field_size = 2528, 1728
    # screen = pygame.display.set_mode((1500, 1000))
    screen = pygame.display.set_mode(display_size)
    start_screen()
    background = pygame.transform.scale(load_image('background.jpg'), field_size)
    clock = pygame.time.Clock()
    default_hero_coords = [32, display_size[0] // 2]
    hero_coords = default_hero_coords.copy()
    hero_right = AnimatedSprite(load_image("heroes/hero_run_right.png"), 8, 1, hero_coords[0], hero_coords[1])
    hero_left = AnimatedSprite(load_image("heroes/hero_run_left.png"), 8, 1, hero_coords[0], hero_coords[1])
    hero_stand_right = AnimatedSprite(load_image("heroes/hero_stand_right.png"), 1, 1, hero_coords[0], hero_coords[1])
    hero_stand_left = AnimatedSprite(load_image("heroes/hero_stand_left.png"), 1, 1, hero_coords[0], hero_coords[1])
    hero_jump_right = AnimatedSprite(load_image("heroes/hero_jump_right.png"), 5, 1, hero_coords[0], hero_coords[1])
    hero_jump_left = AnimatedSprite(load_image("heroes/hero_jump_left.png"), 5, 1, hero_coords[0], hero_coords[1])
    hero_dead = AnimatedSprite(load_image("heroes/hero_dead_right.png"), 5, 1, hero_coords[0], hero_coords[1])
    hero = hero_stand_right
    hero_vector = 'right'
    jump_cnt = 0
    forward = False
    back = False
    jump = False
    file = open('data/map.txt')
    text = file.read()
    speed = 200
    camera = Camera()
    running = True
    blocks = pygame.sprite.Group()
    run_accept_right = True
    run_accept_left = True
    jump_accept = True
    fall = True
    dead = False
    dead_cnt = 0
    checkpointed = False
    for i, row in enumerate(text.split('\n')):
        for j, block in enumerate(row):
            block_name = 'something_wrong.png'
            block_size = ['?', '?']
            current_object = -1
            if block in ['0', 'c', 'k']:
                block_name = 0
                block_size = [0, 0]
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
            if block_name:
                block_pic = pygame.transform.scale(load_image('blocks\\' + block_name), block_size)
            else:
                block_pic = 0
            Block(block_pic, (j * 32, i * 32), block_size)
    while running:
        fall = True
        background_sprite = Background(background, (0, 0), field_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and hero != hero_jump_right and run_accept_left:
                    hero = hero_left
                    hero_vector = 'left'
                    forward = False
                    back = True
                elif event.key == pygame.K_RIGHT and hero != hero_jump_right and run_accept_right:
                    hero = hero_right
                    hero_vector = 'right'
                    forward = True
                    back = False
                elif event.key == pygame.K_UP and jump_accept:
                    if hero_vector == 'right':
                        hero = hero_jump_right
                    else:
                        hero = hero_jump_left
                    jump = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    hero = hero_stand_left
                    back = False
                elif event.key == pygame.K_RIGHT:
                    hero = hero_stand_right
                    forward = False
        hero.rect.w = 20
        for block in blocks:
            if block.image != 0 and pygame.sprite.collide_rect(hero, block):
                print(1)
                if block.rect.w > 32 or block.rect.h > 32:
                    hero = hero_dead
                    dead = True
                    forward = False
                    back = False
                    jump_accept = False
                elif block.rect.w < 32 and block.rect.h < 32:
                    default_hero_coords = [20 * 32, 1000]
                elif hero_coords[0] + 32 > block.rect.x and (
                        hero_coords[1] + 67 <= block.rect.y or hero_coords[1] > block.rect.y):
                    back = False
                    run_accept_left = False
                elif hero_coords[0] < block.rect.x and (
                        hero_coords[1] + 67 <= block.rect.y or hero_coords[1] > block.rect.y):
                    forward = False
                    run_accept_right = False
                if hero_coords[1] + 64 > block.rect.y:
                    fall = False
                    jump_accept = True
            else:
                # if block.image != 0 and hero_coords[1] < block.rect.y or hero_coords[1] + 16 < block.rect.y:
                #     jump = False
                #     jump_cnt = 0
                #     fall = True
                run_accept_left = True
                run_accept_right = True

        if hero == hero_jump_right and jump_accept:
            if jump_cnt == 5:
                jump_cnt = 0
                if forward:
                    hero = hero_right

                elif back:
                    hero = hero_left
                else:
                    hero = hero_stand_right
                jump_cnt = 0
                jump_accept = False
                jump = False
                fall = True
            else:
                hero_coords[1] -= 16
            jump_cnt += 1
        if hero == hero_jump_left and jump_accept:
            if jump_cnt == 5:
                jump_cnt = 0
                if forward:
                    hero = hero_right
                elif back:
                    hero = hero_left
                else:
                    hero = hero_stand_left
                jump_cnt = 0
                jump_accept = False
                jump = False
                fall = True
            else:
                hero_coords[1] -= 16
            jump_cnt += 1

        if dead:
            dead_cnt += 1
            if dead_cnt == 4:
                dead_cnt = 0
                dead = False
                hero = hero_stand_right
                hero_coords = default_hero_coords.copy()

        else:
            if forward:
                hero_coords[0] += speed / FPS
            elif back:
                hero_coords[0] -= speed / FPS
            if forward and (jump or fall):
                hero_coords[0] += speed / FPS * 1.5
            elif back and (jump or fall):
                hero_coords[0] -= speed / FPS * 1.5
            if fall:
                hero_coords[1] += (speed * 2) / FPS

        hero.rect.x = int(hero_coords[0])
        hero.rect.y = int(hero_coords[1])
        hero.update()
        screen.fill((0, 0, 0))
        camera.update(hero)
        camera.apply(background_sprite)
        screen.blit(pygame.transform.scale(background_sprite.image,
                                           background_sprite.rect.size),
                    (background_sprite.rect.x, background_sprite.rect.y))

        for block in blocks:
            if block.image != 0:
                screen.blit(block.image, camera.apply(block))
        print(default_hero_coords)
        screen.blit(hero.image, (hero.rect.x, hero.rect.y))

        # screen.blit(pygame.transform.scale(load_image('blocks\\shadows.png'), size),
        #             (hero.rect.x + 100, hero.rect.y - display_size[1] // 2 + 192))
        clock.tick(FPS)
        pygame.display.flip()
