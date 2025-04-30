from spherov2 import scanner

with scanner.find_toy() as toy:
    toy.spin(360, 1)  # Fait une rotation de 360deg en 1seconde
