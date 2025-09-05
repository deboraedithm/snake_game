import pygame
import random
import sys
import math

pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
FPS = 10

# Cores (RGB)
PRETO = (96, 88, 86)
BRANCO = (251, 252, 255)
AZUL = (28, 110, 140)
AZUL_ESCURO = (39, 65, 86)
VERMELHO = (242, 27, 63)
CINZA = (208, 204, 208)
ROXO = (128, 0, 128)
DOURADO = (250, 223, 127)
CYAN = (0, 232, 252)

# Tamanho dos blocos
TAMANHO_BLOCO = 20

class ParticulaEfeito:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(-1, 1)
        self.vida = 30
        self.cor = cor
        
    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vida -= 1
        
    def desenhar(self, tela):
        if self.vida > 0:
            alpha = int((self.vida / 30) * 255)
            s = pygame.Surface((4, 4))
            s.set_alpha(alpha)
            s.fill(self.cor)
            tela.blit(s, (int(self.x), int(self.y)))

class JogoSnake:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("🐍 Snake Game")
        self.relogio = pygame.time.Clock()
        
        self.fonte_grande = pygame.font.Font(None, 48)
        self.fonte_media = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)
        
        self.reiniciar_jogo()
        
    def reiniciar_jogo(self):
        self.cobra = [(LARGURA//2, ALTURA//2)]
        self.direcao = (TAMANHO_BLOCO, 0)
        
        # Comida
        self.gerar_comida()
        
        # Pontuação e estado
        self.pontos = 0
        self.jogo_ativo = True
        self.particulas = []
        
        # Cores da cobra (gradiente)
        self.cores_cobra = [
            (173, 215, 246),
            (135, 191, 255),
            (63, 142, 252),
            (38, 103, 255),
            (59, 40, 204),
        ]
        
    def gerar_comida(self):
        while True:
            x = random.randint(0, (LARGURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
            y = random.randint(0, (ALTURA - TAMANHO_BLOCO) // TAMANHO_BLOCO) * TAMANHO_BLOCO
            if (x, y) not in self.cobra:
                self.comida = (x, y)
                break
    
    def criar_particulas(self, x, y, cor, quantidade=10):
        for _ in range(quantidade):
            self.particulas.append(ParticulaEfeito(x, y, cor))
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.KEYDOWN:
                if not self.jogo_ativo and evento.key == pygame.K_SPACE:
                    self.reiniciar_jogo()
                elif self.jogo_ativo:
                    
                    if evento.key == pygame.K_UP and self.direcao != (0, TAMANHO_BLOCO):
                        self.direcao = (0, -TAMANHO_BLOCO)
                    elif evento.key == pygame.K_DOWN and self.direcao != (0, -TAMANHO_BLOCO):
                        self.direcao = (0, TAMANHO_BLOCO)
                    elif evento.key == pygame.K_LEFT and self.direcao != (TAMANHO_BLOCO, 0):
                        self.direcao = (-TAMANHO_BLOCO, 0)
                    elif evento.key == pygame.K_RIGHT and self.direcao != (-TAMANHO_BLOCO, 0):
                        self.direcao = (TAMANHO_BLOCO, 0)
        
        return True
    
    def atualizar_jogo(self):
        if not self.jogo_ativo:
            return
        
        # Mover a cobra
        cabeca = self.cobra[0]
        nova_cabeca = (cabeca[0] + self.direcao[0], cabeca[1] + self.direcao[1])
        
        # Verificar colisões
        if (nova_cabeca[0] < 0 or nova_cabeca[0] >= LARGURA or 
            nova_cabeca[1] < 0 or nova_cabeca[1] >= ALTURA):
            self.jogo_ativo = False
            self.criar_particulas(nova_cabeca[0], nova_cabeca[1], VERMELHO, 20)
            return
        
        # Verificar colisão com próprio corpo
        if nova_cabeca in self.cobra:
            self.jogo_ativo = False
            self.criar_particulas(nova_cabeca[0], nova_cabeca[1], VERMELHO, 20)
            return
        
        self.cobra.insert(0, nova_cabeca)
        
        # Verificar se comeu a comida
        if nova_cabeca == self.comida:
            self.pontos += 10
            self.criar_particulas(self.comida[0], self.comida[1], DOURADO, 15)
            self.gerar_comida()
        else:
            self.cobra.pop()
        
        # Atualizar partículas
        self.particulas = [p for p in self.particulas if p.vida > 0]
        for particula in self.particulas:
            particula.atualizar()
    
    def desenhar_cobra_com_gradiente(self):
        for i, segmento in enumerate(self.cobra):
            # Calcular cor baseada na posição no corpo
            if i == 0:  # Cabeça
                cor = (100, 255, 100)
                pygame.draw.rect(self.tela, cor, 
                               (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
                # Olhos da cobra
                pygame.draw.circle(self.tela, PRETO, 
                                 (segmento[0] + 5, segmento[1] + 5), 2)
                pygame.draw.circle(self.tela, PRETO, 
                                 (segmento[0] + 15, segmento[1] + 5), 2)
            else:
                # Gradiente para o corpo
                intensidade = max(50, 255 - i * 10)
                cor = (0, intensidade, 50)
                pygame.draw.rect(self.tela, cor, 
                               (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
                # Borda mais escura
                pygame.draw.rect(self.tela, AZUL_ESCURO, 
                               (segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO), 1)
    
    def desenhar_comida_animada(self):
        # Efeito na comida
        tempo = pygame.time.get_ticks()
        pulso = int(5 * math.sin(tempo * 0.01)) + 5
        
        pygame.draw.rect(self.tela, VERMELHO,
                        (self.comida[0] - pulso//2, self.comida[1] - pulso//2, 
                         TAMANHO_BLOCO + pulso, TAMANHO_BLOCO + pulso))
        pygame.draw.rect(self.tela, DOURADO,
                        (self.comida[0], self.comida[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    def desenhar_fundo_animado(self):
        # Fundo com padrão de grade sutil
        for x in range(0, LARGURA, TAMANHO_BLOCO):
            for y in range(0, ALTURA, TAMANHO_BLOCO):
                if (x + y) % (TAMANHO_BLOCO * 2) == 0:
                    pygame.draw.rect(self.tela, (5, 5, 15), (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                else:
                    pygame.draw.rect(self.tela, (0, 0, 10), (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
    
    def desenhar_interface(self):
        # Pontuação
        texto_pontos = self.fonte_media.render(f"Pontos: {self.pontos}", True, BRANCO)
        self.tela.blit(texto_pontos, (10, 10))
        
        # Comprimento da cobra
        texto_tamanho = self.fonte_pequena.render(f"Tamanho: {len(self.cobra)}", True, CYAN)
        self.tela.blit(texto_tamanho, (10, 50))
        
        if not self.jogo_ativo:
            # Game Over
            texto_game_over = self.fonte_grande.render("GAME OVER", True, VERMELHO)
            rect_go = texto_game_over.get_rect(center=(LARGURA//2, ALTURA//2 - 50))
            self.tela.blit(texto_game_over, rect_go)
            
            texto_pontos_final = self.fonte_media.render(f"Pontuação Final: {self.pontos}", True, BRANCO)
            rect_pf = texto_pontos_final.get_rect(center=(LARGURA//2, ALTURA//2))
            self.tela.blit(texto_pontos_final, rect_pf)
            
            texto_reiniciar = self.fonte_media.render("Pressione ESPAÇO para jogar novamente", True, DOURADO)
            rect_r = texto_reiniciar.get_rect(center=(LARGURA//2, ALTURA//2 + 50))
            self.tela.blit(texto_reiniciar, rect_r)
    
    def executar(self):
        print("🐍 Snake Game iniciado!")
        print("Use as setas para controlar a cobra")
        print("Pressione ESPAÇO para reiniciar após Game Over")
        
        executando = True
        while executando:
            executando = self.processar_eventos()
            self.atualizar_jogo()
            
            # Desenhar tudo
            self.tela.fill(PRETO)
            self.desenhar_fundo_animado()
            
            if self.jogo_ativo:
                self.desenhar_comida_animada()
                self.desenhar_cobra_com_gradiente()
            
            # Desenhar partículas
            for particula in self.particulas:
                particula.desenhar(self.tela)
            
            self.desenhar_interface()
            
            pygame.display.flip()
            self.relogio.tick(FPS)
        
        pygame.quit()

def main():
    """Função principal do jogo"""
    try:
        jogo = JogoSnake()
        jogo.executar()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()