from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
import time
import threading

toy = scanner.find_toy()

def rouler(bot):
    bot.roll(0, 200, 5)  # roule à 200 pendant 5 secondes

with SpheroEduAPI(toy) as bot:
    bot.set_main_led(Color(r=0, g=255, b=0))

    threading.Thread(target=rouler, args=(bot,)).start()

    try:
        while True:
            velocity = bot.get_velocity()
            #print(f"Vitesse: {velocity}",type(velocity))

            if velocity != None:
                if abs(velocity['x'])<1:
                    print("collision x")
                  
                elif abs(velocity['y'])<1:
                    print("collision y")
                
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program stopped.")
