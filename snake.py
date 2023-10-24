import random

import pygame


class Snake:
    cor = (255, 255, 255)
    tamanho = (10, 10)
    velocidade = 10
    tamanho_maximo = 49 * 49

    def __init__(self):
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)

        self.corpo = [(100, 100), (90, 100), (80, 100)]

        self.direcao = 'direita'

        self.pontos = 0

    def blit(self, screen):
        for posicao in self.corpo:
            screen.blit(self.textura, posicao)


    def andar(self):

        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        if self.direcao == 'direita':
            self.corpo.insert(0,(x + self.velocidade, y))
        elif self.direcao == 'esquerda':
            self.corpo.insert(0,(x - self.velocidade, y))
        elif self.direcao == 'cima':
            self.corpo.insert(0,(x, y - self.velocidade))
        elif self.direcao == 'baixo':
            self.corpo.insert(0,(x, y + self.velocidade))

        self.corpo.pop(-1)

    def cima(self):
        if self.direcao != 'baixo':
            self.direcao = 'cima'

    def baixo(self):
        if self.direcao != 'cima':
            self.direcao = 'baixo'

    def esquerda(self):
        if self.direcao != 'direita':
            self.direcao = 'esquerda'

    def direita(self):
        if self.direcao != 'esquerda':
            self.direcao = 'direita'

    def colisao_fruta(self, fruta):
        return self.corpo[0] == fruta.posicao

    def comer(self):
        self.corpo.append((0, 0))
        self.pontos += 1
        pygame.display.set_caption(f'Snake Game | Pontos: {self.pontos}')

    def colisao(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        return x < 0 or y < 0 or x > 490 or y > 490 or cabeca in self.corpo[1:] or len(self.corpo) > self.tamanho_maximo


class Fruta:
    cor = (255, 0, 0)
    tamanho = (10, 10)

    def __init__(self, snake):
        self.textura = pygame.Surface(self.tamanho)
        self.textura.fill(self.cor)
        self.posicao = Fruta.criar_posicao(snake)

    @staticmethod
    def criar_posicao(snake):
        x = random.randint(0, 49) * 10
        y = random.randint(0, 49) * 10

        if (x,y) in snake.corpo:
            Fruta.criar_posicao(snake)
        else:
            return x, y



    def blit(self, screen):
        screen.blit(self.textura, self.posicao)


if __name__ == '__main__':
    pygame.init()

    resolution = (500, 500)
    screen = pygame.display.set_mode(resolution)

    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    black = (0, 0, 0)


    snake = Snake()
    fruta = Fruta(snake)
    fruta.blit(screen)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake.cima()
                    break
                elif event.key == pygame.K_s:
                    snake.baixo()
                    break
                elif event.key == pygame.K_a:
                    snake.esquerda()
                    break
                elif event.key == pygame.K_d:
                    snake.direita()
                    break

        if snake.colisao_fruta(fruta):
            snake.comer()
            fruta = Fruta(snake)

        if snake.colisao():
            snake = Snake()
            fruta = Fruta(snake)

        snake.andar()

        screen.fill(black)
        fruta.blit(screen)
        snake.blit(screen)

        pygame.display.update()
