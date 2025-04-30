from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from threading import Thread
import time

toy = scanner.find_toy()

with SpheroEduAPI(toy) as bot:
    def rouler():
        bot.set_speed(60)
        bot.set_heading(0)
        bot.roll(0, 60, 3)
    
    Thread(target = rouler).start()
    start_time = time.time()
    try:
        while True:
            velocity = bot.get_velocity()
            
            if velocity != None:
                print(f"vitesse x: {velocity['x']}")
                print(f"vitesse y: {velocity['y']}")
        
    except KeyboardInterrupt:
        print("Program stopped.")
        bot.stop()
