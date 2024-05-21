import json

import pygame
#import game
from constants import *
from entities import PhysicsEntity

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]


class Player(PhysicsEntity):  # Inherit from PhysicsEntity
    def __init__(self, game, pos=(0, 0), size=(16, 16)):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.acceleration = [0, 0]

        # Animation frames
        '''
        self.animation_frames = [
            pygame.transform.scale(pygame.image.load("assets/player/frame_1.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_2.png").convert_alpha(), size),
            pygame.transform.scale(pygame.image.load("assets/player/frame_3.png").convert_alpha(), size)
        ]
        # Animation variables
        self.current_frame = 0
        self.frame_delay = 350
        self.last_frame_time = 0
        
        self.image = self.animation_frames[self.current_frame]
        '''

        self.lives = 3
        self.score = 0
        self.coins = 0

    def savePlayer(self):
        directory = "saves/"
        file = open(directory + 'playerSave.json', 'w')

        data = {}
        data['LIVES'] = self.lives
        data['SCORE'] = self.score
        data['COINS'] = self.coins

    def loadPlayer(self):
        directory = "saves/"
        file = open(directory + 'playerSave.json', 'r')
        data = json.load(file)

        self.lives = data['LIVES']
        self.score = data['SCORE']
        self.coins = data['COINS']

    def loadNewPlayer(self):
        self.lives = 3
        self.score = 0
        self.coins = 0

    def update(self, movement=(0,0)):
        super().update()
        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else: self.set_action('idle')

        # self.score += 10
        # self.coins += 1

    def updateVelocity(self):
        # Apply acceleration to velocity
        self.velocity[0] += self.acceleration[0] * 1/10

        #self.velocity[1] = max(-5, self.velocity[1])
        if self.velocity[0] > 5:
            self.velocity[0] = 5
        if self.velocity[0] < -5:
            self.velocity[0] = -5

        # Apply friction to velocity for smooth stopping
        self.velocity[0] *= (1 - FRICTION)

    def move(self):
        self.updateVelocity()
        super().move()

        # Boundary checks to prevent the player from moving out of the screen
        if self.pos[0] < self.game.render_camera[0]:
            self.pos[0] = self.game.render_camera[0]

    def checkEvents(self, eventList):
        for event in eventList:
            # Movement with W A S D and arrows
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    # jump only if player is on the ground
                    #if self.velocity[1] == 0:
                    self.velocity[1] = -PLAYER_SPEED * 4
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.velocity[1] = PLAYER_SPEED
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.acceleration[0] > 0:
                        self.acceleration[0] = 0
                    else:
                        self.acceleration[0] = -PLAYER_SPEED
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.acceleration[0] < 0:
                        self.acceleration[0] = 0
                    else:
                        self.acceleration[0] = PLAYER_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.velocity[1] = 0
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.velocity[1] = 0
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.acceleration[0] == 0:
                        self.acceleration[0] = PLAYER_SPEED
                    else:
                        self.acceleration[0] = 0
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.acceleration[0] == 0:
                        self.acceleration[0] = -PLAYER_SPEED
                    else:
                        self.acceleration[0] = 0

    '''
    def render(self, surf):
        surf.blit(self.image, self.pos)
    '''
