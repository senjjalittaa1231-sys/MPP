import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demo Deteksi Tabrakan (Rect Collision)")
clock = pygame.time.Clock()

# Player direpresentasikan sebagai objek Rect
player_rect = pygame.Rect(100, 275, 50, 50)
speed = 5

# Objek target (kotak statis) juga berupa Rect
target_rect = pygame.Rect(600, 275, 50, 50)

font = pygame.font.SysFont(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    # Inti deteksi tabrakan: colliderrect()
    is_colliding = player_rect.colliderect(target_rect)
    warna_target = (231, 76, 60) if is_colliding else (52, 152, 219)

    window.fill((30, 30, 45))
    pygame.draw.rect(window, (46, 204, 113), player_rect)
    pygame.draw.rect(window, warna_target, target_rect)

    status = "TABRAKAN!" if is_colliding else "Belum Bertabrakan"
    text_surface = font.render(status, True, (255, 255, 255))
    window.blit(text_surface, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()