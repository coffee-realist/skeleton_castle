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
    hero_dead = AnimatedSprite(load_image("heroes/hero_dead.png"), 5, 1, 60, 65)
    hero_run = AnimatedSprite(load_image("heroes/hero_run.png"), 8, 1, 60, 65)
    hero = hero_run
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hero == hero_dead:
                    hero = hero_run
                else:
                    hero = hero_dead
        hero.update()
        screen.fill('black')
        screen.blit(hero.image, (50, 50))
        pygame.display.flip()
        clock.tick(FPS)