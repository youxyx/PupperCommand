# 适配：原生蓝牙PS3手柄(BlueZ sixaxis补丁) | PupperCommand专用
import os
# 【关键修复】设置 pygame 使用虚拟视频驱动，解决无显示器报错
os.environ["SDL_VIDEODRIVER"] = "dummy"

from UDPComms import Publisher, Subscriber, timeout
import pygame
import time

# ===================== 原配置完全保留（不改动机器狗逻辑）=====================
MESSAGE_RATE = 20

# ===================== 初始化系统原生蓝牙PS3手柄 =====================
pygame.init()
pygame.joystick.init()

# 等待蓝牙手柄连接（容错：开机自动等待）
while pygame.joystick.get_count() == 0:
    print("等待蓝牙PS3手柄连接... 按手柄PS键配对")
    pygame.time.wait(1000)
    pygame.joystick.quit()
    pygame.joystick.init()

# 初始化第一个手柄（蓝牙PS3自动识别为js0）
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"PS3蓝牙手柄已连接: {joystick.get_name()}")

# ===================== UDP通信（完全不变）=====================
joystick_pub = Publisher(8830)
joystick_subcriber = Subscriber(8840, timeout=0.01)

# ===================== 主循环 =====================
while True:
    pygame.event.pump()  # 刷新手柄输入

    # ---------------- 原生PS3蓝牙手柄 标准映射 ----------------
    # 左摇杆
    left_x = joystick.get_axis(0)
    left_y = -joystick.get_axis(1)
    # 右摇杆
    right_x = joystick.get_axis(2)
    right_y = -joystick.get_axis(3)

    # 扳机 L2 / R2
    L2 = (joystick.get_axis(4) + 1) / 2
    R2 = (joystick.get_axis(5) + 1) / 2

    # 肩部 L1 / R1
    L1 = joystick.get_button(4)
    R1 = joystick.get_button(5)

    # 功能键 □×○△ (注意：原装PS3手柄映射通常是 0:×, 1:○, 2:△, 3:□，如果不对请互换)
    square = joystick.get_button(3)    # 原装PS3通常是3
    x = joystick.get_button(0)         # 原装PS3通常是0
    circle = joystick.get_button(1)    # 原装PS3通常是1
    triangle = joystick.get_button(2)  # 原装PS3通常是2

    # 方向键
    hat = joystick.get_hat(0)
    dpadx = hat[0]
    dpady = hat[1]

    # ---------------- 发送消息（和原代码完全一致）----------------
    msg = {
        "ly": left_y, "lx": left_x,
        "rx": right_x, "ry": right_y,
        "L2": L2, "R2": R2,
        "R1": R1, "L1": L1,
        "dpady": dpady, "dpadx": dpadx,
        "x": x, "square": square,
        "circle": circle, "triangle": triangle,
        "message_rate": MESSAGE_RATE,
    }
    joystick_pub.send(msg)

    # 接收UDP指令（PS3手柄无LED，空实现不报错）
    try:
        joystick_subcriber.get()
    except timeout:
        pass

    time.sleep(1 / MESSAGE_RATE)
