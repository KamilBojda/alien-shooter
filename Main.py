import pygame
from pygame.locals import *
import sys
import classes.core.ship as ships
import classes.core.settings as settings
import classes.core.levels as levels
import random
import classes.core.weapons as weapons
pygame.init()
pygame.display.set_caption('Alien Shooter')
# R G B colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

clock = settings.CLOCK

ship = ships.Ship()
ship.rect.centerx = settings.WINDOW_WIDTH // 2
ship.rect.bottom = settings.WINDOW_HEIGHT

def initialiseGame():
    #adding weapons
    settings.LIST_OF_WEAPONS.append(weapons.Weapon('Single',1,3,'resources/images/single-shot.png'))

    #adding levels
    settings.LIST_OF_LEVELS.append(levels.Level1())
    settings.LIST_OF_LEVELS.append(levels.Level2())
    settings.LIST_OF_LEVELS.append(levels.Level3())
    settings.LIST_OF_LEVELS.append(levels.Level4())
    settings.LIST_OF_LEVELS.append(levels.Level5())
    settings.LIST_OF_LEVELS.append(levels.Level6())
    settings.LIST_OF_LEVELS.append(levels.Level7())
    settings.LIST_OF_LEVELS.append(levels.Level8())
    settings.LIST_OF_LEVELS.append(levels.Level9())
    settings.LIST_OF_LEVELS.append(levels.Level10())

    #adding first weapon
    ship.weapon = settings.LIST_OF_WEAPONS[0]

initialiseGame()
CURRENT_LEVEL = settings.LIST_OF_LEVELS[settings.LEVEL_COUNTER]

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def message_display(text, x, y, font):
    largeText = pygame.font.Font('freesansbold.ttf', font)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    settings.WINDOW.blit(TextSurf, TextRect)


def gameLoop():
    SCORE = 0
    gameExit = False
    gameOver = False


    while not gameExit:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            else:
                ship.react(event)
        settings.WINDOW.blit(settings.BACKGROUND_IMG,(0,0))

        ship.update()
        ship.draw()

        #drawing bullets
        for bullet in settings.BULLETS:
            bullet.update()
            bullet.draw()
            hit_group = pygame.sprite.spritecollide(bullet, settings.LIST_OF_ENEMIES, False)
            for enemy in hit_group:
                enemy.hit(ship.weapon.dmg, settings.LEVEL_COUNTER)
                bullet.kill()
        for bullet in settings.LIST_OF_ENEMY_BULLETS:
            bullet.update()
            bullet.draw()
            if pygame.sprite.collide_rect(ship, bullet) and ship.lives > 0:
                bullet.kill()
                ship.lives -= 1
                ship.kill()
            elif pygame.sprite.collide_rect(ship, bullet):
                ship.kill()
                gameOver = True

        #checking if you pass the level:
        if not settings.LIST_OF_ENEMIES and settings.LEVEL_WIN:
            settings.LEVEL_COUNTER+=1
            print('Level ' + str(settings.LEVEL_COUNTER + 1))
            if settings.LEVEL_COUNTER < len(settings.LIST_OF_LEVELS):
                CURRENT_LEVEL = settings.LIST_OF_LEVELS[settings.LEVEL_COUNTER]
                CURRENT_LEVEL.start()
            else:
                print('Wygrałeś grę')

        #rysowanie przeciwnikow
        for enemy in settings.LIST_OF_ENEMIES:
            enemy.draw()
            if not enemy.allocated:
                enemy.initialise(settings.LEVEL_COUNTER)
            elif not enemy.initialise_allocated:
                enemy.go_to_final_position()
            elif enemy.attack_flag:
                enemy.attack()
            else:
                enemy.move()
            enemy.shoot()

        #drawing explosions
        for explosion in settings.LIST_OF_EXPLOSIONS:
            if explosion.counter == 0:
                explosion.kill()
            settings.WINDOW.blit(settings.EXPLOSION_IMG,(explosion.rect.x,explosion.rect.y))
            explosion.counter -= 1

        #drawing available bonuses
        for bonus in settings.BONUSES_LIST:
            bonus.update()
            bonus.draw()
            #checking if player collected bonus
            if pygame.sprite.collide_rect(ship, bonus):
                bonus.action()
                bonus.kill()

        #columns
        settings.WINDOW.blit(settings.COLUMN_IMG,(0,0))
        settings.WINDOW.blit(settings.COLUMN_IMG,(settings.WINDOW_WIDTH-100,0))


        #messages
        #right side
        message_display("Lives: {}".format(ship.lives), (settings.WINDOW_WIDTH - 50), (settings.WINDOW_HEIGHT - 570), 24)
        message_display("Speed: {}".format(ship.speed), (settings.WINDOW_WIDTH - 50), (settings.WINDOW_HEIGHT - 530), 14)
        message_display("Bullets: {}".format(ship.max_bullets), (settings.WINDOW_WIDTH - 50), (settings.WINDOW_HEIGHT - 490), 14)
        message_display("Weapon:", (settings.WINDOW_WIDTH - 50), (settings.WINDOW_HEIGHT - 430), 14)
        message_display("{}({})".format(ship.weapon.name,ship.weapon.dmg), (settings.WINDOW_WIDTH - 50), (settings.WINDOW_HEIGHT - 410), 14)
        #left side
        message_display("Level: {}".format(settings.LEVEL_COUNTER+1), (50), (settings.WINDOW_HEIGHT - 570), 23)
        message_display("Enemies: {}".format(len(settings.LIST_OF_ENEMIES)), (50), (settings.WINDOW_HEIGHT - 530), 15)

        if gameOver:
            message_display("Game over!", (settings.WINDOW_WIDTH // 2), (settings.WINDOW_HEIGHT // 2), 24)
            settings.reset()
        if settings.LEVEL_COUNTER == 9:
            message_display("Boss HP: {}".format(settings.BOSS_HP), (settings.WINDOW_WIDTH/2), (20),24)
        pygame.display.flip()
        clock.tick(settings.CLOCK_RATE)
gameLoop()
pygame.quit()
quit()
