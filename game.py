import pygame
from keylistener import KeyListener
from map import Map
from screen import Screen
from player import Player, OtherPlayers
from screen import Screen
from network import Network
from tool import Tool
import asyncio


class Game:
    def __init__(self):
        self.running: bool = True
        self.screen: Screen = Screen()
        self.map: Map = Map(self.screen)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = None
        self.start_time = None  # Record the start time of the game
        self.switch_map_blocked = True
        self.game_start = False

    async def run(self, player_instances):
        # p = self.choose_player(player_instances)
        n = Network()
        p = n.getP()
        print("p*********", p)
        self.player = Player(
            self.keylistener, self.screen, p["x"], p["y"], p["role"], p["name"])
        self.map.add_player(self.player)

        # intéressant si je laisse juste players instances il y a u bonhomme en haut à gauche
        filtered_instances = [
            player for player in player_instances if player["name"] != self.player.name]
        self.map.add_characters(filtered_instances)
        # self.map.add_characters(player_instances[0:(len(player_instances)-1)])
        clock = pygame.time.Clock()
        game_over_time = None

        while self.running:
            clock.tick(60)
            # Envoyez une requête pour obtenir la liste des joueurs du serveur
            other_players = n.send(self.player.to_dict(self.map.current_map.name))
            print("others_players", other_players)
            # Si tous les joeurs sont sur la map de base(donc qu'ils ont rejoins la partie et que le début du jeu n'a pas été lancé.
            if all(player['current_map_name'] != "paradis" for player in other_players) and self.start_time is None:
                self.start_time = pygame.time.get_ticks()
            # Si le début du jeu a été lancé et que le temps écoulé est supérieur à 60 secondes
            if self.start_time is not None and (pygame.time.get_ticks() - self.start_time > 60000):
                self.game_start = True
            self.handle_input()
            self.map.move_characters(other_players)
            # si je suis une souris et que le jeu n'a pas comméncé alors je suis coincé
            if (self.player.role != "mouse" or self.game_start):
                self.switch_map_blocked = False
            # si le jeu n'a pas commencé alros je ne peux pas changer de map sauf si je suis le chat et je ne peux toucher eprsonne tant que personne n'a pas comméncé
            self.map.update(self.switch_map_blocked, self.game_start)
            if all(player['role'] != "mouse" for player in other_players) and self.player.role != "mouse":
                self.display_game_over()
                if game_over_time is None:
                    game_over_time = pygame.time.get_ticks()  # Record the current time

            if self.start_time is not None and (pygame.time.get_ticks() - self.start_time < 60000):
                self.display_intro_message()
            self.screen.update()
            if game_over_time and pygame.time.get_ticks() - game_over_time >= 5000:
                self.running = False
                break
            await asyncio.sleep(0)

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)

    def display_game_over(self) -> None:
        font = pygame.font.Font(None, 144)
        text = "Game Over"
        # Change the color to dark red
        text_surface = font.render(text, True, (139, 0, 0))
        text_surface = pygame.transform.rotate(
            text_surface, 45)  # Rotate the text 45 degrees
        text_rect = text_surface.get_rect(
            center=(self.screen.get_size()[0]/2, self.screen.get_size()[1]/2))
        self.screen.get_display().blit(text_surface, text_rect)

    def display_intro_message(self) -> None:
        font = pygame.font.Font(None, 55)
        if self.player.role == "mouse":
            text = "Vous êtes un chat, attrapez la sardine !"
        else:
            text = "Vous êtes la sardine, fuyez les chats !"
        text_surface = font.render(text, True, (139, 0, 0))
        text_surface = pygame.transform.rotate(text_surface, 10)
        text_rect = text_surface.get_rect(
            center=(self.screen.get_size()[0]/2, self.screen.get_size()[1]/2))
        self.screen.get_display().blit(text_surface, text_rect)

        # Calculate the remaining time and convert it to seconds
        remaining_time = (self.start_time + 60000 -
                          pygame.time.get_ticks()) // 1000
        # Create a new surface for the timer
        timer_surface = font.render(str(remaining_time), True, (139, 0, 0))
        timer_rect = timer_surface.get_rect(center=(self.screen.get_size(
        )[0]/2, self.screen.get_size()[1]/2 + 60))  # Position the timer below the message
        self.screen.get_display().blit(timer_surface, timer_rect)


# # Update the display
# pygame.display.flip()

# # Wait for a few seconds
# pygame.time.wait(3000)
# self.running = False

# def choose_player(self, player_instances):
#     selected_index = 0  # Index of the currently selected player
#     font = pygame.font.Font(None, 54)
#     clock = pygame.time.Clock()

#     grid_spacing_x = self.screen.get_size()[0] / 4
#     grid_spacing_y = self.screen.get_size()[1] / 4

#     while True:
#         self.screen.update()
#         self.screen.display_message(
#             "Choose Your Player", (255, 255, 255),
#             self.screen.get_size()[0] / 2, 30, font)

#         for i, player in enumerate(player_instances):
#             row = i // 4  # Calculate the row index
#             col = i % 4   # Calculate the column index

#             color = (200, 200, 200)
#             if i == selected_index:
#                 color = (255, 255, 255)

#             text_rect = font.render(player.name, True, color).get_rect(
#                 center=(col * grid_spacing_x + grid_spacing_x / 2, 200 + row * grid_spacing_y))

#             player_image = Tool.split_image(
#                 pygame.image.load(f"./assets/sprite/{player.name}_walk.png"), 0, 0, 24, 32)
#             player_image = pygame.transform.scale(
#                 player_image, (24 * 3, 32 * 3))
#             image_rect = player_image.get_rect(
#                 center=(col * grid_spacing_x + grid_spacing_x / 2, 130 + row * grid_spacing_y))

#             self.screen.display.blit(font.render(
#                 player.name, True, color), text_rect)
#             self.screen.display.blit(player_image, image_rect)

#         pygame.display.flip()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                 elif event.key == pygame.K_RETURN:
#                     chosen_player = player_instances[selected_index]
#                     return chosen_player
#                 elif event.key == pygame.K_UP:
#                     selected_index = max(0, selected_index - 4)
#                 elif event.key == pygame.K_DOWN:
#                     selected_index = min(
#                         len(player_instances) - 1, selected_index + 4)
#                 elif event.key == pygame.K_LEFT:
#                     selected_index = max(0, selected_index - 1)
#                 elif event.key == pygame.K_RIGHT:
#                     selected_index = min(
#                         len(player_instances) - 1, selected_index + 1)

#         clock.tick(10)  # Control the frame rate
