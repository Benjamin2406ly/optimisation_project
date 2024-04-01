import Robot
import Position
import InitWindow
import SendWindow
import Delivery
import random
import numpy as np
from scipy.optimize import linear_sum_assignment

def init():
    global items, informations, initwindows, sendwindows_left, sendwindows_right, sendwindows_top, delivery_array, colors, robots, Path_length, if_optimize, if_consider_collision,num_delivery

    num_delivery = 50
    if_optimize = False
    if_consider_collision = True

    items = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
    informations = [(items[i],(-2,2*i)) for i in range(8)]+[(items[i + 8],(16,14-2*i)) for i in range(8)]+[(items[i + 16],(2*i,16)) for i in range(8)]
    delivery_array = [Delivery.delivery(random.choice(informations)) for _ in range(num_delivery)]

    initwindows = [InitWindow.initwindow(i, (2*i-2, -2), (delivery_array[i+7])) for i in range(1, 9)]

    sendwindows_left = [SendWindow.sendwindow(items[i],(-2, 2*i)) for i in range(8)]
    sendwindows_right = [SendWindow.sendwindow(items[i + 8],(16, 14 - 2*i)) for i in range(8)]
    sendwindows_top = [SendWindow.sendwindow(items[i + 16],(2*i, 16)) for i in range(8)]
 
    colors = [(255-30*i, 30*i, 0) for i in range(8)]
    robots = [Robot.robot((0 + 2*i, -2), 'up', i, delivery_array[i], f'#{colors[i][0]:02x}{colors[i][1]:02x}{colors[i][2]:02x}') for i in range(8)]

    Path_length = np.zeros((8,8))

    delivery_array = delivery_array[16:]

# path calculation
def task_rest_path(robot: Robot.robot, delivery: Delivery.delivery):
    if robot.in_task == True and delivery is not None:
        return abs(robot.position.x - delivery.sendwindow_position.x) + abs(robot.position.y - delivery.sendwindow_position.y)
    else:
        return 0
    
def Catch_delivery_path(robot: Robot.robot, initwindow: InitWindow.initwindow):
    if initwindow.delivery is not None:
        return abs(robot.position.x - initwindow.position.x) + abs(robot.position.y - initwindow.position.y)
    else:
        return 1000

def path_calculation():
    for i, robot in enumerate(robots):      # 8个机器人
        for j, initwindow in enumerate(initwindows):  # 8个初始窗口
            if robot.in_task == True:
                Path_length[i][j] = task_rest_path(robot, robot.delivery) + Catch_delivery_path(robot, initwindow) + task_rest_path(robot, initwindow.delivery)
            else:
                Path_length[i][j] = Catch_delivery_path(robot, initwindow) + task_rest_path(robot, initwindow.delivery)
    return Path_length

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

def robot_next_being_ocuppied(attempt, robot: Robot.robot, other_robot: Robot.robot):
    robot.determine_next_position()
    other_robot.determine_next_position()
    if attempt > 3:
        return
    elif robot.index == other_robot.index:
        return
    elif robot.next_position.if_eq(other_robot.position):
        if other_robot.dir == 'stop':
            robot.turn_left()
            robot.determine_next_position()
        elif other_robot.dir != 'stop':
            if direction_if_oppose(robot,other_robot):
                robot.turn_left()
                robot_next_being_ocuppied(attempt + 1, robot, other_robot)
                
def robot_next_will_ocuppied(attempt, robot: Robot.robot, other_robot: Robot.robot):
    robot.determine_next_position()
    other_robot.determine_next_position()
    if attempt > 3:
        return     
    elif robot.index == other_robot.index:
        return
    elif robot.next_position.if_eq(other_robot.next_position):    
        if direction_if_oppose(robot,other_robot):
            robot.turn_left()
            robot_next_will_ocuppied(attempt + 1, robot, other_robot)
        elif not direction_if_oppose(robot,other_robot):
            if robot.index > other_robot.index:
                other_robot.set_dir('stop')
                other_robot.determine_next_position()
            elif robot.index < other_robot.index:
                robot.set_dir('stop')
                robot.determine_next_position()

def robot_collision_decesion_making(robot: Robot.robot, robots):  
    for other_robot in robots: 
        robot_next_being_ocuppied(0, robot, other_robot)
        robot_next_will_ocuppied(0, robot, other_robot)

