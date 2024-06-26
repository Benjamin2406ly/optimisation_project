import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Direction
import Robot
import InitWindow
import time

Direction.init()

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize = (8, 8))

# 画出8x8的中转站空间
space = plt.Rectangle((0, 0), 16, 16, fill=False, color='black')

# 动画变量
patchs = []
texts = []
arrows = []

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
    arrows.append(robot.plt_arrow())

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

def update_patchs_and_texts(patchs, texts, arrows):
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
            patchs[i].set_linewidth(3)

    for text in ax.texts:
        text.remove()
    
    for i in range(len(texts)):
        if i < 8:
            texts[i][0] = Direction.initwindows[i].position.x + 1
            texts[i][1] = Direction.initwindows[i].position.y - 1
            if Direction.initwindows[i].delivery:
                texts[i][2] = str(Direction.initwindows[i].index) + ':' + str(Direction.initwindows[i].delivery.item)
            else:
                texts[i][2] = str(Direction.initwindows[i].index) + ':None'
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
            texts[i][0] = 2.5*(i - 40)
            texts[i][1] = 21
            if 0 <= (i-40) <len(Direction.delivery_array):
                texts[i][2] = '<--'+Direction.delivery_array[i-40].item
            elif (i-40) >= len(Direction.delivery_array):
                texts[i][2] = '<--'+'None'

    for arrow in ax.patches:
        arrow.remove()
    for i in range(len(arrows)):
        if Direction.robots[i].dir == 'up':
            arrows[i][0] = Direction.robots[i].position.x + 1
            arrows[i][1] = Direction.robots[i].position.y + 1.5
            arrows[i][2] = 0
            arrows[i][3] = 0.5
        elif Direction.robots[i].dir == 'down':
            arrows[i][0] = Direction.robots[i].position.x + 1
            arrows[i][1] = Direction.robots[i].position.y + 0.5
            arrows[i][2] = 0
            arrows[i][3] = -0.5
        elif Direction.robots[i].dir == 'left':
            arrows[i][0] = Direction.robots[i].position.x + 0.5
            arrows[i][1] = Direction.robots[i].position.y + 1
            arrows[i][2] = -0.5
            arrows[i][3] = 0
        elif Direction.robots[i].dir == 'right':
            arrows[i][0] = Direction.robots[i].position.x + 1.5
            arrows[i][1] = Direction.robots[i].position.y + 1
            arrows[i][2] = 0.5
            arrows[i][3] = 0
        elif Direction.robots[i].dir == 'stop':
            arrows[i][0] = Direction.robots[i].position.x + 1
            arrows[i][1] = Direction.robots[i].position.y + 1
            arrows[i][2] = 0
            arrows[i][3] = 0
            
def update_delivery(delivery_array:Direction.delivery_array, initwindow:InitWindow.initwindow):
    if initwindow.delivery is None and delivery_array:
        initwindow.set_delivery(delivery_array[0])
        if delivery_array:   
            delivery_array.pop(0)

def robot_catch_delivery(robot:Robot.robot, initwindow:InitWindow.initwindow):
    if initwindow.delivery and robot.position.if_eq(initwindow.position) and not robot.delivery:
        initwindow.robot_catch_delivery(robot)

def robot_send_delivery(robot:Robot.robot):
    if robot.delivery and robot.position.if_eq(robot.delivery.sendwindow_position):
        robot.send_delivery()

def main_task():
    if Direction.if_optimize:
        Direction.Path_length = Direction.path_calculation()
        Direction.schedule_optimize(Direction.Path_length)
    else:
        Direction.Path_length = Direction.path_calculation()
        Direction.schedule_normal()

start_time = time.time()

def update(frame):
    for initwindow in Direction.initwindows:
        update_delivery(Direction.delivery_array, initwindow)

    for robot in Direction.robots:
        for initwindow in Direction.initwindows:
            robot_catch_delivery(robot, initwindow)

    for robot in Direction.robots:
        robot_send_delivery(robot)  

    main_task()
    update_patchs_and_texts(patchs, texts, arrows)
    for patch in patchs:
        ax.add_patch(patch)
    for text in texts:
        ax.text(*text, ha = 'center', va = 'center', color = 'black',fontsize = 10)
    for arrow in arrows:
        if arrow is not None:
            ax.arrow(*arrow, head_width=0.4, head_length=0.4, fc='blue', ec='black')

    if all([robot.item is None for robot in Direction.robots]) and all([initwindow.delivery is None for initwindow in Direction.initwindows]) and not Direction.delivery_array:
        # ani.event_source.stop()
        plt.close()
    return ax,

ani = FuncAnimation(fig, update, frames=range(1000), interval=1000, blit=True)
plt.show()

end_time = time.time()

print('All delivery has been completed!')
print('Time:', end_time - start_time, 's')