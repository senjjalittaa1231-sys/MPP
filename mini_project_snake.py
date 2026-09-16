import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Senja Snake")

clock = pygame.time.Clock()

GRID = 20

BATAS_KIRI = 20
BATAS_ATAS = 60
BATAS_KANAN = WIDTH - 20
BATAS_BAWAH = HEIGHT - 20

snake_body = [
    (400, 300),
    (380, 300),
    (360, 300),
    (340, 300)
]

snake_colors = [
    (120, 20, 120),
    (120, 20, 120),
    (120, 20, 120),
    (120, 20, 120)
]

ukuran_ular = GRID

direction = "RIGHT"
next_direction = "RIGHT"

kecepatan = 10

warna_warna = [
    (120, 20, 120),
    (200, 30, 30),
    (20, 70, 180),
    (20, 120, 60),
    (40, 40, 40),
    (220, 140, 10)
]

warna_index = 0

JUMLAH_MAKANAN = 20
makanan = []

skor = 0

font = pygame.font.SysFont(None, 32)
font_judul = pygame.font.SysFont(None, 58)
font_game_over = pygame.font.SysFont(None, 60)
font_nice = pygame.font.SysFont(None, 52)
font_login = pygame.font.SysFont(None, 30)

nama_pemain = ""
input_aktif = False
game_dimulai = False

nice_timer = 0


def posisi_makanan_baru():
    while True:
        x = random.randrange(
            BATAS_KIRI + GRID,
            BATAS_KANAN - GRID,
            GRID
        )

        y = random.randrange(
            BATAS_ATAS + GRID,
            BATAS_BAWAH - GRID,
            GRID
        )

        posisi = (x, y)

        if posisi in snake_body:
            continue

        if posisi in makanan:
            continue

        return posisi


def buat_semua_makanan():
    makanan.clear()

    for i in range(JUMLAH_MAKANAN):
        makanan.append(posisi_makanan_baru())


buat_semua_makanan()


def gerakkan_ular():
    kepala_x, kepala_y = snake_body[0]

    if direction == "RIGHT":
        kepala_x += GRID
    elif direction == "LEFT":
        kepala_x -= GRID
    elif direction == "UP":
        kepala_y -= GRID
    elif direction == "DOWN":
        kepala_y += GRID

    snake_body.insert(0, (kepala_x, kepala_y))
    snake_colors.insert(0, snake_colors[0])


def cek_makanan():
    kepala = snake_body[0]

    for i, makanan_pos in enumerate(makanan):
        if kepala == makanan_pos:
            return i

    return -1


def gambar_background():
    window.fill((215, 240, 215))

    warna_grid = (190, 220, 190)

    for x in range(BATAS_KIRI, BATAS_KANAN, GRID):
        pygame.draw.line(
            window,
            warna_grid,
            (x, BATAS_ATAS),
            (x, BATAS_BAWAH),
            1
        )

    for y in range(BATAS_ATAS, BATAS_BAWAH, GRID):
        pygame.draw.line(
            window,
            warna_grid,
            (BATAS_KIRI, y),
            (BATAS_KANAN, y),
            1
        )

    pygame.draw.rect(
        window,
        (40, 100, 40),
        (
            BATAS_KIRI,
            BATAS_ATAS,
            BATAS_KANAN - BATAS_KIRI,
            BATAS_BAWAH - BATAS_ATAS
        ),
        3
    )


def warna_ular(index):
    return snake_colors[index]


def gambar_ular():
    for i, bagian in enumerate(snake_body):
        x, y = bagian
        warna = warna_ular(i)

        pygame.draw.rect(
            window,
            warna,
            (
                x - ukuran_ular // 2 + 1,
                y - ukuran_ular // 2 + 1,
                ukuran_ular - 2,
                ukuran_ular - 2
            )
        )

        pygame.draw.rect(
            window,
            (40, 10, 40),
            (
                x - ukuran_ular // 2,
                y - ukuran_ular // 2,
                ukuran_ular,
                ukuran_ular
            ),
            1
        )

    kepala_x, kepala_y = snake_body[0]

    if direction == "RIGHT":
        mata1 = (kepala_x + 5, kepala_y - 5)
        mata2 = (kepala_x + 5, kepala_y + 5)

    elif direction == "LEFT":
        mata1 = (kepala_x - 5, kepala_y - 5)
        mata2 = (kepala_x - 5, kepala_y + 5)

    elif direction == "UP":
        mata1 = (kepala_x - 5, kepala_y - 5)
        mata2 = (kepala_x + 5, kepala_y - 5)

    else:
        mata1 = (kepala_x - 5, kepala_y + 5)
        mata2 = (kepala_x + 5, kepala_y + 5)

    pygame.draw.rect(
        window,
        (255, 255, 255),
        (mata1[0] - 2, mata1[1] - 2, 4, 4)
    )

    pygame.draw.rect(
        window,
        (255, 255, 255),
        (mata2[0] - 2, mata2[1] - 2, 4, 4)
    )

    pygame.draw.rect(
        window,
        (0, 0, 0),
        (mata1[0] - 1, mata1[1] - 1, 2, 2)
    )

    pygame.draw.rect(
        window,
        (0, 0, 0),
        (mata2[0] - 1, mata2[1] - 1, 2, 2)
    )


