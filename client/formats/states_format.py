from pydantic import BaseModel


class Power:
    def __init__(self, cur_power, on_charge):
        self.cur_power = cur_power
        self.on_charge = on_charge


class Vision:
    def __init__(self, objs, locations):
        self.objs = objs
        self.locations = locations


class Obstacle:
    def __init__(self, dist):
        self.dist = dist


class ObstacleInput(BaseModel):
    dist: str


class Body:
    def __init__(self, hori_rot, vert_rot):
        self.hori_rot = hori_rot
        self.vert_rot = vert_rot


class BodyInput(BaseModel):
    hori_rot: int
    vert_rot: int
