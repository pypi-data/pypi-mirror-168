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


import pygame
now = time.localtime()
sec = time.time() % 60
now = f'{now[0]}-{now[1]}-{now[2]} {now[3]}:{now[4]}:{sec:.2f} '
print(f'{OKGREEN}{now}{ENDL}开始加载pgzero模块...')
from pgzero import music
from pgzero.clock import clock, schedule, tick
from pgzero.loaders import fonts, images, root, sounds
from pgzero.rect import Rect

now = time.localtime()
sec = time.time() % 60
now = f'{now[0]}-{now[1]}-{now[2]} {now[3]}:{now[4]}:{sec:.2f} '
print(f'{OKGREEN}{now}{ENDL}pgzero模块成功，开始加载cpgzh模块... ')
from .actor import Actor
from .animation import animate
from .data import Data
from .master import Master
from .mouse import mouse
from .pen import Font, Pen
from .keys import keys,keyboard
from .runner import get_screen, go