def gambar_makanan():
    for x, y in makanan:
        pygame.draw.rect(
            window,
            (220, 30, 40),
            (x - 7, y - 7, 14, 14)
        )

        pygame.draw.rect(
            window,
            (255, 120, 120),
            (x - 4, y - 4, 5, 5)
        )

        pygame.draw.rect(
            window,
            (20, 100, 30),
            (x + 5, y - 9, 6, 4)
        )


def cek_game_over():
    kepala_x, kepala_y = snake_body[0]

    if kepala_x < BATAS_KIRI + GRID // 2:
        return True

    if kepala_x > BATAS_KANAN - GRID // 2:
        return True

    if kepala_y < BATAS_ATAS + GRID // 2:
        return True

    if kepala_y > BATAS_BAWAH - GRID // 2:
        return True

    for bagian in snake_body[1:]:
        if snake_body[0] == bagian:
            return True

    return False


def gambar_tombol(rect, teks):
    pygame.draw.rect(
        window,
        (70, 30, 90),
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        window,
        (30, 10, 40),
        rect,
        2,
        border_radius=8
    )

    font_tombol = pygame.font.SysFont(None, 25)

    teks_tombol = font_tombol.render(
        teks,
        True,
        (255, 255, 255)
    )

    window.blit(
        teks_tombol,
        (
            rect.centerx - teks_tombol.get_width() // 2,
            rect.centery - teks_tombol.get_height() // 2
        )
    )


def gambar_joystick():
    pusat_x = 90
    pusat_y = HEIGHT - 80

    ukuran_tombol = 32
    jarak = 36

    tombol_atas = pygame.Rect(
        pusat_x - ukuran_tombol // 2,
        pusat_y - jarak - ukuran_tombol // 2,
        ukuran_tombol,
        ukuran_tombol
    )

    tombol_bawah = pygame.Rect(
        pusat_x - ukuran_tombol // 2,
        pusat_y + jarak - ukuran_tombol // 2,
        ukuran_tombol,
        ukuran_tombol
    )

    tombol_kiri = pygame.Rect(
        pusat_x - jarak - ukuran_tombol // 2,
        pusat_y - ukuran_tombol // 2,
        ukuran_tombol,
        ukuran_tombol
    )

    tombol_kanan = pygame.Rect(
        pusat_x + jarak - ukuran_tombol // 2,
        pusat_y - ukuran_tombol // 2,
        ukuran_tombol,
        ukuran_tombol
    )

    pygame.draw.circle(
        window,
        (70, 30, 90),
        (pusat_x, pusat_y),
        22
    )

    pygame.draw.circle(
        window,
        (170, 80, 180),
        (pusat_x, pusat_y),
        12
    )

    gambar_tombol(tombol_atas, "↑")
    gambar_tombol(tombol_bawah, "↓")
    gambar_tombol(tombol_kiri, "←")
    gambar_tombol(tombol_kanan, "→")


def kontrol_joystick(pos):
    global next_direction

    pusat_x = 90
    pusat_y = HEIGHT - 80

    dx = pos[0] - pusat_x
    dy = pos[1] - pusat_y

    jarak_tombol = 36

    if abs(dx) > abs(dy):

        if dx > jarak_tombol // 2:
            if direction != "LEFT":
                next_direction = "RIGHT"

        elif dx < -jarak_tombol // 2:
            if direction != "RIGHT":
                next_direction = "LEFT"

    else:

        if dy > jarak_tombol // 2:
            if direction != "UP":
                next_direction = "DOWN"

        elif dy < -jarak_tombol // 2:
            if direction != "DOWN":
                next_direction = "UP"


