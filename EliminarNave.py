import pygame
import random

# Inicializar Pygame
pygame.init()

def start_eliminar_nave():

    # Configuración de la pantalla
    ancho, alto = 800, 600
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Juego de Disparar Naves")

    # Colores
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)

    # Cargar la imagen de fondo
    fondo = pygame.image.load("images/espacio.jpg")
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    #Música de fondo
    pygame.mixer.music.load('sonido/intergalactic_odyssey.ogg')
    pygame.mixer.music.play(-1) # con -1 reproduce la musica infinitamente
    pygame.mixer.music.set_volume(0.3) # Volumen

    ## --------------- CARGAR IMAGENES EXPLOSIÓN -------------------------- ##
    meteor_images = []
    meteor_list = ["images/explosiones/expl1.png", "images/explosiones/expl2.png", "images/explosiones/expl3.png",
                   "images/explosiones/expl4.png","images/explosiones/expl5.png", "images/explosiones/expl6.png",
                   "images/explosiones/expl7.png", "images/explosiones/expl8.png","images/explosiones/expl0.png"]
    for img in meteor_list:
	    meteor_images.append(pygame.image.load(img).convert())

    explosion_anim = []

    for i in range(9):
        file = "images/explosiones/expl{}.png".format(i)
        img = pygame.image.load(file).convert()
        img.set_colorkey(NEGRO)
        img_scale = pygame.transform.scale(img, (70, 70))
        explosion_anim.append(img_scale)

    # Clase para la nave del jugador
    class Jugador(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/nave-p.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (ancho // 2, alto - 50)
            self.speed = 5

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < ancho:
                self.rect.x += self.speed

    # Clase para las naves enemigas
    class Enemigo(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/nave.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, ancho - self.rect.width)
            self.rect.y = random.randint(10, alto - 200)
            self.speed = random.randint(2, 5)

        def update(self):
            self.rect.x += self.speed
            if self.rect.left > ancho:
                self.rect.x = 0
                self.rect.y = random.randint(15, alto - 200)
                self.speed = random.randint(2, 5)

    # Clase para los disparos
    class Bala(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load("images/bullet.png")
            self.image = pygame.transform.scale(self.image, (20, 40))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = 8

        def update(self):
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.kill()


    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()
            self.image = explosion_anim[0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50 # how long to wait for the next frame VELOCITY OF THE EXPLOSION

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_anim):
                    self.kill() # if we get to the end of the animation we don't keep going.
                else:
                    center = self.rect.center
                    self.image = explosion_anim[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Jugador()
    all_sprites.add(player)

    # Puntuación
    score = 0

    # Reloj para controlar la velocidad del juego
    clock = pygame.time.Clock()

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: # Evento al tocar barra espaciadora
                if event.key == pygame.K_SPACE:
                    # Disparar un proyectil cuando se presiona la barra espaciadora
                    bullet = Bala(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Crear nuevas naves enemigas aleatoriamente
        if len(enemies) < 5:
            enemy = Enemigo()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Verificar si los disparos impactan a las naves enemigas
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            score += 1

        # Actualizar todos los sprites
        all_sprites.update()

        # Dibuja el fondo
        screen.blit(fondo, (0, 0))
        all_sprites.draw(screen)

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        text = font.render(f"Eliminados: {score}", True, BLANCO)
        screen.blit(text, (10, 10))

        pygame.display.update()

        # Controlar la velocidad del juego
        clock.tick(60)

    # Salir del juego
    pygame.quit()

if __name__ == "__main__":
    start_eliminar_nave()
