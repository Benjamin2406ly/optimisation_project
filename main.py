import matplotlib.pyplot as plt
import Direction

global paused
paused = False

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize = (8, 8))

# 画出8x8的中转站空间
space = plt.Rectangle((0, 0), 16, 16, fill=False, color='black')

# 画出8个发货窗口
for initwindow in Direction.initwindows:
    initwindow.plt_initwindow(ax)
    initwindow.plt_label(ax)

# 画出24个接收窗口
for i in range(8):
    Direction.sendwindows_left[i].plt_sendwindow(ax)
    Direction.sendwindows_left[i].plt_label(ax)
    Direction.sendwindows_right[i].plt_sendwindow(ax)
    Direction.sendwindows_right[i].plt_label(ax)
    Direction.sendwindows_top[i].plt_sendwindow(ax)
    Direction.sendwindows_top[i].plt_label(ax)

# 添加机器人
for robot in Direction.robots:
    robot.plt_robot(ax)
    robot.plt_label(ax)

# 绘制网格线
for i in range(8):
    plt.plot([2*i + 1, 2*i + 1], [0, 16], color='gray', linestyle='--')
    plt.plot([0, 16], [2*i + 1, 2*i + 1], color='gray', linestyle='--')

# 设置坐标轴范围和标签
ax.set_xlim(-4, 20)
ax.set_ylim(-4, 20)
ax.set_xticks([])
ax.set_yticks([])

# 更新机器人的位置和标签
def update(frame):
    Direction.main_task()
    for robot in Direction.robots:
        rectangle = plt.Rectangle((robot.position.x + 0.5, robot.position.y + 0.5), 1, 1, color=robot.color, alpha=1) 
        label = ax.text(robot.position.x + 1, robot.position.y + 1, str(robot.item), ha='center', va='center', color='black', fontsize=8)
        return rectangle, label

from matplotlib.animation import FuncAnimation
ani = FuncAnimation(fig, update, frames=range(100), interval=50, blit=True)

# def onClick(event):
#     paused ^= True
#     if paused:
#         ani.event_source.stop()
#     else:
#         ani.event_source.start()

# fig.canvas.mpl_connect('button_press_event', onClick)
# 显示图形
plt.show()