def mulai_lagi():
    global snake_body
    global snake_colors
    global direction
    global next_direction
    global skor
    global kecepatan
    global warna_index
    global game_over
    global nice_timer

    snake_body = [
        (400, 300),
        (380, 300),
        (360, 300),
        (340, 300)
    ]

    snake_colors = [
        (120, 20, 120),
        (120, 20, 120),
        (120, 20, 120),
        (120, 20, 120)
    ]

    direction = "RIGHT"
    next_direction = "RIGHT"

    skor = 0
    kecepatan = 10
    warna_index = 0
    nice_timer = 0

    buat_semua_makanan()

    game_over = False


def gambar_login():
    window.fill((215, 240, 215))

    pygame.draw.rect(
        window,
        (70, 30, 90),
        (150, 80, 500, 440),
        border_radius=20
    )

    judul = font_judul.render(
        "GAME SENJA SNAKE",
        True,
        (255, 255, 255)
    )

    window.blit(
        judul,
        (
            WIDTH // 2 - judul.get_width() // 2,
            125
        )
    )

    subjudul = font_login.render(
        "Masukkan nama pemain",
        True,
        (235, 210, 240)
    )

    window.blit(
        subjudul,
        (
            WIDTH // 2 - subjudul.get_width() // 2,
            205
        )
    )

    kotak_nama = pygame.Rect(
        230,
        255,
        340,
        50
    )

    if input_aktif:
        warna_kotak = (255, 240, 255)
        warna_border = (220, 100, 220)
    else:
        warna_kotak = (255, 255, 255)
        warna_border = (180, 180, 180)

    pygame.draw.rect(
        window,
        warna_kotak,
        kotak_nama,
        border_radius=8
    )

    pygame.draw.rect(
        window,
        warna_border,
        kotak_nama,
        2,
        border_radius=8
    )

    if nama_pemain:
        teks_nama = font_login.render(
            nama_pemain,
            True,
            (50, 50, 50)
        )
    else:
        teks_nama = font_login.render(
            "Nama kamu...",
            True,
            (150, 150, 150)
        )

    window.blit(
        teks_nama,
        (
            kotak_nama.x + 15,
            kotak_nama.y + 12
        )
    )

    if input_aktif and len(nama_pemain) < 18:
        garis_x = kotak_nama.x + 15 + teks_nama.get_width() + 2

        pygame.draw.line(
            window,
            (70, 30, 90),
            (garis_x, kotak_nama.y + 10),
            (garis_x, kotak_nama.y + 40),
            2
        )

    tombol_mulai = pygame.Rect(
        270,
        350,
        260,
        55
    )

    pygame.draw.rect(
        window,
        (170, 80, 180),
        tombol_mulai,
        border_radius=12
    )

    teks_mulai = font_login.render(
        "MULAI GAME",
        True,
        (255, 255, 255)
    )

    window.blit(
        teks_mulai,
        (
            tombol_mulai.centerx - teks_mulai.get_width() // 2,
            tombol_mulai.centery - teks_mulai.get_height() // 2
        )
    )

    info = font.render(
        "Klik kotak nama lalu ketik nama kamu",
        True,
        (230, 210, 235)
    )

    window.blit(
        info,
        (
            WIDTH // 2 - info.get_width() // 2,
            440
        )
    )

    return kotak_nama, tombol_mulai


running = True
game_over = False

