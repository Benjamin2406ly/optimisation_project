import matplotlib.pyplot as plt
import Direction
import numpy as np

global  paused
paused = False

# 创建标签
text_send = 'from Shanghai'
text_receive = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']   

# 创建画布和坐标轴
fig, ax = plt.subplots()

# 创建一个8x8的中转站空间
space = plt.Rectangle((0, 0), 8, 8, fill=False, color='black')

# 创建8个标签为“自上海发货”的窗口
windows_bottom = [plt.Rectangle((i, -1), 1, 1, linewidth=1, edgecolor='white') for i in range(8)]

# 创建24个字母城市的接收窗口
windows_left = [plt.Rectangle((-1, i), 1, 1, linewidth=1, edgecolor='white') for i in range(8)]
windows_right = [plt.Rectangle((8, i), 1, 1, linewidth=1, edgecolor='white') for i in range(8)]
windows_top = [plt.Rectangle((i, 8), 1, 1, linewidth=1, edgecolor='white') for i in range(8)]

# 绘制网格线
for i in range(8):
    plt.plot([i + 0.5, i + 0.5], [0, 8], color='gray', linestyle='--')
    plt.plot([0, 8], [i + 0.5, i + 0.5], color='gray', linestyle='--')

# 添加标签
plt.text(4, -2, text_send, ha='center', va='center', fontsize=12)
for i in range(8):
    plt.text(-1.5, i + 0.5, text_receive[i], ha='center', va='center', fontsize=12)
    plt.text(i + 0.5, 9.5, text_receive[i + 8], ha='center', va='center', fontsize=12)
    plt.text(9.5, 7.5 - i, text_receive[i + 16], ha='center', va='center', fontsize=12)

# 添加图形元素到坐标轴
ax.add_patch(space)
for window in windows_bottom:
    ax.add_patch(window)
for window in windows_left:
    ax.add_patch(window)
for window in windows_right:
    ax.add_patch(window)
for window in windows_top:
    ax.add_patch(window)
for rob in Direction.robots:
    ax.add_patch(rob.plt_robot())

# 设置坐标轴范围和标签
ax.set_xlim(-3, 11)
ax.set_ylim(-3, 11)
ax.set_xticks([])
ax.set_yticks([])

# 更新机器人的位置和标签
def update(frame):
    # if cnt == 10:
    #     cnt = 0
    # else:
    #     cnt += 1
    for robot in (Direction.robots):
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