# this module is used for keyboard control
# when using this module, you have to click on the pygame 
# window before you start pressing any keyboard keys

import pygame


def init():
    pygame.init()
    window = pygame.display.set_mode((400, 400))

def get_key(key_name):
    answer = False
    for event in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        answer = True
    pygame.display.update()
    return answer

def destroy_py_game_window():
    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    init()