while running:

    if not game_dimulai:

        kotak_nama, tombol_mulai = gambar_login()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if kotak_nama.collidepoint(event.pos):
                    input_aktif = True

                elif tombol_mulai.collidepoint(event.pos):
                    if nama_pemain.strip() != "":
                        game_dimulai = True
                        input_aktif = False

            if event.type == pygame.FINGERDOWN:

                x = int(event.x * WIDTH)
                y = int(event.y * HEIGHT)

                if kotak_nama.collidepoint((x, y)):
                    input_aktif = True

                elif tombol_mulai.collidepoint((x, y)):
                    if nama_pemain.strip() != "":
                        game_dimulai = True
                        input_aktif = False

            if event.type == pygame.KEYDOWN:

                if input_aktif:

                    if event.key == pygame.K_BACKSPACE:
                        nama_pemain = nama_pemain[:-1]

                    elif event.key == pygame.K_RETURN:

                        if nama_pemain.strip() != "":
                            game_dimulai = True
                            input_aktif = False

                    else:

                        if len(nama_pemain) < 18:

                            if event.unicode.isprintable():
                                nama_pemain += event.unicode

        pygame.display.flip()
        clock.tick(60)

        continue

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_RIGHT, pygame.K_d):

                if direction != "LEFT":
                    next_direction = "RIGHT"

            elif event.key in (pygame.K_LEFT, pygame.K_a):

                if direction != "RIGHT":
                    next_direction = "LEFT"

            elif event.key in (pygame.K_UP, pygame.K_w):

                if direction != "DOWN":
                    next_direction = "UP"

            elif event.key in (pygame.K_DOWN, pygame.K_s):

                if direction != "UP":
                    next_direction = "DOWN"

            if game_over and event.key == pygame.K_SPACE:
                mulai_lagi()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not game_over:
                kontrol_joystick(event.pos)

            else:

                tombol_restart = pygame.Rect(
                    WIDTH // 2 - 120,
                    HEIGHT // 2 + 30,
                    240,
                    45
                )

                if tombol_restart.collidepoint(event.pos):
                    mulai_lagi()

        if event.type == pygame.FINGERDOWN:

            x = int(event.x * WIDTH)
            y = int(event.y * HEIGHT)

            if not game_over:
                kontrol_joystick((x, y))

            else:

                tombol_restart = pygame.Rect(
                    WIDTH // 2 - 120,
                    HEIGHT // 2 + 30,
                    240,
                    45
                )

                if tombol_restart.collidepoint((x, y)):
                    mulai_lagi()

        if event.type == pygame.FINGERMOTION:

            x = int(event.x * WIDTH)
            y = int(event.y * HEIGHT)

            if not game_over:
                kontrol_joystick((x, y))

    if not game_over:

        direction = next_direction

        gerakkan_ular()

        index_makanan = cek_makanan()

        if index_makanan != -1:

            skor += 1

            makanan.pop(index_makanan)
            makanan.append(posisi_makanan_baru())

            warna_baru = warna_warna[warna_index]

            snake_colors = [
                warna_baru
                for i in snake_body
            ]

            warna_index += 1

            if warna_index >= len(warna_warna):
                warna_index = 0

            nice_timer = 35

            if skor % 5 == 0:

                kecepatan += 2

                if kecepatan > 25:
                    kecepatan = 25

        else:

            snake_body.pop()
            snake_colors.pop()

        if cek_game_over():
            game_over = True

    gambar_background()

    if not game_over:
        gambar_makanan()

    gambar_ular()

    teks_nama_pemain = font.render(
        "Pemain: " + nama_pemain,
        True,
        (40, 20, 50)
    )

    window.blit(
        teks_nama_pemain,
        (30, 20)
    )

    teks_skor = font.render(
        "Skor: " + str(skor),
        True,
        (40, 20, 50)
    )

    window.blit(
        teks_skor,
        (270, 20)
    )

    teks_panjang = font.render(
        "Panjang: " + str(len(snake_body)),
        True,
        (40, 20, 50)
    )

    window.blit(
        teks_panjang,
        (390, 20)
    )

    teks_speed = font.render(
        "Speed: " + str(kecepatan),
        True,
        (40, 20, 50)
    )

    window.blit(
        teks_speed,
        (560, 20)
    )

    if nice_timer > 0 and not game_over:

        teks_nice = font_nice.render(
            "NICE!",
            True,
            (200, 30, 30)
        )

        window.blit(
            teks_nice,
            (
                WIDTH // 2 - teks_nice.get_width() // 2,
                80
            )
        )

        nice_timer -= 1

    if not game_over:
        gambar_joystick()

    if game_over:

        teks_game_over = font_game_over.render(
            "GAME OVER",
            True,
            (180, 20, 30)
        )

        window.blit(
            teks_game_over,
            (
                WIDTH // 2 - teks_game_over.get_width() // 2,
                HEIGHT // 2 - 70
            )
        )

        teks_skor_akhir = font.render(
            "Skor Akhir: " + str(skor),
            True,
            (40, 40, 40)
        )

        window.blit(
            teks_skor_akhir,
            (
                WIDTH // 2 - teks_skor_akhir.get_width() // 2,
                HEIGHT // 2
            )
        )

        tombol_restart = pygame.Rect(
            WIDTH // 2 - 120,
            HEIGHT // 2 + 30,
            240,
            45
        )

        pygame.draw.rect(
            window,
            (70, 30, 90),
            tombol_restart,
            border_radius=10
        )

        teks_restart = font.render(
            "MAIN LAGI",
            True,
            (255, 255, 255)
        )

        window.blit(
            teks_restart,
            (
                WIDTH // 2 - teks_restart.get_width() // 2,
                HEIGHT // 2 + 43
            )
        )

    pygame.display.flip()

    clock.tick(kecepatan)

pygame.quit()
sys.exit()