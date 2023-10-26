from random import  *

import pygame

RES = WIDTH, HEIGHT = 820, 660

screen = pygame.display.set_mode((WIDTH, HEIGHT))
class ParticleStyle:
    def __init__(self):
        self.particles = []
        self.star_img = pygame.image.load('dino.png').convert_alpha()
        self.star_img = pygame.transform.scale(self.star_img, (20,20 ))
        self.width = self.star_img.get_rect().width
        self.height = self.star_img.get_rect().height

    def process(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                particle[0].x+= particle[1]
                particle[0].y+= particle[2]
                particle[3]-= 0.2
                from zapitog import screen
                screen.blit(self.star_img, particle[0])

    def add_particles(self):
        for i in range(55):
            pos_x = pygame.mouse.get_pos()[0]-self.width/2
            pos_y = pygame.mouse.get_pos()[1]-self.height/2

            direction_x = randint(-8,8)
            direction_y = randint(-8,8)

            lifetime = randint(2,4)
            particle_rect = pygame.Rect(pos_x,pos_y,self.width,self.height)
            self.particles.append([particle_rect,direction_x,direction_y,lifetime])

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[3]>0]
        self.particles = particle_copy

particle_style = ParticleStyle()