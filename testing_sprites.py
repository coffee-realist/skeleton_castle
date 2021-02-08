import os
import sys
import pygame

INTRO_WINDOW_SIZE = 1280, 720
ABOUT_WINDOW_SIZE = 1023, 649
GAME_WINDOW_SIZE = 1280, 720
WINDOW_STATE = 0
FPS = 10
image = pygame.Surface([60, 65])
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


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


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    running = True
    hero_right = AnimatedSprite(load_image("heroes/hero_run_right.png"), 8, 1, 60, 65)
    hero_left = AnimatedSprite(load_image("heroes/hero_run_left.png"), 8, 1, 60, 65)
    hero_stand_right = AnimatedSprite(load_image("heroes/hero_stand_right.png"), 1, 1, 60, 65)
    hero_stand_left = AnimatedSprite(load_image("heroes/hero_stand_left.png"), 1, 1, 60, 65)
    hero_jump_right = AnimatedSprite(load_image("heroes/hero_jump_right.png"), 5, 1, 60, 65)
    hero_jump_left = AnimatedSprite(load_image("heroes/hero_jump_left.png"), 5, 1, 60, 65)
    hero = hero_stand_right
    hero_vector = 'right'
    jump_cnt = 0
    coords = [50, 50]
    forward = False
    back = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and hero != hero_jump_right:
                        hero = hero_left
                        hero_vector = 'left'
                        forward  = False
                        back = True
                elif event.key == pygame.K_RIGHT and hero != hero_jump_right:
                        hero = hero_right
                        hero_vector = 'right'
                        forward = True
                        back = False
                elif event.key == pygame.K_UP:
                    if hero_vector == 'right':
                        hero = hero_jump_right
                    else:
                        hero = hero_jump_left
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    hero = hero_stand_left
                    back = False
                elif event.key == pygame.K_RIGHT:
                    hero = hero_stand_right
                    forward = False
        if hero == hero_jump_right:
            jump_cnt += 1
            if jump_cnt == 5:
                jump_cnt = 0
                hero = hero_stand_right
        if hero == hero_jump_left:
            jump_cnt += 1
            if jump_cnt == 5:
                jump_cnt = 0
                hero = hero_stand_left
        if forward:
            coords[0] += 5
        elif back:
            coords[0] -= 5




        hero.update()
        screen.fill('black')
        screen.blit(hero.image, coords)
        pygame.display.flip()
        clock.tick(FPS)
