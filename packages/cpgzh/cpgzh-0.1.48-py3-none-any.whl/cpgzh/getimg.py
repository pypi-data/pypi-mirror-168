import os

from PIL import Image, ImageSequence


def get_num(s: str):
    """获取s中所有的数字"""
    s = '.'.join(s.split('.')[:-1])
    string = '0123456789.'
    ans = ''
    for w in s:
        if w in string:
            ans += w
    if '.' in ans:
        if ans[-1] != '.':
            ans = ans.split('.')
            ans = ans[0]+'.'+ans[1]
    try:
        return float(ans)
    except:
        return 0


def gif2png(image):
    """将gif动画拆解成每一帧png的函数"""
    image_dir = os.path.dirname(image)
    head, name = os.path.split(image)
    name = name[:-4]
    image_dir = os.path.join(image_dir, name)
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)
    img = Image.open(image)
    # 创建读取每一帧的迭代器
    iter_ = ImageSequence.Iterator(img)
    images = []
    for index, i in enumerate(iter_):
        now_img = os.path.join(image_dir, f"{name}({index + 1}).png")
        i.save(now_img)
        images.append(now_img)
    return images


def loadimgs(path):
    """加载并排序图片"""
    if os.path.isdir(path):
        new_lists = []
        files = os.listdir(path)
        for file in files:
            if os.path.isfile(os.path.join(path, file)):
                if file.split(".")[-1] in ["png", "jpg", "jpeg", "gif", "bmp"]:
                    new_lists.append(file)
        # 使用正则表达式提取出数字，然后对文件名进行排序
        new_lists = sorted(new_lists, key=get_num)
        # print(new_lists)
        return [os.path.join(path, i) for i in new_lists]


if __name__ == '__main__':
    imgs = loadimgs('/home/fslong/文档/青少年软件编程/00-projects/cpgzh/images/r-c')
    for img in imgs:
        print(img)
