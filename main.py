# main.py
import pygame
from menu import Menu
from game import Game
from name_prompt import NamePrompt

pygame.init()
pygame.display.set_caption("SUPERSEED TAP")

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

menu = Menu(screen_width, screen_height)
game = None
name_prompt = None
running = True
state = "menu"
player_name = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if state == "menu":
            result = menu.handle_events(event)
            if result == "exit":
                running = False
            elif result == "name_prompt":
                name_prompt = NamePrompt(screen_width, screen_height)
                state = "name_prompt"
        
        elif state == "name_prompt":
            result = name_prompt.handle_events(event)
            if result == "close":
                state = "menu"
                name_prompt = None
            elif result:
                player_name = result
                game = Game()
                game.heroe.name = player_name
                state = "game"
        
        elif state == "game" and game:
            game.handle_events(event)

    if state == "menu":
        menu.draw()
    elif state == "name_prompt" and name_prompt:
        name_prompt.draw()
    elif state == "game" and game:
        game.run()
        if not game.running:  # Si el juego termina (por el botón "Exit")
            state = "menu"  # Regresa al lobby
            game = None  # Reinicia el juego (se creará una nueva instancia al iniciar de nuevo)

pygame.quit()  # Cierra Pygame al final del programa