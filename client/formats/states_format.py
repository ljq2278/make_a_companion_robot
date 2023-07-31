from pydantic import BaseModel


class Kernel:
    def __init__(self, voltage):
        self.voltage = voltage


class KernelInput(BaseModel):
    voltage: str

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
