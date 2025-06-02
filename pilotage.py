from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import filtre_kalman as Fk
import numpy as np
from threading import Thread, Event
import random as rd
import time

class Pilotage:
    def __init__(self, toy_name="SB-DB73", bot_speed=30, collision_time=5, sampling_rate=0.1):
        self.BOT_SPEED = bot_speed
        self.COLLISION_TIME = collision_time
        self.SAMPLING_RATE = sampling_rate

        self.fk = Fk.FK()
        self.collision = Event()
        self.running = Event()
        self.pos_collisions = []
        self.pos_all = [(0, 0)]

        self.toy = scanner.find_toy(toy_name=toy_name)
        self.bot = SpheroEduAPI(self.toy)

    def policia(self):
        self.bot.set_front_led(Color(255, 0, 0))
        self.bot.set_back_led(Color(0, 0, 255))
        self.bot.set_front_led(Color(0, 0, 255))
        self.bot.set_back_led(Color(255, 0, 0))

    def random_collision_SLAM(self):
        self.bot.set_speed(self.BOT_SPEED)
        self.bot.set_heading(0)
        self.bot.set_stabilization(True)

        while not self.running.is_set():
            self.collision.set()
            self.bot.spin(90, 1)
            self.collision.clear()
            self.bot.roll(self.bot.get_heading(), self.BOT_SPEED, 5)
            collision_position = self.pos_all[-1]
            self.pos_collisions.append(collision_position)
            time.sleep(1)

    def position_tracking(self):
        dt = self.SAMPLING_RATE
        while True:
            #if not self.collision.is_set():
            self.policia()
            velocite = self.bot.get_velocity()
            acceleration = self.bot.get_acceleration()
            if velocite and acceleration:
                vx, vy = velocite['x'], velocite['y']
                ax, ay = acceleration['x'], acceleration['y']
                vel = np.array([[vx], [vy]])
                acc = np.array([[ax], [ay]])
                self.fk.kalman_predict(vel, acc)

                z = self.bot.get_location()
                mesure = np.array([[z['x']], [z['y']]])
                self.fk.kalman_update(mesure)
                position = tuple(float(x) for x in self.fk.get_position.ravel())
                self.pos_all.append(position)
                print(position)  # Debug print
            else:
                print("Collision active — pausing position update" + str(time.time())) 
            time.sleep(dt)

    def position(self):
        return self.pos_all

    def start(self):
        #self.running.clear()
        with self.bot:
            tracking_thread = Thread(target=self.position_tracking, name="TrackingThread")
            tracking_thread.start()
            try:
                self.random_collision_SLAM()
            except KeyboardInterrupt:
                self.bot.stop_roll()
                self.running.set()
                tracking_thread.join()
                print("Program interrupted.")
            finally:
            
                self.stop_moving()
                self.tracking_thread.join()


                

    def stop_moving(self):
        self.running.set()
        self.bot.stop_roll()

    def start_moving(self):
        self.running.clear()
