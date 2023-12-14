import pygame
import pyscroll
import pytmx
from tool import Tool
from player import Player, OtherPlayers, OtherPlayersVisualisation
from screen import Screen
from switch import Switch


class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None

        self.player: Player | None = None
        self.characters: list | None = []
        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.all_sprites = pygame.sprite.Group()

        self.character_sprites = pygame.sprite.Group()

        self.current_map: Switch = Switch(
            "switch", "map_0_test", pygame.Rect(0, 0, 0, 0), 0)

        self.switch_map(self.current_map)
        self.images = {}
        self.cross_image = pygame.transform.scale(pygame.image.load(
            "./assets/sprite/red_cross.png"), (24 * 2, 32 * 2))

    def switch_map(self, switch: Switch) -> None:
        self.tmx_data = pytmx.load_pygame(
            f"./assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(
            map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(
            map_layer=self.map_layer, default_layer=13)

        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 1
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.collisions = []

        for obj in self.tmx_data.objects:
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))
            if obj.name == None:
                print("no name", obj.id, obj.x, obj.y, obj.width, obj.height)
            type = obj.name.split(" ")[0]
            if type == "switch":
                self.switchs.append(Switch(
                    type, obj.name.split(" ")[1], pygame.Rect(
                        obj.x, obj.y, obj.width, obj.height),
                    int(obj.name.split(" ")[-1])
                ))

        if self.player:
            self.pose_player(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.collisions)
            self.group.add(self.player)
            self.group.add(self.character_sprites)
            if switch.name.split("_")[0] != "map":
                self.player.switch_bike(True)

        self.current_map = switch

    def add_player(self, player) -> None:
        self.player = player
        self.group.add(player)

        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.collisions)

    def add_characters(self, character_data):
        for data in character_data:
            screen_x = (data.x -
                        self.player.rect.width/2)
            screen_y = (data.y -
                        self.player.rect.height/2)
            character = OtherPlayersVisualisation(
                screen_x, screen_y,  data.direction, data.index_image, data.spritesheet_index, self.map_layer.zoom, self.current_map.name, data.role, data.name)
            self.character_sprites.add(character)
            self.all_sprites.add(character)
            self.group.add(character)
            self.characters.append(character)
            self.add_characters_image()

    def add_characters_image(self):
        for player in self.characters:
            image = pygame.image.load(
                f"./assets/sprite/{player.name}_walk.png")
            image = Tool.split_image(image, 0, 0, 24, 32)
            image = pygame.transform.scale(image, (24 * 2, 32 * 2))
            self.images[player.name] = image

    def move_characters(self, character_data):
        for character, data in zip(self.character_sprites, character_data):
            character.rect.x = (data.x -
                                self.player.rect.width/2)
            character.rect.y = (
                data.y - self.player.rect.height/2)
            character.direction = data.direction
            character.index_image = data.index_image
            character.spritesheet_index = data.spritesheet_index
            character.current_map_name = data.current_map_name
            character.role = data.role

    def update(self, switch_map_blocked=False, game_start=False) -> None:
        if self.player:
            if switch_map_blocked == False and self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None

            if game_start:
                for character in self.character_sprites.sprites():
                    if isinstance(character, OtherPlayersVisualisation):
                        if self.player.rect.colliderect(character.rect):
                            self.handle_encounter(character)

        self.group.center(self.player.rect.center)
        self.group.update(self.current_map.name)
        self.group.draw(self.screen.get_display())
        self.draw_header()

    def pose_player(self, switch: Switch):
        position = self.tmx_data.get_object_by_name(
            "spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)

    def handle_encounter(self, other_player: OtherPlayersVisualisation) -> None:

        if other_player.role == "cat" and self.player.role == "mouse":
            self.player.switch_ghost()

    def draw_header(self):
        for i, player in enumerate(self.characters):
            image = self.images[player.name]
            self.screen.get_display().blit(image, (20, 20 + i * 100))
            if player.role == "ghost":
                # image.set_alpha(70)
                self.screen.get_display().blit(self.cross_image, (20, 20 + i * 100))
