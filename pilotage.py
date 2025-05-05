from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from threading import Thread
import time
from math import*

toy = scanner.find_toy()


with SpheroEduAPI(toy) as bot:
    def rouler():
        bot.set_speed(60)
        bot.set_heading(0)
        bot.roll(0, 100, 20)
    
    Thread(target = rouler).start()
    epoch = time.time()
    
    try:
        while True:
            velocity = bot.get_velocity()
            
            if velocity != None:
                vitesse = sqrt(velocity['x']**2 + velocity['y']**2)
                if vitesse <0.5:
                    print("NOOoooOOOOo la polIiiciiiaaaa!" , time.time() - epoch)
                time.sleep(0.5)
        
    except KeyboardInterrupt:
        print("Program stopped.")
