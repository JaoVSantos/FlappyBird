# Principais bibliotecas para o projeto

import pygame  # biblioteca para games do python
import os  # Biblioteca para ligar o IDLE ao sistema(Computador)
import random  # Biblioteca randomica para criarmos situação diferentes no game.

# Constantes para definimos alguns padroes do jogo

TELA_LARGURA = 500  # constante para largura da tela em pixels
TELA_ALTURA = 700  # constnate para altura da tela em pixels

# Constante com o pygame que usamos para escalar a imagem e também baixa-lá do sistema usando OS.
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEM_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# Modulo para definirmos as letras que serão entregues no game
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


# Criar os objetos (para definirmos as coisas que existem no jogo e também a movimentaçã0).

class Passaro:
    IMGS = IMAGEM_PASSARO
    # Animações da rotação.
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    # Atributos de classe do PASSARO(Informações do passaro na tela).
    def __init__(self, x, y):  # Classe para decidimos oque o passaro vai fazer e pode fazer(X, Y)
        self.x = x  # Para definir o movimento no eixo X do passaro.
        self.y = y  # Para definir o movimento no eixo y do passaro.
        self.angulo = 0  # O Angulo que o passaro vai começar no game.(NO CASO RETO E NO MEIO DO MAPA).
        self.velocidade = 0  # A velocidade inicial do passaro no game(velocidade para cima e para baixo).
        self.altura = self.y  # Altura do passaro vai ser o valor do eixo Y.
        self.tempo = 0  # O tempo é a constante que logo depois que o passaro pular, ele cai. o tempo de decaimento dele.
        self.contagem_imagem = 0  # é para saber qual imagem do passaro está passando naquele momento(as 3 imagens)
        self.imagem = self.IMGS[0]  # definimos que quando criarmos o passaro, vir a primeira imagem.

    # Função que vai definir a movimentação linear do passaro(X, Y)

    def pular(self):
        self.velocidade = -7.5  # EIXO Y NO PYTHON SEMPRE COMEÇA PRA BAIXO, ENTAO USAMOS NEGATIVO PARA IR PARA CIMA.
        self.tempo = 0
        self.altura = self.y

    def mover(self):  # Calculo de deslocamento.
        self.tempo += 1  # para cada momento do jogo, em segundos, o tempo do jogo sobe. por isso += 1

        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo  # Formula do sorvetão(Aceleração),
        # deslocamento do passaro conforme passar do jogo

        # Restrintir a movimentação dele para que não haja bugs ou aproveitamentos
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Agora vamos fazer o angulo do passaro.
        if deslocamento < 0 or self.y < (
                self.altura * 50):  # Self.y serve para evitar que o passaro caia a 90º e sim de forma mais 'animada'.
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA  # Para botar a rotação no maximo, tanto pra cima quanto para baixo.

        else:
            if self.angulo > - 90:  # Serve para diminuir quando estiver descendo, diminuindo para nao cair a 90º
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # primeiro vamos definir as imagens do passaro.
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:  # ESSAS 3 IMAGENS SÃO AS QUE VAO APARECER DE ACORDO COM QUE O PASSARO VOE(BAIXO, CIMA E MEIO)
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem <= self.TEMPO_ANIMACAO * 4 + 1:  # Caso ela esteja no topo, ele vai cair de novo.
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Se o passaro estiver dispencando(caindo direto)
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar imagem

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)  # imagem do passaro mas rotacionada para fazer animações mais claras
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center  # Animação quando ele estiver no centro da imagem e saindo de pouco
        retangulo = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, retangulo.topleft)  # PARA MANDAR PARA TELA DO PYGAME ( DESENHAR NO PYGAME/PYTHON)

    # FAZER A COLISÃO DO PASSARO COM O CHÃO E O CANO.
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)  # Vai pegar o pixel do cano e do passaro e comparar para ver se há colisão.

