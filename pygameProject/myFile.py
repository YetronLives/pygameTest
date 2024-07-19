# # import pygame.examples.aliens as al
# # import pygame.examples.chimp as chimp
# # import pygame.examples.midi as mid
# # mid.main()
# # al.main()
# # chimp.main()
# 
# # import modules
# import sys, pygame
#
# # manage external resources (currently empty)
# # game classes and functions (currently empty)
#
# # initialize the game
# pygame.init()
#
# size = width, height = 1024, 768
# speed = [5, 5]
# black = 0,0,0
# white = 255, 255, 255
#
# screen = pygame.display.set_mode(size)
#
# red_rect = pygame.Rect(0,0,50,50)
# red_surf = pygame.Surface((red_rect.h, red_rect.w))
# red_surf.fill(color=(255,0,0))
#
# clock = pygame.time.Clock()
#
# # start the main loop
# while True:
#     # listen for events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()
#
#     # update the game objects as appropriate
#     red_rect = red_rect.move(speed)
#     if red_rect.left < 0 or red_rect.right > width:
#         speed[0] = -speed[0]
#     if red_rect.top < 0 or red_rect.bottom > height:
#         speed[1] = -speed[1]
#
#     # update the screen
#     screen.fill(white)
#     screen.blit(red_surf, red_rect)
#     pygame.display.flip()
#     clock.tick(60)

