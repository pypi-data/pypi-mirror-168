# 对pgzero里一些功能进行重新封装和说明，用于教学
from pgzero.animation import animate as ani


def animate(object, tween='linear', duration=1, on_finished=None, **targets):
    """
    控制角色运动的功能，比如从一个地方运动到另外一个地方。\n
    object：你要运动的角色(必选)。\n
    pos：终点坐标(必选)。
    tween：运动的方式，linear就是线性的意思，还有：accelerate、decelerate、accel_decel、end_elastic、start_elastic、both_elastic、bounce_end、bounce_start、bounce_start_end等参数可选，请大家自行尝试。\n
    duration：延迟的时间，单位为s。\n
    on_finished：结束后做的事。\n
    """
    return ani(object, tween, duration, on_finished, **targets)