# move to destination
def to_destination(robot: Robot.robot, pstion: Position.position):
    if robot.position.y == -2:
        robot.set_dir('up')
    elif robot.position.y == 16:
        robot.set_dir('down')
    elif robot.position.x == -2:
        robot.set_dir('right')
    elif robot.position.x == 16:
        robot.set_dir('left')

    elif 0 < robot.position.x < 14 and 0 < robot.position.y < 14:   # 无所谓先上下还是先左右
        if robot.position.y < pstion.y:
            robot.set_dir('up')
        elif robot.position.y > pstion.y:
            robot.set_dir('down')     
        elif robot.position.x < pstion.x:
            robot.set_dir('right')
        elif robot.position.x > pstion.x:
            robot.set_dir('left')

    elif (robot.position.x == 0 and 0 < robot.position.y < 14) or (robot.position.x == 14 and 0 < robot.position.y < 14):   # 先上下
        if robot.position.y < pstion.y and robot.position.y < 16:
            robot.set_dir('up')
        elif robot.position.y > pstion.y and robot.position.y > -2:
            robot.set_dir('down')     
        elif robot.position.x < pstion.x and -2 < robot.position.y < 16:
            robot.set_dir('right')
        elif robot.position.x > pstion.x and -2 < robot.position.y < 16:
            robot.set_dir('left') 

    elif (robot.position.y == 0 and 0 < robot.position.x < 14) or (robot.position.y == 14 and 0 < robot.position.x < 14):   # 先左右
        if robot.position.x < pstion.x and robot.position.x < 16:
            robot.set_dir('right')
        elif robot.position.x > pstion.x and robot.position.x > -2:
            robot.set_dir('left')
        elif robot.position.y < pstion.y and -2 < robot.position.x < 16:
            robot.set_dir('up')
        elif robot.position.y > pstion.y and -2 < robot.position.x < 16:
            robot.set_dir('down')

    elif robot.position.x == 0 and robot.position.y == 0:   # 先右上
        if robot.position.y < pstion.y:
            robot.set_dir('up')
        elif robot.position.x < pstion.x:
            robot.set_dir('right')    
        elif robot.position.y > pstion.y:
            robot.set_dir('down')     
        elif robot.position.x > pstion.x:
            robot.set_dir('left')  

    elif robot.position.x == 14 and robot.position.y == 0:   # 先左上
        if robot.position.y < pstion.y:
            robot.set_dir('up')
        elif robot.position.x > pstion.x:
            robot.set_dir('left')    
        elif robot.position.y > pstion.y:
            robot.set_dir('down')     
        elif robot.position.x < pstion.x:
            robot.set_dir('right')

    elif robot.position.x == 0 and robot.position.y == 14:   # 先右下
        if robot.position.x < pstion.x:
            robot.set_dir('right')
        elif robot.position.y > pstion.y:
            robot.set_dir('down')    
        elif robot.position.x > pstion.x:
            robot.set_dir('left')
        elif robot.position.y < pstion.y:
            robot.set_dir('up')
    
    elif robot.position.x == 14 and robot.position.y == 14:   # 先左下
        if robot.position.x > pstion.x:
            robot.set_dir('left')
        elif robot.position.y > pstion.y:
            robot.set_dir('down')    
        elif robot.position.x < pstion.x:
            robot.set_dir('right')
        elif robot.position.y < pstion.y:
            robot.set_dir('up')

    else:
        pass
    if if_consider_collision:
        robot_collision_decesion_making(robot, robots)
    robot.move()

# schedule
def task_assign(robot: Robot.robot, initwindow: InitWindow.initwindow):
    if robot.in_task == True:
        to_destination(robot, robot.delivery.sendwindow_position)
    else:
        to_destination(robot, initwindow.position)
    
def schedule_optimize(Path_length):  
    row_i, col_i = linear_sum_assignment(Path_length)
    for i in range(8):
        if initwindows[col_i[i]].delivery is None and delivery_array is None:
            robots[row_i[i]].set_dir('stop')
        else:
            task_assign(robots[row_i[i]], initwindows[col_i[i]])

def schedule_normal():
    for i in range(8):
        task_assign(robots[i], initwindows[i])