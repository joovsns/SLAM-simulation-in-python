import pygame as py
import math
import random
from environment import buildMapu
from sensors import LaserSensor


environment = buildMapu((600, 1200))
environment.originalMap = environment.eksternaMapa.copy()
environment.infomap.fill((0, 0, 0))
laser = LaserSensor(200, environment.originalMap, uncertanity=(0.5, 0.01))


class Robot:
    def __init__(self, x, y, laser, mapa, infomap):
        self.x = x
        self.y = y
        self.angle = random.uniform(0, 2 * math.pi)
        self.vel = 2
        self.rot_step = math.radians(20)
        self.laser = laser
        self.map = mapa
        self.infomap = infomap  # važno za proveru crvenih tačaka

    def get_pos(self):
        return int(self.x), int(self.y)

    def move_forward(self):
        new_x = self.x + self.vel * math.cos(self.angle)
        new_y = self.y - self.vel * math.sin(self.angle)
        if not self.detect_collision((new_x, new_y)):
            self.x, self.y = new_x, new_y
        else:
            self.angle += random.choice([-1, 1]) * self.rot_step  # skreni


    def detect_collision(self, pos):
        x, y = int(pos[0]), int(pos[1])
        width, height = self.map.get_width(), self.map.get_height()
        if not (0 <= x <= width and 0 <= y <= height):
            return True  # van mape

        color_map = self.map.get_at((x, y))[:3]
        color_info = self.infomap.get_at((x, y))[:3]

        if color_map == (0, 0, 0):         # pravi zid
            return True
        if color_info == (255, 0, 0):      # već detektovani zid od strane LIDAR-a
            return True
        return False


    def update(self):
        self.laser.position = self.get_pos()
        data = self.laser.sense_obstacles()
        if data:
            environment.dataStorage(data)


robot = None
running = True


while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            color = environment.originalMap.get_at(pos)[:3]
            if color == (255, 255, 255):
                laser.position = pos
                robot = Robot(pos[0], pos[1], laser, environment.originalMap, environment.infomap)
                print("Robot postavljen na:", pos)


    if robot:
        robot.update()
        robot.move_forward()
        environment.show_sensorData()


    environment.map.blit(environment.infomap, (0, 0))
    if robot:
        py.draw.circle(environment.map, (255, 105, 180), robot.get_pos(), 5)
    py.display.update()
