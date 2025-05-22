from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import numpy as np
import filtre_kalman as Fk
from threading import Thread, Event
import random as rd
import time

BOT_SPEED = 30
COLLISION_TIME = 5
SAMPLING_RATE = 0.1


fk = Fk.FK()

collision = Event()

pos_collisions = []
pos_all = [(0, 0)]

toy = scanner.find_toy(toy_name="SB-DB73")

def policia(bot):
    bot.set_front_led(Color(255, 0, 0))
    bot.set_back_led(Color(0, 0, 255))
    # Wee Woo
    bot.set_front_led(Color(0, 0, 255))
    bot.set_back_led(Color(255, 0, 0))


def random_collision_SLAM(bot):
    bot.set_speed(BOT_SPEED)
    bot.set_heading(0)
    bot.set_stabilization(True)
    
    while True:
        heading = 180 + rd.choice([-1, 1]) * rd.randint(50)
        collision.is_set() # Arrete la mise a jour des positions pendant que le robot tourne
        bot.spin(heading, 1) 
        collision.clear() # Mettre en marche la mise a jour des positions
        bot.roll(bot.get_heading(), BOT_SPEED, 5) # Marche tout droit
        
        collision_position = pos_all[-1]
        collision_position = (collision_position['x'],  collision_position['y'])
        
        pos_collisions.append(collision_position) # Rajoute la position a laquelle il y a (normalement) eu une collision
        time.sleep(1)


def position_tracking(bot):
    dt = SAMPLING_RATE
    while not collision.is_set():
        policia(bot)
        
        velocite = bot.get_velocity()
        acceleration = bot.get_acceleration()
        if velocite and acceleration:
            vx, vy = velocite['x'], velocite['y']
            ax, ay = acceleration['x'], acceleration['y']
            vel = np.array([[vx], [vy]])
            acc = np.array([[ax], [ay]])  
            fk.kalman_predict(vel, acc) # On predit la mesure par le filtre de Kalman
            
            z = bot.get_location()
            mesure = np.array([ [z['x']], [z['y']] ])
            
            fk.kalman_update(mesure) # On met a jour le filtre de Kalman avec la poisition mesuree
            position = tuple(float(x) for x in fk.get_position.ravel())
            pos_all.append(position)
            
        time.sleep(dt)
    
    
with SpheroEduAPI(toy) as bot:
    Thread(target = position_tracking, args = (bot, )).start()

    try:
        random_collision_SLAM(bot)    
            
    except KeyboardInterrupt:
        bot.stop_roll()
        print("Programme interrompu.")
        print(pos_all)
