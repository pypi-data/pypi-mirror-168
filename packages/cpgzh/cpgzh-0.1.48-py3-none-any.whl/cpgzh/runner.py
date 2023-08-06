import os
import sys

import pygame
from pgzero.game import PGZeroGame
from .keys import keyboard
from pgzero.runner import prepare_mod

import time

HEADER = '\033[1;95m'
OKBLUE = '\033[1;94m'
OKGREEN = '\033[1;92m'
OKRED = '\033[1;31m'
WARNING = '\033[1;93m'
FAIL = '\033[1;91m'
ENDL = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[1;4m'


mod = sys.modules["__main__"]
try:
    WIDTH = mod.WIDTH
    HEIGHT = mod.HEIGHT
    pygame.init()
    w, h = pygame.display.get_desktop_sizes()[0]
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{int((w-WIDTH)/2)},{int((h-HEIGHT)/2)}'
except:
    os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
finally:
    now = time.localtime()
    sec = time.time() % 60
    now = f'{now[0]}-{now[1]}-{now[2]} {now[3]}:{now[4]}:{sec:.2f} '
    print(f'{OKGREEN}{now}{ENDL}cpgzh模块加载成功，开始游戏加载主程序...')
    prepare_mod(mod)


def go():
    """启动游戏引擎"""
    if getattr(sys, '_pgzrun', None):
        return
    app = PGZeroGame(mod)
    app.keyboard = keyboard
    now = time.localtime()
    sec = time.time() % 60
    now = f'{now[0]}-{now[1]}-{now[2]} {now[3]}:{now[4]}:{sec:.2f} '
    print(f'{OKGREEN}{now}{ENDL}主程序加载成功，启动游戏...')
    try:
        app.mainloop()
    finally:
        pygame.display.quit()
        pygame.mixer.quit()
        now = time.localtime()
        sec = time.time() % 60
        now = f'{now[0]}-{now[1]}-{now[2]} {now[3]}:{now[4]}:{sec:.2f} '
        print(f'{OKGREEN}{now}{ENDL}游戏结束，谢谢使用。')


def get_screen():
    """返回当前游戏所在的屏幕"""
    mod = sys.modules["__main__"]
    return mod.screen
