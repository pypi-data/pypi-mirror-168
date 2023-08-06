def get_keys():
    '获取按键'
    import os
    import pygame.locals
    path = os.path.join(os.path.dirname(__file__), 'keys.py')
    srclines = ["class keys(IntEnum):\n    '用于获取键盘按键的类'\n"]
    for k, v in vars(pygame.locals).items():
        if k.startswith('K_'):
            if k[2].isalpha():
                k = k[2:]
            srclines.append("    %s = %d\n" % (k.upper(), v))
    srclines.append("\nclass keymods(IntEnum):\n")
    for k, v in vars(pygame.locals).items():
        if k.startswith('KMOD_'):
            srclines.append("    %s = %d\n" % (k[5:].upper(), v))
    strings = 'from enum import IntEnum\n\n'
    for s in srclines:
        if not s.endswith('\n'):
            s += '\n'
        strings += s

    strings+='''
from warnings import warn
from pgzero.keyboard import Keyboard
class Keyboard(Keyboard):
    '重写获取按键函数'
    def __getitem__(self, k):
        if isinstance(k, str):
            warn(
                f"使用了字符串作为按键名(keyboard['{k}'])，后续将会弃用这种方法，请使用keyboard[keys.{k.upper()}]这种方法 ")
            return getattr(self, k)
        else:
            try:
                return k.value in self._pressed
            except:
                print('按键判断错误，请检查按键或尝试运行get_keys.py重新获取按键。')


keyboard = Keyboard()
'''

    with open(path, 'w+', encoding='utf-8') as f:
        f.write(strings)


if __name__ == '__main__':
    get_keys()
