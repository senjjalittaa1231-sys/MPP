# Membuat posisi makanan (food) muncul secara acak di dalam layar
import random

import pygame

from collison_demo import HEIGHT, WIDTH

GRID_SIZE = 20 # ukuran satu kotak grid

def buat_posisi_acak_makanan():
    kolom_maks = WIDTH // GRID_SIZE
    baris_maks = HEIGHT // GRID_SIZE
    x = random.randint(0, kolom_maks - 1) * GRID_SIZE
    y = random.randint(0, baris_maks - 1) * GRID_SIZE
    return pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)

food_rect = buat_posisi_acak_makanan()

# Di dalam game loop, setelah pengecekan tabrakan head vs makanan:
# if head_rect.colliderect(food_rect):
#     food_rect = buat_posisi_acak_makanan()  
#     # . . . tambahkan logika penambahan panjnag badan ular di sini