import Robot

robots = []    
for i in range(8):     
    color = (255-30*i, 30*i, 0)
    robots.append(Robot.robot((0, -1), 'up', i, None, f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'))

def direction_if_oppose(self,other):
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

def robot_collision_decesion_making(robots):
    for robot in robots:
        robots_without_robot = [r for r in robots if r != robot]
        def robot_next_being_ocuppied():
            if robot.next_position().occupied:
                if robot.next_position().robot.dir == 'stop':
                    robot.set_dir('stop')
                elif robot.next_position().robot.dir != 'stop':
                    if direction_if_oppose(robot,robot.next_position().robot):
                        robot.set_dir('left')
                        robot_next_being_ocuppied()
                    else:
                        pass

        def robot_next_will_ocuppied():     
            if robot.next_position().if_eq(other_robot.next_position()):
                for other_robot in robots_without_robot:  
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


                            
                        
                
