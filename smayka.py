from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from threading import Thread
import random as rd
import time

BOT_SPEED = 50
COLLISION_TIME = 5

toy = scanner.find_toy(toy_name="SB-DB73")
pos_all = []
pos_collisions = []


def random_collision_SLAM(bot):
    bot.set_speed(30)
    bot.set_heading(0)
    
    while True:
        heading = int(120 + rd.random()*160)
        bot.roll(bot.get_heading() + heading, BOT_SPEED, 5)
        coll_position = bot.get_location()
        coll_position = (coll_position['x'],  coll_position['y'])
        pos_collisions.append(coll_position)
        time.sleep(1)

    
with SpheroEduAPI(toy) as bot:
    
    Thread(target = random_collision_SLAM, args = (bot)).start()

    try:
        while True:
            position = bot.get_location()
            position = (position['x'],  position['y'])
            pos_all.append(position)
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("Programme interrompu.")
        bot.stop_roll()
