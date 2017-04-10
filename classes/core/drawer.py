import threading
import classes.core.settings as settings
import random

def start():
    threading.Thread(target=draw).start()

def draw():
    settings.WINDOW.blit(settings.BACKGROUND_IMG, (0, 0))
    for enemy in settings.LIST_OF_ENEMIES:
        settings.WINDOW.blit(enemy.img, (enemy.x, enemy.y))
        if random.randint(1, 1000) < 2:
            enemy.shoot()
        if enemy.allocated:
            enemy.move()
        else:
            enemy.initialise(0)
        if not enemy.initialise_allocated:
            enemy.go_to_final_position()