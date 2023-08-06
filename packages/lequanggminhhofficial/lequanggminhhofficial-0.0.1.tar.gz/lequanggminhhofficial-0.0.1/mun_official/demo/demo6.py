import pygame
import mun_official
import math
from random import randint

pygame.init()

screen = pygame.display.set_mode((800, 600))
test_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
test_surface.fill((0, 0, 0, 255))

a = mun_official.Mun_official(test_surface, 400, 300)
a.set_filter('x', mun_official.filter.exponential)
a.set_filter('y', mun_official.filter.exponential)

animes = [mun_official.Mun_official(test_surface, randint(0, 800), randint(0, 600)) for i in range (200)]

playing = True
holding = False

while playing:
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            holding = True
        elif e.type == pygame.MOUSEBUTTONUP:
            holding = False

    screen.fill((255,255,255))
    a.angle = math.degrees(math.atan2(a.y-my, mx-a.x))
    for mun_official_thing in animes:
        mun_official_thing.angle = math.degrees(math.atan2(mun_official_thing.y-my, mx-mun_official_thing.x))
    if holding:
        a.pos = (mx, my)
    else:
        a.pos = a.pos
    a.update()
    for mun_official_thing in animes:
        mun_official_thing.update()
        mun_official_thing.render(screen)
    a.render(screen)
    pygame.display.flip()
    # pygame.time.wait(10)

pygame.quit()