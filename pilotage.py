from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import EventType 

toy = scanner.find_toy()

with SpheroEduAPI(toy) as bot:
    def on_collision(bot):
        print("Collision detected!")

    bot.register_event(EventType.on_collision, on_collision)

    bot.set_speed(60)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Program stopped.")
