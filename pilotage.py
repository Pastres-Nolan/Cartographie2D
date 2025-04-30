from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import EventType 

toy = scanner.find_toy()
with SpheroEduAPI(toy) as bot:
    bot.set_speed(60)
    
    def oncollision(bot):
        print("Collision")
    
    bot.register_event(EventType.on_collision, oncollision)
