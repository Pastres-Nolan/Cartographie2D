from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import filtre_kalman as Fk
from math import sqrt
import numpy as np
from threading import Thread, Event
import random as rd
import time

#SB-9A4B
#SB-DB73
class Pilotage:
    def __init__(self, toy_name="SB-DB73", bot_speed=25, collision_time=5, sampling_rate=0.2):
        self.THRESHHOLD = 2
        self.BOT_SPEED = bot_speed
        self.COLLISION_TIME = collision_time
        self.SAMPLING_RATE = sampling_rate
        self.EPOCH = time.time()

        self.fk = Fk.FK()
        self.collision = False
        self.running = Event()
        self.pos_collisions = []
        self.pos_all = [(0, 0), (0, 0)]

        self.toy = scanner.find_toy(toy_name=toy_name)
        self.bot = SpheroEduAPI(self.toy)


    def policia(self):

        self.bot.set_front_led(Color(255, 0, 0))
        self.bot.set_back_led(Color(0, 0, 255))
        #Wee Woo
        self.bot.set_front_led(Color(0, 0, 255))
        self.bot.set_back_led(Color(255, 0, 0))


    def random_collision_SLAM(self):

        self.bot.set_speed(self.BOT_SPEED)
        self.bot.set_heading(0)
        self.bot.set_stabilization(True)
       
        while not self.running.is_set(): 
            if self.BOT_SPEED and (time.time()-self.EPOCH) >7: # permet de ne pas prendre le départ du robot comme point de collision (le départ est à 4-5 secondes)
                collision_position = self.pos_all[-1]
                self.pos_collisions.append(collision_position)
                self.bot.roll(self.bot.get_heading() + 175 + 50 * rd.randint(-1, 1), self.BOT_SPEED, 1)
                for i in range(5): # une collion est prise toutes les 1 +5 secondes (en espérant que le robot touche un mur avant de prendre ce point)
                    self.bot.roll(self.bot.get_heading(), self.BOT_SPEED, 1)
            time.sleep(1)


    def position_tracking(self):
        dt = self.SAMPLING_RATE
        while True:
            self.policia()
            velocite = self.bot.get_velocity()
            acceleration = self.bot.get_acceleration()
            if velocite and acceleration :
                
                self.recoit_donnees = True
                vx, vy = velocite['x'], velocite['y']
                ax, ay = acceleration['x'], acceleration['y']
                vel = np.array([[vx], [vy]])
                acc = np.array([[ax], [ay]])
                self.fk.kalman_predict(vel, acc)

                z = self.bot.get_location()
                mesure = np.array([ [z['x']], [z['y']] ])
                self.fk.kalman_update(mesure)
                position = tuple(float(x) for x in self.fk.get_position.ravel())
                self.pos_all.append(position)
                self.pos_all.pop(0)

                time.sleep(dt)


    def position(self):
        return self.pos_all[-1]


    def start(self):
        with self.bot:
            Thread(target=self.position_tracking).start()
            try:
                self.random_collision_SLAM()
            except KeyboardInterrupt:
                self.bot.stop_roll()
                print("Program interrupted.")


    def stop_moving(self):
        self.BOT_SPEED = 0
        self.running.clear()


    def start_moving(self):
        self.running.clear()
        self.BOT_SPEED = 30