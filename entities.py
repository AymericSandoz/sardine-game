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


players_start = [
    {"x": 100, "y": 400, "role": "cat", "name": "cow"},
    {"x": 50, "y": 50, "role": "mouse", "name": "sheep"},
    {"x": 50, "y": 50, "role": "mouse", "name": "chicken"},
    {"x": 50, "y": 50, "role": "mouse", "name": "shlops"},
    {"x": 50, "y": 50, "role": "mouse", "name": "basile"},
    {"x": 50, "y": 50, "role": "mouse", "name": "sacha"},
    # {"x": 1500, "y": 350},
]

# Créez des instances de la classe Player à partir de la liste de dictionnaires
player_instances = []
for player_data in players_start:
    x = player_data["x"]
    y = player_data["y"]
    role = player_data["role"]
    name = player_data["name"]
    player_instance = OtherPlayers(
        x, y, direction="down", index_image=0, spritesheet_index="foot_red", current_map_name="paradis", role=role, name=name)
    player_instances.append(player_instance)

MAX_PLAYERS = len(player_instances)



