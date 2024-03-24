import matplotlib.pyplot as plt
import random
import Direction
import InitWindow
import SendWindow
import Delivery

global paused
paused = False
# 创建标签
text_receive = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']  

# 创建8个自上海发货的窗口
initwindows = [InitWindow.initwindow(i, (i-1, -1), None) for i in range(1, 9)]

# 创建24个字母城市的接收窗口
sendwindows_left = [SendWindow.sendwindow(text_receive[i],(-1, i)) for i in range(8)]
sendwindows_right = [SendWindow.sendwindow(text_receive[i + 8],(8, 7 - i)) for i in range(8)]
sendwindows_top = [SendWindow.sendwindow(text_receive[i + 16],(i, 8)) for i in range(8)]

# 创建1000个随机的快递
items = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
delivery_array = [Delivery.delivery(random.choice(items)) for _ in range(1000)]

# 创建画布和坐标轴
fig, ax = plt.subplots()

# 画出8x8的中转站空间
space = plt.Rectangle((0, 0), 8, 8, fill=False, color='black')

# 画出8个发货窗口
for initwindow in initwindows:
    initwindow.plt_initwindow(ax)
    initwindow.plt_label(ax)

# 画出24个接收窗口
for i in range(8):
    sendwindows_left[i].plt_sendwindow(ax)
    sendwindows_left[i].plt_label(ax)
    sendwindows_right[i].plt_sendwindow(ax)
    sendwindows_right[i].plt_label(ax)
    sendwindows_top[i].plt_sendwindow(ax)
    sendwindows_top[i].plt_label(ax)

# 绘制网格线
for i in range(8):
    plt.plot([i + 0.5, i + 0.5], [0, 8], color='gray', linestyle='--')
    plt.plot([0, 8], [i + 0.5, i + 0.5], color='gray', linestyle='--')

# 添加机器人
for robot in Direction.robots:
    robot.plt_robot(ax)
    robot.plt_label(ax)

# 设置坐标轴范围和标签
ax.set_xlim(-3, 11)
ax.set_ylim(-3, 11)
ax.set_xticks([])
ax.set_yticks([])

# 更新机器人的位置和标签
def update(frame):
    for robot in Direction.robots:
        robot.move()
        return robot.plt_robot(), robot.plt_label()

# from matplotlib.animation import FuncAnimation
# ani = FuncAnimation(fig, update, frames=range(100), interval=50, blit=True)

# def onClick(event):
#     paused ^= True
#     if paused:
#         ani.event_source.stop()
#     else:
#         ani.event_source.start()

# fig.canvas.mpl_connect('button_press_event', onClick)
# 显示图形
plt.show()