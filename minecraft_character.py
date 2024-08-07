import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Luta com Personagem Quadrado")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configurações do personagem
player_size = 50
player_color = WHITE
player_pos = [100, SCREEN_HEIGHT // 2]
player_speed = 5
player_health = 100

# Configurações do inimigo
enemy_size = 50
enemy_color = RED
enemy_pos = [SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2]
enemy_speed = 3
enemy_health = 100

# Configurações do soco
punch_width = 10
punch_height = 20
punch_speed = 15
player_punch = pygame.Rect(0, 0, punch_width, punch_height)
player_punch_active = False
enemy_punch = pygame.Rect(0, 0, punch_width, punch_height)
enemy_punch_active = False

# Função para desenhar o personagem
def draw_player(screen, position):
    pygame.draw.rect(screen, player_color, pygame.Rect(position[0], position[1], player_size, player_size))

# Função para desenhar o inimigo
def draw_enemy(screen, position):
    pygame.draw.rect(screen, enemy_color, pygame.Rect(position[0], position[1], enemy_size, enemy_size))

# Função para desenhar o soco
def draw_punch(screen, rect):
    pygame.draw.rect(screen, WHITE, rect)

# Função para verificar colisão e aplicar dano
def check_collision(punch_rect, target_pos, target_size):
    if punch_rect.colliderect(pygame.Rect(target_pos[0], target_pos[1], target_size, target_size)):
        return True
    return False

# Função principal do jogo
def game_loop():
    global player_punch_active, player_punch
    global enemy_punch_active, enemy_punch
    global player_health, enemy_health
    
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        
        # Movimento do personagem
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
            player_pos[1] += player_speed
        
        # Movimento do inimigo
        if enemy_pos[1] < player_pos[1] and enemy_pos[1] < SCREEN_HEIGHT - enemy_size:
            enemy_pos[1] += enemy_speed
        if enemy_pos[1] > player_pos[1] and enemy_pos[1] > 0:
            enemy_pos[1] -= enemy_speed

        # Ativar soco do jogador
        if keys[pygame.K_SPACE] and not player_punch_active:
            player_punch_active = True
            player_punch = pygame.Rect(player_pos[0] + player_size, player_pos[1] + player_size // 2 - punch_height // 2, punch_width, punch_height)
        
        # Mover soco do jogador
        if player_punch_active:
            player_punch.x += punch_speed
            if player_punch.x > SCREEN_WIDTH:
                player_punch_active = False
        
        # Verificar colisão do soco do jogador
        if player_punch_active and check_collision(player_punch, enemy_pos, enemy_size):
            enemy_health -= 10
            player_punch_active = False
        
        # Ativar soco do inimigo
        if not enemy_punch_active and pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size).colliderect(pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)):
            enemy_punch_active = True
            enemy_punch = pygame.Rect(enemy_pos[0] - punch_width, enemy_pos[1] + enemy_size // 2 - punch_height // 2, punch_width, punch_height)
        
        # Mover soco do inimigo
        if enemy_punch_active:
            enemy_punch.x -= punch_speed
            if enemy_punch.x < 0:
                enemy_punch_active = False
        
        # Verificar colisão do soco do inimigo
        if enemy_punch_active and check_collision(enemy_punch, player_pos, player_size):
            player_health -= 10
            enemy_punch_active = False
        
        # Atualizar tela
        screen.fill(BLACK)
        draw_player(screen, player_pos)
        draw_enemy(screen, enemy_pos)
        if player_punch_active:
            draw_punch(screen, player_punch)
        if enemy_punch_active:
            draw_punch(screen, enemy_punch)
        
        # Mostrar saúde
        font = pygame.font.SysFont(None, 36)
        player_health_text = font.render(f"Saúde do Jogador: {player_health}", True, WHITE)
        enemy_health_text = font.render(f"Saúde do Inimigo: {enemy_health}", True, WHITE)
        screen.blit(player_health_text, (10, 10))
        screen.blit(enemy_health_text, (SCREEN_WIDTH - enemy_health_text.get_width() - 10, 10))
        
        pygame.display.flip()
        clock.tick(30)

# Executar o jogo
game_loop()
