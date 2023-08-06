from cpgzh import *
import datetime

WIDTH = 800
HEIGHT = 500


WIDTH = 800
HEIGHT = 500
font = Font()
font1 = Font()
font2 = Font()
font1.color = "red"
font2.color = "blue"
font2.bold = True
font2.angle = 180


rc = Actor("r-c", center=(700, 700))
rc.scale = 0.2
rc.animate_fps = 2
jisi = Actor("大祭司", center=(400, 400))
monv = Actor("恶魔女", center=(800, 400))
monv.flip_y = 1

master = Master()
pen = Pen()

a = 10
b = 12
c = a
a = b
b = c

a, b = b, a


def flushImages():
    "刷新造型列表"
    now = datetime.datetime.now()
    print(f"{now.time()} 刷新造型列表")
    jisi.images = jisi.images[0]


def update():
    "更新数据"
    master.run_tasks()
    # 面向鼠标
    jisi.face_to()
    # 面向演员
    rc.face_to(monv)
    # 面向一个点
    monv.face_to([0, 0])

    if jisi.collide_pixel(monv):
        print(f"碰撞点坐标：{jisi.collide_pixel(monv)}")
    if keyboard[keys.Z]:
        print(1)


def draw():
    "绘制角色"
    pen.clear()
    # 填充屏幕
    pen.rect((WIDTH / 2, HEIGHT / 2), WIDTH, HEIGHT, "white", 0)
    pen.fill("#ff88ff")
    rc.draw()
    jisi.draw()
    monv.draw()
    if "text" in dir(master.data):  # 如果data中有text属性
        pen.text(str(master.data.text), pos=(100, 100))
    # 绘制一个点
    pen.dot((300, 50), 50, "#ffff00")
    # 绘制一条线
    pen.line((250, 50), (350, 50), "#00ffff", 20)
    # 绘制圆或者圆环
    pen.circle((100, 200), 100, "#ff0000", 20)
    # 绘制椭圆或者椭圆环
    pen.ellipse((300, 200), 200, 100, "#00ff00", 20)
    # 绘制方块或者方块环
    pen.rect((500, 200), 200, 200, "#0000ff", 10, 30)
    # font样式写字
    pen.text("哈哈1", topleft=(200, 400), color="green")
    # font1样式写字
    pen.text("哈哈2", font=font1, center=(200, 450))
    # font2样式写字
    pen.text("哈哈3", font=font2, center=(200, 500))


def on_mouse_down(pos, button):
    "当鼠标按下"
    print(button, pos)
    # 按下左键刷新造型列表
    if button == mouse.keys.LEFT:
        jisi.animate_fps = 10
    # 滚轮调节动画fps
    elif button == mouse.keys.WHEEL_UP:
        jisi.animate_fps += 3
    elif button == mouse.keys.WHEEL_DOWN:
        jisi.animate_fps -= 3
    # 按下右键提问是否刷新造型
    else:
        yesOrNo = master.yes_no("是否切换造型？")
        if yesOrNo:
            jisi.animate_fps = 10
        else:
            jisi.animate_fps = 0


def on_mouse_move(pos):
    "当鼠标移动时"
    monv.x, monv.y = pos


def on_key_down(key):
    "当键盘按下"
    # 设置全屏化
    if key == keys.A:        
        master.set_fullscreen()
    # 设置窗口化
    elif key == keys.B:
        master.set_windowed()
    # 切换全屏和窗口化
    elif key == keys.C:
        master.toggle_fullscreen()
    # 隐藏鼠标
    elif key == keys.D:
        mouse.hide()
    # 显示鼠标
    elif key == keys.E:
        mouse.show()
    # 输入文本
    elif key == keys.F:
        text = master.input("请输入一个名字:")
        print(text)
    # 选择文件
    elif key == keys.G:
        text = master.select_file("请选择一个文件：")
        print(text)
    # 保存文件
    elif key == keys.H:
        text = master.select_file_save("请选择存档保存位置：")
        print(text)
    # 选择文件夹
    elif key == keys.I:
        text = master.select_dir("请选择一个文件夹:")
        print(text)
    # 是否选择框
    elif key == keys.J:
        text = master.yes_no("是否选择女装？")
        print(text)
    # 保存master的数据
    elif key == keys.K:
        master.save_data()
    # 手动加载存储的数据
    elif key == keys.L:
        # master.data.text = 'test'
        master.data_path = "测试.dat"
        master.load_data()
    # 删除保存的数据
    elif key == keys.M:
        master.del_data()
    # 设置动画的帧率
    elif key == keys.N:
        fps = master.input("请输入动画切换的速度(每s切换多少次)：")
        jisi.animate_fps = int(fps)
    # 切换造型是否切换
    elif key == keys.O:
        jisi.toggle_animate()
    # 提示信息
    elif key == keys.P:
        master.msg("提示：\n你已经换好女装了")
    # 警告信息
    elif key == keys.Q:
        master.warning("警告:\n今天的女装不太完美")
    # 错误信息
    elif key == keys.R:
        master.error("错误：\n你还没换好女装")
    # 游戏开始
    elif key == keys.S:
        print(master.data.start())
    # 获取游戏运行时常
    elif key == keys.T:
        print(master.data.get_time())
    # 停止切换造型
    elif key == keys.U:
        monv.animate_fps = 0
    # 隐藏角色
    elif key == keys.V:
        monv.hide()
    # 显示角色
    elif key == keys.W:
        monv.show()
    # 等待1s后隐藏
    elif key == keys.X:
        master.create_delay_tasks(monv.hide, 1)
    # 等待1s后显示
    elif key == keys.Y:
        master.create_delay_tasks(monv.show, 1)
    # 按下空格键
    elif key == keys.SPACE:        
        print(key) 
    # 增加透明特效  
    elif key == keys.Z:        
        jisi.transparency += 10
    # 增加颜色特效
    elif key==keys.K_1:        
        monv.color_effect += 10
        


go()
