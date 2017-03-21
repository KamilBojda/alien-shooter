import pygame
import classes.core.weapons as weapons
class Ship:
    def __init__(self):
        self.img = pygame.image.load('resources/images/ship.png')
        self.hp = 100
        self.speed = 5
        self.bullet_speed = 50
        self.weapon = weapons.Weapon()
        self.width = 166
        self.height = 309
