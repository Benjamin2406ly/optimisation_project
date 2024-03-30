import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Direction
import Delivery
import Position
import Robot
import InitWindow
import SendWindow

Direction.init()

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize = (8, 8))

# 画出8x8的中转站空间
space = plt.Rectangle((0, 0), 16, 16, fill=False, color='black')

# 动画变量
patchs = []
texts = []

# 画出8个发货窗口
for initwindow in Direction.initwindows:
    patchs.append(initwindow.plt_initwindow())
    texts.append(initwindow.plt_label())   # ha = 'center', va = 'center', color = 'green',fontsize = 8

# 画出24个接收窗口
for i in range(8):
    patchs.append(Direction.sendwindows_left[i].plt_sendwindow())
    texts.append(Direction.sendwindows_left[i].plt_label()) 
for i in range(8):
    patchs.append(Direction.sendwindows_right[i].plt_sendwindow())
    texts.append(Direction.sendwindows_right[i].plt_label())
for i in range(8):
    patchs.append(Direction.sendwindows_top[i].plt_sendwindow())
    texts.append(Direction.sendwindows_top[i].plt_label()) 

# 添加机器人
for robot in Direction.robots:
    patchs.append(robot.plt_robot())
    texts.append(robot.plt_label())   

# 添加快递列前8
for i in range(8):
    texts.append([4 + i, 21, Direction.delivery_array[i].item])

# 绘制网格线
for i in range(8):
    plt.plot([2*i + 1, 2*i + 1], [0, 16], color='gray', linestyle='--')
    plt.plot([0, 16], [2*i + 1, 2*i + 1], color='gray', linestyle='--')

# 设置坐标轴范围和标签
ax.set_xlim(-4, 20)
ax.set_ylim(-4, 22)
ax.set_xticks([])
ax.set_yticks([])

def update_patchs_and_texts(patchs, texts):
    for i in range(len(patchs)):
        if i < 8:
            patchs[i].set_x(Direction.initwindows[i].position.x)
            patchs[i].set_y(Direction.initwindows[i].position.y)
        elif 8 <= i < 16:
            patchs[i].set_x(Direction.sendwindows_left[i - 8].position.x)
            patchs[i].set_y(Direction.sendwindows_left[i - 8].position.y)
        elif 16 <= i < 24:
            patchs[i].set_x(Direction.sendwindows_right[i - 16].position.x)
            patchs[i].set_y(Direction.sendwindows_right[i - 16].position.y)
        elif 24 <= i < 32:
            patchs[i].set_x(Direction.sendwindows_top[i - 24].position.x)
            patchs[i].set_y(Direction.sendwindows_top[i - 24].position.y)
        elif 32 <= i < 40:
            patchs[i].set_x(Direction.robots[i - 32].position.x+0.5)
            patchs[i].set_y(Direction.robots[i - 32].position.y+0.5)
            patchs[i].set_edgecolor(Direction.robots[i - 32].edgecolor)
            patchs[i].set_linewidth(2)

    for text in ax.texts:
        text.remove()
    
    for i in range(len(texts)):
        if i < 8:
            texts[i][0] = Direction.initwindows[i].position.x + 1
            texts[i][1] = Direction.initwindows[i].position.y - 1
            if Direction.initwindows[i].delivery:
                texts[i][2] = str(Direction.initwindows[i].index) + ':' + str(Direction.initwindows[i].delivery.item)
        elif 8 <= i < 16:
            texts[i][0] = Direction.sendwindows_left[i - 8].position.x - 1
            texts[i][1] = Direction.sendwindows_left[i - 8].position.y + 1
        elif 16 <= i < 24:
            texts[i][0] = Direction.sendwindows_right[i - 16].position.x + 3
            texts[i][1] = Direction.sendwindows_right[i - 16].position.y + 1
        elif 24 <= i < 32:
            texts[i][0] = Direction.sendwindows_top[i - 24].position.x + 1
            texts[i][1] = Direction.sendwindows_top[i - 24].position.y + 3
        elif 32 <= i < 40:
            texts[i][0] = Direction.robots[i - 32].position.x + 1
            texts[i][1] = Direction.robots[i - 32].position.y + 1
            if Direction.robots[i - 32].item is not None:
                texts[i][2] = str(Direction.robots[i - 32].item)
            else:
                texts[i][2] = 'None'
        elif 40 <= i < 48:
            texts[i][0] = 1 + 2*(i - 40)
            texts[i][1] = 21
            if Direction.delivery_array:
                texts[i][2] = '<--'+Direction.delivery_array[i-40].item

def update_delivery(delivery_array:Direction.delivery_array, initwindow:InitWindow.initwindow):
    if initwindow.delivery is None and delivery_array:
        initwindow.set_delivery(delivery_array[0])
        if delivery_array:
            delivery_array.pop(0)

def robot_catch_delivery(robot:Robot.robot, initwindow:InitWindow.initwindow):
    if initwindow.delivery and robot.position.if_eq(initwindow.position):
        initwindow.robot_catch_delivery(robot)

def robot_send_delivery(robot:Robot.robot):
    if robot.delivery and robot.position.if_eq(robot.delivery.sendwindow_position):
        robot.send_delivery()

def main_task():
    Direction.Path_length = Direction.path_calculation()
    Direction.schedule(Direction.Path_length)

def update(frame):
    for initwindow in Direction.initwindows:
        update_delivery(Direction.delivery_array, initwindow)

    for robot in Direction.robots:
        for initwindow in Direction.initwindows:
            robot_catch_delivery(robot, initwindow)

    for robot in Direction.robots:
        robot_send_delivery(robot)  

    main_task()
    update_patchs_and_texts(patchs, texts)
    for patch in patchs:
        ax.add_patch(patch)
    for text in texts:
        ax.text(*text, ha = 'center', va = 'center', color = 'black',fontsize = 12)
    return ax,

ani = FuncAnimation(fig, update, frames=range(1000), interval=500, blit=True)

# def onClick(event):
#     paused ^= True
#     if paused:
#         ani.event_source.stop()
#     else:
#         ani.event_source.start()

# fig.canvas.mpl_connect('button_press_event', onClick)
# 显示图形
plt.show()

if not Direction.delivery_array:
    print('All delivery has been completed!')

# for i in range(8):
#     print(Direction.robots[i].item)
#     print(Direction.robots[i].delivery.item)

# print(Direction.Path_length)
# for text in texts:
#     print(text[2])
for robot in Direction.robots:
    print(robot.item)