import pygame
import random

# Inicializar Pygame
pygame.init()


def start_rescatar_astronauta():

    # Configuración de la pantalla
    ancho, alto = 550, 700
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Juego con Sprites en Pygame")

    # Cargar la imagen de fondo
    background_image = pygame.image.load("images/espacio.jpg")
    background_image = pygame.transform.scale(background_image, (ancho, alto))

    #Música de fondo
    pygame.mixer.music.load('sonido/intergalactic_odyssey.ogg')
    pygame.mixer.music.play(-1) # con -1 reproduce la musica infinitamente
    pygame.mixer.music.set_volume(0.2) # Volumen

    # Clase para el personaje
    class Jugador(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/nave-p.png")
            self.image = pygame.transform.scale(self.image, (50, 50))  # Escalar a 50x50 píxeles
            self.rect = self.image.get_rect()
            self.rect.center = (ancho // 2, alto - 50)
            self.speed = 4

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < ancho:
                self.rect.x += self.speed

    # Clase para el Astronauta perdido
    class Astronauta(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/astronauta.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect()
            self.rect.center = (random.randint(20, ancho - 20), 0)  # Iniciar astronautas en la parte superior

        def update(self):
            # Mover la astronauta hacia abajo
            self.rect.y += 3
            # Si la astronauta sale de la pantalla, eliminarla
            if self.rect.top > alto:
                self.kill()

    class Gracias(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()
            self.image = pygame.image.load("images/gracias.png")
            self.image = pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect()
            self.rect.center = (center[0] + 20, center[1])
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 400

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.kill()


    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    astronautas = pygame.sprite.Group()
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

        # Crear nuevas astronautas aleatoriamente
        if len(astronautas) < 2:
            astronauta = Astronauta()
            astronautas.add(astronauta)
            all_sprites.add(astronauta)

        # Verificar si el jugador recoge astronautas
        hits = pygame.sprite.spritecollide(player, astronautas, True)
        for hit in hits:
            thanks = Gracias(hit.rect.center)
            all_sprites.add(thanks)
            score += 1

        # Actualizar todos los sprites
        all_sprites.update()

        # Dibuja el fondo
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        text = font.render(f"Salvados: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.update()

        clock.tick(60) # Velocidad del juego

    # Salir del juego
    pygame.quit()

# Ejecutar el juego si se llama directamente este script
if __name__ == "__main__":
    start_rescatar_astronauta()
