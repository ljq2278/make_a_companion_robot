from pydantic import BaseModel


class Others:
    def __init__(self, us_dist, voltage, person_near, head_hori, head_vert, body_direct, last_async_task, last_async_task_state, last_async_task_result):
        self.us_dist = us_dist
        self.voltage = voltage
        self.person_near = person_near
        self.head_hori = head_hori
        self.head_vert = head_vert
        self.body_direct = body_direct
        self.last_async_task = last_async_task
        self.last_async_task_state = last_async_task_state
        self.last_async_task_result = last_async_task_result


class OthersInput(BaseModel):
    us_dist: int
    voltage: float
    person_near: bool
    head_hori: int
    head_vert: int
    body_direct: int
    last_async_task: str
    last_async_task_state: str
    last_async_task_result: str
