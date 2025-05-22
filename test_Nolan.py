from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from threading import Thread
import random as rd
import tkinter as tk
import time
from math import sqrt
import filtre_Kalman as Fk
import numpy as np
from bleak import BleakClient
import asyncio 



BOT_SPEED = 40
COLLISION_TIME = 5
SAMPLING_RATE = 0.1
fk = Fk.FK()

root = tk.Tk()
canvas = tk.Canvas(root, bg="white", width=800, height=800)
canvas.pack()

pos_collisions = []
pos_all = [(0, 0),(0,0)]  

adresse = "SB-DB73"
toy = scanner.find_toy(toy_name=adresse)


def policia(bot):
    bot.set_front_led(Color(255, 0, 0))
    bot.set_back_led(Color(0, 0, 255))
    bot.set_front_led(Color(0, 0, 255))
    bot.set_back_led(Color(255, 0, 0))


def random_collision_SLAM(bot):
    bot.set_speed(BOT_SPEED)
    bot.set_heading(0)
    bot.set_stabilization(True)
    k=0
   
    while True:
        
        heading = int(195 + rd.random() * 50 * rd.choice([-1, 1])) 
        bot.roll(bot.get_heading() +90, BOT_SPEED, COLLISION_TIME)
        x1,y1 = pos_all[-1]
        x2,y2 = pos_all[-2]
        xvector,yvector = (x1-x2,y1-y2)
        if abs(xvector)!=0 or abs(yvector) !=0 :
            k= 1 /sqrt(xvector**2 + yvector**2)
            xvector,yvector = k*xvector, k*yvector
            c = 0.3
            new_x = x1 + c * xvector
            new_y = y1 + c * yvector
            

            pos_collisions.append((new_x,new_y))

        np.save('positions.py',np.array(pos_all))


def position_tracking(bot):
    dt = SAMPLING_RATE
    
    while True:
        policia(bot)
        

        
        velocite = bot.get_velocity()
        acceleration = bot.get_acceleration()
        if velocite and acceleration:
            vx, vy = velocite['x'], velocite['y']
            ax, ay = acceleration['x'], acceleration['y']
            
            vel = np.array([[vx], [vy]])
            acc = np.array([[ax], [ay]])     
            
            fk.kalman_predict(vel, acc)
            z = bot.get_location()
            mesure = np.array([[z['x']], [z['y']]])
            
            fk.kalman_update(mesure)
            position = tuple(float(x) for x in fk.get_position.ravel())
            pos_all.append(position)
            
        time.sleep(dt)
        
            

def update_canvas():
    aggrandissement = 3
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

async def deconnecter(adresse):
    async with BleakClient(adresse) as client:
        await client.disconnect()

with SpheroEduAPI(toy) as bot:
    Thread(target=position_tracking, args=(bot,)).start()
    
    try:
        Thread(target=random_collision_SLAM, args=(bot,)).start()
        update_canvas()
        root.mainloop()
        
    except KeyboardInterrupt:
        print("Programme interrompu.")
        asyncio.run(deconnecter(adresse))
        bot.stop_roll()
        # Lancer automatiquement le fichier d'affichage à la fin

