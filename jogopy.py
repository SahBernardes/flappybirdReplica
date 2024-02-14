'''Replica do flapbird'''

import pygame
import os
import random

telaLargura = 300
telaAltura = 500

imgCano = pygame.transform.scale2x(pygame.image.load(os.path.join('img','pipe.png')))
imgChao = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'base.png')))
imgBackground =pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bg')))
imgsBird = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird1'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird2'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird3')))
]

pygame.font.init()
fontePontos= pygame.font.SysFont('arial', 30)

class passaro :
    imgs = imgsBird
    #Rotação do passaro
    rotacaoMax = 25
    velociddRotacao = 20
    timeAnimacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidd = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImg = 0
        self.img = self.imgs[0]

    def pular(self):
        self.velocidd = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calculando o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidd * self.tempo

        # restringindo o deslocamento
        if deslocamento > 15:
            deslocamento = 15
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacaoMax:
                self.angulo = self.rotacaoMax
        else:
            if self.angulo > -90:
                self.angulo -= self.velociddRotacao

    def desenhar(self, tela):
        # definir a img do passaro
        self.contagemImg += 1

        if self.contagemImg < self.timeAnimacao:
            self.img = self.imgs[0]
        elif self.contagemImg < self.timeAnimacao * 2:
            self.img = self.imgs[1]
        elif self.contagemImg < self.timeAnimacao * 3:
            self.img = self.imgs[2]
        elif self.contagemImg < self.timeAnimacao * 4:
            self.img = self.imgs[1]
        elif self.contagemImg >= self.timeAnimacao * 4 + 1:
            self.img = self.imgs[0]
            self.contagemImg = 0

        # quando despencar
        if self.angulo <= -70:
            self.img = self.imgs[1]
            self.contagemImg = self.timeAnimacao * 2

        # desenhar img
        imgRotacionada = pygame.transform.rotate(self.img, self.angulo)
        centroImg = self.img.get_rect(topleft=(self.x, self.y)).center
        retangulo = imgRotacionada.get_rect(center=centroImg)
        tela.blit(imgRotacionada, retangulo.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.img)

class cano:
    pass

class chao:
    pass