class Cano:
    DISTANCIA = 200  # Distancia das duplas de dano(baixo e cima) em pixels
    VELOCIDADE_CANO = 5  # Para decidir o quanto o cano vai chegar perto.

    def __init__(self, x):
        self.x = x
        self.altura = 0  # Tamanho em altura do Dano
        self.pos_topo = 0  # Posição do cano de cima e baixo, sempre no eixo Y
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False,
                                               True)  # IMAGEM FLIPADA PARA QUE O CANO ESTEJA VIRADO PARA BAIXO.
        self.CANO_BASE = IMAGEM_CANO  # IMAGEM DO CANO DO TOPO E IMAGEM DO CANO DO CHÃO(BASE).
        self.passou = False  # Só pra decidir se o passaro passou pelo cano.
        self.definir_altura()  # Função que vai gerar o valor da altura do cano.

    def definir_altura(self):  # Função que vai definir a altura do cano e também calcular a altura dos canos.
        self.altura = random.randrange(50, 450)  # Distancia que o cano vai nascer dos 800 de altura, pegamos 300 livres para o passaro passar.
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):  # movimentação do cano no jogo
        self.x -= self.VELOCIDADE_CANO

    def desenhar(self, tela):  # pegar informação de desenho do cano p/ jogo.
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):  # para sabermos quando o cano vai colidir no passaro(diferente do de cima)
        passaro_mask = passaro.get_mask()
        top_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))  # Distancia da base/topo do passaro
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        base_ponto = passaro_mask.overlap(base_mask,distancia_base)  # BOOLEANO CASO EXISTA UM PONTO DE COLISÃO ENTRE OS OBJETOS.
        topo_ponto = passaro_mask.overlap(top_mask, distancia_topo)

        if base_ponto or topo_ponto:  # se haver colisão, retornar verdadeiro.
            return True
        else:
            return False


class Chao:  # Classe que será utilizada para movimentação do CHAO

    VELOCIDADE = 5  # VELOCIDADE DO CHAO
    LARGURA_CHAO = IMAGEM_CHAO.get_width()  # Imagem do chão + o tamanho do pixel da imagem.
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):  # FUNÇÃO DE CRIAÇÃO DO CHÃO.
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA_CHAO

    def mover(self):            # Movimentação do Chão que aparecerá de acordo com que o jogo vai passando
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA_CHAO < 0:  # Quando o chão 1 passar, irá trocar para o chão 2 e assim num loop infinito.
            self.x0 = self.x1 + self.LARGURA_CHAO
        if self.x1 + self.LARGURA_CHAO < 0:
            self.x1 = self.x0 + self.LARGURA_CHAO

    def desenhar(self, tela):  # Desenhar a aparencia do chão no jogo.
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):  # Desenhar na tela todos os elementos do jogo
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:  # como será com IA, usaremos quantos passaros necessarios
        passaro.desenhar(tela)
    for cano in canos:  # os dois canos na tela.
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f'PONTUAÇÃO: {pontos}', 1, (255, 255, 255))  # o tamanho da fonte que aparecerá na tela
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()  # atualizar a tela do nosso jogo.


def main():  # -------------------> Começar a configura a interação do player com o game.
    passaros = [Passaro(200, 300)]  # Configuração dos pixels que o passaro ocupa
    chao = Chao(650)    # pixel do chao apenas em X
    canos = [Cano(650)]  # pixel do cano apenas em Y
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))              # Tela do pygame, altura e largura
    pontos = 0  # Pontos iniciais do game
    relogio = pygame.time.Clock()  # tempo que o jogo será iniciado, 0s

    rodando = True
    while rodando:  # Enquanto o jogo estiver rodando, iniciado.
        relogio.tick(20)  # Tempo que rola o game.

        for evento in pygame.event.get():       # Quando o usuario for clicar no X para encerrar o game.
            if evento.type == pygame.QUIT:      # Interação com o usuario
                rodando = False
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:  # Para configurar que o usuario usará o ESPAÇO para jogar.
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        for passaro in passaros:  # Mover os itens do jogo.
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):  # Para cada passaro na lista de passaros.
                if cano.colidir(passaro):  # se o cano bater no passaro, pare.
                    passaros.pop(i)

            if not cano.passou and passaro.x > cano.x:  # Analisar pra saber se o passaro passou do cano.
                cano.passou = True
                adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:  # Caso o cano tenha saido da imagem, remover ele.
                remover_canos.append(cano)

        if adicionar_cano:          # Cada cano que passar, adicionar outro cano
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:  # Cada cano que o passaro passar, remove o cano da tela.
            canos.remove(cano)

        for i, passaro in enumerate(passaros):  # Caso o passaro morra, retira-lo da tela.
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()