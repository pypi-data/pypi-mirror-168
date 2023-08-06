import pygame
from pgzero.constants import mouse as mouse_keys


class Mouse:
    """鼠标类"""

    def __init__(self) -> None:
        """鼠标类"""
        self.keys = mouse_keys

    @staticmethod
    def get_pos():
        """获取鼠标坐标"""
        return pygame.mouse.get_pos()

    @staticmethod
    def set_pos(x, y=None):
        pygame.mouse.set_pos(x, y)

    @staticmethod
    def hide() -> None:
        """隐藏鼠标"""
        pygame.mouse.set_visible(False)

    @staticmethod
    def show() -> None:
        """显示鼠标"""
        pygame.mouse.set_visible(True)


mouse = Mouse()
