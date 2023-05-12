import math
from map import Map


class Odemetry:
    def __init__(self):
        # Constants (mm)
        self.differentialWidth = 217
        self.distToDifferentialCenter = self.differentialWidth / 2
        self.wheelRadius = 40
        self.wheelCircumference = 2 * math.pi * self.wheelRadius
        # Variable
        self.x = 0
        self.y = 0
        self.theta = 0
        self.map = Map()

    '''
    Note down the current coordinates on the map
    '''
    def border(self):
        self.map.addPoint(self.x, self.y)

    '''
    Solves odometry
    '''
    def solve(self, left, right):
        distance_left = self.encoder_to_distance_delta(left)
        distance_right = self.encoder_to_distance_delta(right)
        delta_theta = self.solve_delta_theta(distance_left, distance_right)
        self.solve_coordinates(delta_theta, distance_left, distance_right)

    '''
    Convert degree value from encoder to distance traveled in millimeters
    '''
    def encoder_to_distance_delta(self, delta):
        return delta / 360 * self.wheelCircumference

    '''
    Solves the change in rotation
    '''
    def solve_delta_theta(self, dist_left, dist_right):
        distance_difference = dist_right - dist_left
        delta_theta = distance_difference / (2 * self.distToDifferentialCenter)
        return delta_theta

    '''
    Solves the new x,y coordinates
    '''
    def solve_coordinates(self, delta_theta, dist_left, dist_right):
        self.theta += delta_theta
        distance = (dist_left + dist_right) / 2
        delta_x = distance * math.cos(self.theta)
        delta_y = distance * math.sin(self.theta)
        self.x += delta_x
        self.y += delta_y
