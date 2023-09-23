import pygame
import sys
from Rescate import start_rescatar_astronauta
from EliminarNave import start_eliminar_nave

pygame.init()

# Configuración de la pantalla
ancho, alto = 800, 600
PANTALLA = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Fuente
font = pygame.font.Font(None, 36)

PANTALLA.fill(NEGRO)

# Opciones del menú
menu_options = ["Jugar Rescatar Astronautas", "Jugar Eliminar Naves", "Salir"]

# Función para mostrar el menú
def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(menu_options)):
                    text = font.render(menu_options[i], True, BLANCO)
                    text_rect = text.get_rect(center=(ancho // 2, alto // 2 - len(menu_options) * text.get_height() // 2 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        if i == 0: # Juego Astronauta
                            start_rescatar_astronauta()
                        elif i == 1: # Juego Ovnis
                            start_eliminar_nave()
                        elif i == 2:
                            pygame.quit()
                            sys.exit()

        PANTALLA.fill(NEGRO)

        # Dibuja las opciones del menú
        for i in range(len(menu_options)):
            text = font.render(menu_options[i], True, BLANCO)
            posicion_y = alto // 2 - len(menu_options) * text.get_height() // 2 + i * 50
            PANTALLA.blit(text, (ancho // 2 - text.get_width() // 2, posicion_y))

        pygame.display.update()

# Mantener el Juego en Ejecucion
show_menu()
