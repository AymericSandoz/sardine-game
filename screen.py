import pygame


class Screen:
    def __init__(self):
        self.display: pygame.display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pokémon")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate: int = 144
        self.deltatime: float = 0.0

    def update(self) -> None:
        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.display.fill((0, 0, 0))
        self.deltatime = self.clock.get_time()


    def get_delta_time(self) -> float:
        return self.deltatime

    def get_size(self) -> tuple[int, int]:
        return self.display.get_size()

    def get_display(self) -> pygame.display:
        return self.display

    # def display_message(self, message: str, color: tuple[int, int, int], x: int, y: int, font: pygame.font) -> None:
    #     text_surface = font.render(message, True, color)
    #     text_rect = text_surface.get_rect(center=(x, y))
    #     self.get_display().blit(text_surface, text_rect)

