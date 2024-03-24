import Robot
import Position
import InitWindow
import SendWindow
import Delivery
import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import threading
import time

global items, informations, initwindows, sendwindows_left, sendwindows_right, sendwindows_top, delivery_array, robots, Path_length

items = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
informations = [(items[i],(-2,2*i)) for i in range(8)]+[(items[i + 8],(16,14-2*i)) for i in range(8)]+[(items[i + 16],(2*i,16)) for i in range(8)]
delivery_array = [random.choice(informations) for _ in range(1000)]

initwindows = [InitWindow.initwindow(i, (2*i-2, -2), (delivery_array[:8])) for i in range(1, 9)]

sendwindows_left = [SendWindow.sendwindow(items[i],(-2, 2*i)) for i in range(8)]
sendwindows_right = [SendWindow.sendwindow(items[i + 8],(16, 14 - 2*i)) for i in range(8)]
sendwindows_top = [SendWindow.sendwindow(items[i + 16],(2*i, 16)) for i in range(8)]

robots = []
for i in range(8):     
    color = (255-30*i, 30*i, 0)
    robots.append(Robot.robot((0 + 2*i, -2), 'up', 2*i, (None,(0,0)), f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'))

# path calculation
Path_length = np.zeros((8,8))

def task_rest_path(robot: Robot.robot, delivery: Delivery.delivery):
    if robot.in_task == True:
        return abs(robot.position.x - delivery.sendwindow_position.x) + abs(robot.position.y - delivery.sendwindow_position.y)
    else:
        return 0
    
def Catch_delivery_path(robot: Robot.robot, initwindow: InitWindow.initwindow):
    return abs(robot.position.x - initwindow.position.x) + abs(robot.position.y - initwindow.position.y)

def path_calculation():
    for i, robot in enumerate(robots):      # 8个机器人
        for j, initwindow in enumerate(initwindows):  # 8个初始窗口
            if robot.in_task == True:
                Path_length[i][j] = task_rest_path(robot, robot.delivery) + Catch_delivery_path(robot, initwindow) + task_rest_path(robot, initwindow.delivery)
            else:
                Path_length[i][j] = Catch_delivery_path(robot, initwindow) + task_rest_path(robot, initwindow.delivery)

# avoid collision
def direction_if_oppose(self: Robot.robot, other: Robot.robot):
    if self.dir == 'up' and other.dir == 'down':
        return True
    elif self.dir == 'down' and other.dir == 'up':
        return True
    elif self.dir == 'left' and other.dir == 'right':
        return True
    elif self.dir == 'right' and other.dir == 'left':
        return True
    else:
        return False

def robot_collision_decesion_making(robot: Robot.robot):
    robots_without_robot = [r for r in robots if r != robot]
    def robot_next_being_ocuppied():
        if robot.next_position().occupied:
            if robot.next_position().robot.dir == 'stop':
                robot.set_dir('stop')
            elif robot.next_position().robot.dir != 'stop':
                if direction_if_oppose(robot,robot.next_position().robot):
                    robot.set_dir('left')
                    robot_next_being_ocuppied()
    def robot_next_will_ocuppied():     
        for other_robot in robots_without_robot:      
            if robot.next_position().if_eq(other_robot.next_position()):    
                if direction_if_oppose(robot,other_robot):
                    robot.set_dir('left')
                    robot_next_will_ocuppied()
                elif not direction_if_oppose(robot,other_robot):
                    if robot.index > other_robot.index:
                        other_robot.set_dir('stop')
                    elif robot.index < other_robot.index:
                        robot.set_dir('stop')

    robot_next_being_ocuppied()
    robot_next_will_ocuppied()

# move to destination
def to_destination(robot: Robot.robot, pstion: Position.position):
    if robot.position.x < pstion.x:
        robot.set_dir('right')
    elif robot.position.x > pstion.x:
        robot.set_dir('left')
    elif robot.position.y < pstion.y:
        robot.set_dir('up')
    elif robot.position.y > pstion.y:
        robot.set_dir('down')
    else:
        pass
    robot_collision_decesion_making(robot)
    robot.move()

# schedule
def task_assign(robot: Robot.robot, initwindow: InitWindow.initwindow):
    if robot.in_task == True:
        to_destination(robot, robot.delivery.sendwindow_position)
    else:
        to_destination(robot, initwindow.position)
    
def schedule():  
    row_i, col_i = linear_sum_assignment(Path_length)
    for i in range(8):
        task_assign(robots[row_i[i]], initwindows[col_i[i]])

# update delivery
def update_delivery(i, delivery_array, initwindows):
    for initwindow in initwindows: 
        if initwindow.delivery is None:
            initwindow.set_delivery(delivery_array[i])
        
# main task
def main_task():
    def update_delivery_thread():
        i = 0
        while i < len(delivery_array):
            update_delivery(i, delivery_array, initwindows)
            i += 1

    def path_calculation_thread():
        while True:
            path_calculation()
            time.sleep(1)  

    def schedule_thread():
        while True:
            schedule()
            time.sleep(1)  

    update_delivery_thread = threading.Thread(target=update_delivery_thread)
    path_calculation_thread = threading.Thread(target=path_calculation_thread)
    schedule_thread = threading.Thread(target=schedule_thread)

    update_delivery_thread.start()
    path_calculation_thread.start()
    schedule_thread.start()

    update_delivery_thread.join()
    path_calculation_thread.join()
    schedule_thread.join()