import pygame
from tool import Tool
from entity import Entity
from keylistener import KeyListener
from screen import Screen
from switch import Switch


class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int, role: int, name: str):
        super().__init__(keylistener, screen, x, y, role, name)
        self.pokedollars: int = 0

        self.spritesheet_bike: pygame.image = pygame.image.load(
            "./assets/sprite/hero_01_red_m_cycle_roll.png")
        self.spritesheet_cat: pygame.image = pygame.image.load(
            "./assets/sprite/hero_01_white_f_run.png")

        self.switchs: list[Switch] | None = None
        self.collisions: list[pygame.Rect] | None = None
        self.change_map: Switch | None = None
        self.role = role
        self.name = name
        self.spritesheet_index: str = None
        self.joined = True
        self.init_spritesheet()

    def update(self, player_current_map_name) -> None:
        self.check_input()
        self.check_move()

        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                if not self.check_collisions(temp_hitbox):
                    self.check_collisions_switchs(temp_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

    def add_switchs(self, switchs: list[Switch]):
        self.switchs = switchs

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    self.change_map = switch
        return None

    def add_collisions(self, collisions):
        self.collisions = collisions

    def check_collisions(self, temp_hitbox: pygame.Rect):
        for collision in self.collisions:
            if temp_hitbox.colliderect(collision):
                return True
        return False

    def check_input(self):
        if self.keylistener.key_pressed(pygame.K_b):
            self.switch_bike()

    def switch_bike(self, deactive=False):
        if self.speed == 1 and not deactive:
            self.speed = 4  # laiisser un nb paire sinon tout les perso se decalent lol quel enfer
            self.all_images = self.get_all_images(self.spritesheet_bike)
            # self.align_hitbox()
            self.spritesheet_index = "bike_red"
        else:
            self.speed = 1
            self.all_images = self.get_all_images(self.spritesheet)
            # self.align_hitbox()
            self.spritesheet_index = "foot_red"
        self.keylistener.remove_key(pygame.K_b)

    def switch_ghost(self):
        self.role = "ghost"
        # self.image.set_alpha(30)


class OtherPlayers():
    def __init__(self, x: int, y: int, direction: str, index_image: int = 0, spritesheet_index: str = "foot_red", current_map_name: str = "map_0", role: str = "mouse", name: str = "basile"):
        self.x = x
        self.y = y
        self.direction = direction
        self.index_image = index_image
        self.spritesheet_index = spritesheet_index
        self.current_map_name = current_map_name
        self.role = role
        self.name = name

    def __iter__(self):
        yield self.x
        yield self.y


class OtherPlayersVisualisation(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: str, index_image: int, spritesheet_index: str = "foot_red", map_zoom: int = 1, current_map_name: str = "map_0", role: str = "mouse", name: str = "basile"):
        super().__init__()

        self.x = x
        self.y = y
        self.role = role
        self.name = name
        self.init_spritesheet()
        self.direction: str = direction
        self.position = pygame.math.Vector2(x, y)
        self.spritesheet_bike: pygame.image = pygame.image.load(
            "./assets/sprite/hero_01_red_m_cycle_roll.png")
        self.image: pygame.image = Tool.split_image(
            self.spritesheet, 0, 0, 24, 32)

        self.rect = self.image.get_rect()
        # self.resize_image(map_zoom)
        self.index_image: int = 0
        self.all_images: dict[str, list[pygame.image]
                              ] = self.get_all_images(self.spritesheet)
        self.spritesheet_index: str = "foot_red"
        self.current_map_name = current_map_name
        self.visible = True

    def __iter__(self):
        yield self.x
        yield self.y

    def update(self, player_current_map_name) -> None:
        self.switch_spritesheet()
        self.image = self.all_images[self.direction][self.index_image]

        self.set_visibility(player_current_map_name)

        if self.role == "ghost":
            self.image.set_alpha(150)
        # self.kill()

    def get_all_images(self, spritesheet) -> dict[str, list[pygame.image]]:
        all_images = {
            "down": [],
            "left": [],
            "right": [],
            "up": []
        }

        width: int = spritesheet.get_width() // 4
        height: int = spritesheet.get_height() // 4

        for i in range(4):
            for j, key in enumerate(all_images.keys()):
                all_images[key].append(Tool.split_image(
                    spritesheet, i * width, j * height, 24, 32))
        return all_images

    def init_spritesheet(self) -> None:
        if self.role == "cat":
            self.spritesheet: pygame.image = pygame.image.load(
                "./assets/sprite/hero_01_white_f_run.png")
        else:
            self.spritesheet: pygame.image = pygame.image.load(
                f"./assets/sprite/{self.name}_walk.png")
        print(self.name)

    def switch_spritesheet(self):
        if self.spritesheet_index == "bike_red":
            self.all_images = self.get_all_images(self.spritesheet_bike)
        elif self.spritesheet_index == "cat_red":
            self.all_images = self.get_all_images(self.spritesheet)

    # def resize_image(self, factor):
    #     print(self.rect)
    #     old_rect = self.rect
    #     self.image = pygame.transform.scale(
    #         self.image, (24 * factor, 32 * factor))
    #     self.rect = self.image.get_rect(topleft=(old_rect.topleft))
    #     print(self.rect)

    # Add a method to toggle visibility
    def set_visibility(self, player_current_map_name):
        if player_current_map_name == self.current_map_name:
            self.visible = True
        else:
            self.visible = False
            self.rect.x = -400
            self.rect.y = -400
