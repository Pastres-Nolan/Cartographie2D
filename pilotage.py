from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from threading import Thread
import random as rd
import tkinter as tk
import time
from math import sqrt

BOT_SPEED = 40
COLLISION_TIME = 5
SAMPLING_RATE = 0.1

# Initialisation de l'interface tkinter
root = tk.Tk()
canvas = tk.Canvas(root, bg="white", width=800, height=800)
canvas.pack()

pos_collisions = []
pos_all = [(0, 0)]  # Centre du canvas pour éviter les valeurs négatives

toy = scanner.find_toy(toy_name="SB-DB73")


def policia(bot):
    bot.set_front_led(Color(255, 0, 0))
    bot.set_back_led(Color(0, 0, 255))
    bot.set_front_led(Color(0, 0, 255))
    bot.set_back_led(Color(255, 0, 0))


def random_collision_SLAM(bot):
    bot.set_speed(BOT_SPEED)
    bot.set_heading(0)
    bot.set_stabilization(True)
    
    while True:
        
        heading = int(195 + rd.random() * 50 * rd.choice([-1, 1])) 
        bot.roll(bot.get_heading() + 120, BOT_SPEED, COLLISION_TIME)
        time.sleep(SAMPLING_RATE)


def position_tracking(bot):
    dt = SAMPLING_RATE
    
    while True:
        velocite = bot.get_velocity()
        acc = bot.get_acceleration()
        policia(bot)
        
        if velocite and acc:
            vx, vy = velocite['x'], velocite['y']
            x_initial, y_initial = pos_all[-1]
            
            accx, accy = acc['x'], acc['y']
            x = x_initial + vx * dt + (1/2) * accx * dt**2
            y = y_initial + vy * dt + (1/2) * accy * dt**2
            pos_all.append((x, y))
            
            
            if sqrt(vx**2 + vy**2) < 3:
                pos_collisions.append((x, y))
                print(pos_collisions)
        time.sleep(SAMPLING_RATE)


def update_canvas():
    aggrandissement = 8
    decalage = 400
    rayon = 5
    
    canvas.delete("all")

    for i in range(1, len(pos_all)):
        x1, y1 = pos_all[i - 1]
        x2, y2 = pos_all[i]
        x1p = x1 * aggrandissement + decalage
        x2p = x2 * aggrandissement + decalage
        y1p = y1 * aggrandissement + decalage
        y2p = y2 * aggrandissement + decalage
        canvas.create_line(x1p, y1p, x2p, y2p, fill="blue")
    
   
    for (xc, yc) in pos_collisions:
        x1c = xc * aggrandissement + decalage - rayon
        x2c = xc * aggrandissement + decalage + rayon
        y1c = yc * aggrandissement + decalage - rayon
        y2c = yc * aggrandissement + decalage + rayon
        canvas.create_oval(x1c, y1c, x2c, y2c, fill='red')
    
    root.after(100, update_canvas)


with SpheroEduAPI(toy) as bot:
    Thread(target=position_tracking, args=(bot,)).start()
    
    try:
        Thread(target=random_collision_SLAM, args=(bot,)).start()
        update_canvas()
        root.mainloop()
        
    except KeyboardInterrupt:
        print("Programme interrompu.")
        bot.stop_roll()