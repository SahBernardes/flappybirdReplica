'''Replica do flapbird'''

import pygame
import os
import random

telaLargura = 400
telaAltura = 600

imgCano = pygame.transform.scale2x(pygame.image.load(os.path.join('img','pipe.png')))
imgChao = pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'base.png')))
imgBackground =pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bg.png')))
imgsBird = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('img', 'bird3.png')))
]

pygame.font.init()
fontePontos = pygame.font.SysFont('arial', 30)

class Passaro :
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
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidd * self.tempo

        # restringindo o deslocamento
        if deslocamento > 16:
            deslocamento = 16
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
        if self.angulo <= -80:
            self.img = self.imgs[1]
            self.contagemImg = self.timeAnimacao * 2

        # desenhar img
        imgRotacionada = pygame.transform.rotate(self.img, self.angulo)
        centroImg = self.img.get_rect(topleft=(self.x, self.y)).center
        retangulo = imgRotacionada.get_rect(center=centroImg)
        tela.blit(imgRotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Cano:
    distancia = 200
    velocidd = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.canoTopo = pygame.transform.flip(imgCano, False, True)
        self.canoBase = imgCano
        self.passou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posTopo = self.altura - self.canoTopo.get_height()
        self.posBase = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidd

    def desenhar(self, tela):
        tela.blit(self.canoTopo, (self.x, self.posTopo))
        tela.blit(self.canoBase, (self.x, self.posBase))

    def colidir(self, passaro):
        passaroMask = passaro.get_mask()
        topoMask = pygame.mask.from_surface(self.canoTopo)
        baseMask = pygame.mask.from_surface(self.canoBase)

        distanciaTopo = (self.x - passaro.x, self.posTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posBase - round(passaro.y))

        topoPonto = passaroMask.overlap(topoMask, distanciaTopo)
        basePonto = passaroMask.overlap(baseMask, distanciaBase)

        if basePonto or topoPonto:
            return True
        else:
            return False

class Chao:
    velocidade = 5
    largura = imgChao.get_width()
    img = imgChao

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.largura

    def mover(self):
        self.x0 -= self.velocidade
        self.x1 -= self.velocidade

        if self.x0 + self.largura < 0:
            self.x0 = self.x1 + self.largura
        elif self.x1 + self.largura < 0:
            self.x1 =self.x0 + self.largura

    def desenhar(self, tela):
        tela.blit(self.img, (self.x0, self.y))
        tela.blit(self.img, (self.x1, self.y))

def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(imgBackground, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    txt = fontePontos.render(f'Pontuação : {pontos}', 1, (255, 255, 255))
    tela.blit(txt, (telaLargura - 10 - txt.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    #função principal
    passaros = [Passaro(230, 250)]
    chao = Chao(530)
    canos = [Cano(500)]
    tela = pygame.display.set_mode((telaLargura, telaAltura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #interação do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                   for passaro in passaros:
                        passaro.pular()

        #movendo as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionarCano = False
        removerCanos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionarCanos = True
            cano.mover()
            if cano.x + cano.canoTopo.get_height() < 0:
                removerCanos.append(cano)

        if adicionarCano:
            pontos += 1
            canos.append(Cano(500))
        for cano in removerCanos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.img.get_height()) > chao.y or passaro. y < 0:
                passaros.pop(i)

        desenharTela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()
