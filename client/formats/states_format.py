from pydantic import BaseModel


class Others:
    def __init__(self, us_dist, voltage, person_near):
        self.us_dist = us_dist
        self.voltage = voltage
        self.person_near = person_near


class OthersInput(BaseModel):
    us_dist: str
    voltage: float
    person_near: bool


class Body:
    def __init__(self, hori_rot, vert_rot):
        self.hori_rot = hori_rot
        self.vert_rot = vert_rot


class BodyInput(BaseModel):
    hori_rot: int
    vert_rot: int
