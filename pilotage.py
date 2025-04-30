import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

toy = scanner.find_toy()

with SpheroEduAPI(toy) as api :
    api.set_speed(100)
    api.roll(0,150,2)