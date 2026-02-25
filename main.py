import arcade
import random
import math


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Arcade Map Viewer"

INITIAL_CENTER_X = 2000
INITIAL_CENTER_Y = 2000

INITIAL_SCALE = 1.0

WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000
TILE_SIZE = 64

MIN_SCALE = 0.2
MAX_SCALE = 5.0
ZOOM_SPEED = 0.1

COLORS_LIGHT = {
    'water': (30, 144, 255),
    'grass': (34, 139, 34),
    'forest': (0, 100, 0),
    'mountain': (139, 69, 19),
    'snow': (255, 250, 250),
    'road': (100, 100, 100)
}

COLORS_DARK = {
    'water': (10, 40, 80),
    'grass': (20, 60, 20),
    'forest': (0, 30, 0),
    'mountain': (50, 30, 10),
    'snow': (100, 100, 110),
    'road': (40, 40, 40)
}


class MapGame(arcade.Window):
    def __init__(self, width, height, title, start_x, start_y, start_scale):
        super().__init__(width, height, title)

        self.camera = arcade.Camera2D()

        self.initial_center_x = start_x
        self.initial_center_y = start_y
        self.initial_scale = start_scale

        self.current_scale = start_scale
        self.is_dark_theme = False

        self.ground_list = None
        self.roads_list = None

        self.generate_world()

        self.camera.position = (self.initial_center_x, self.initial_center_y)
        self.camera.zoom = self.initial_scale

    def generate_world(self):
        self.ground_list = arcade.SpriteList()
        self.roads_list = arcade.SpriteList()

        cols = WORLD_WIDTH // TILE_SIZE
        rows = WORLD_HEIGHT // TILE_SIZE

        for x in range(cols):
            for y in range(rows):
                center_x = x * TILE_SIZE + TILE_SIZE / 2
                center_y = y * TILE_SIZE + TILE_SIZE / 2

                dist_from_center = math.sqrt((x - cols / 2) ** 2 + (y - rows / 2) ** 2)
                max_dist = math.sqrt((cols / 2) ** 2 + (rows / 2) ** 2)

                norm_dist = dist_from_center / max_dist

                noise = random.random() * 0.2

                tile_type = 'water'
                if norm_dist + noise < 0.3:
                    tile_type = 'mountain'
                elif norm_dist + noise < 0.45:
                    tile_type = 'forest'
                elif norm_dist + noise < 0.65:
                    tile_type = 'grass'
                else:
                    tile_type = 'water'

                sprite = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, arcade.color.WHITE)
                sprite.center_x = center_x
                sprite.center_y = center_y
                sprite.type = tile_type
                self.ground_list.append(sprite)

                if abs(x - cols / 2) < 2 or abs(y - rows / 2) < 2:
                    road = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE // 4, arcade.color.GRAY)
                    road.center_x = center_x
                    road.center_y = center_y
                    if abs(x - cols / 2) < 2:
                        road.width = TILE_SIZE // 4
                        road.height = TILE_SIZE
                    else:
                        road.width = TILE_SIZE
                        road.height = TILE_SIZE // 4
                    self.roads_list.append(road)

        self.update_colors()

    def update_colors(self):
        palette = COLORS_DARK if self.is_dark_theme else COLORS_LIGHT

        for sprite in self.ground_list:
            sprite.color = palette.get(sprite.type, arcade.color.WHITE)

        road_color = (60, 60, 60) if self.is_dark_theme else (150, 150, 150)
        for sprite in self.roads_list:
            sprite.color = road_color

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.ground_list.draw()
        self.roads_list.draw()

        cx, cy = self.camera.position
        arcade.draw_circle_outline(cx, cy, 10, arcade.color.RED, 2)

        camera = arcade.Camera2D()
        camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        camera.zoom = 1.0
        camera.use()

        info_text = (
            f"Pos: {int(cx)}, {int(cy)}\n"
            f"Zoom: {self.camera.zoom:.2f}x\n"
            f"Theme: {'Dark' if self.is_dark_theme else 'Light'}\n"
            f"Controls: WASD - Move, +/- - Zoom, T - Theme, R - Reset"
        )

        arcade.draw_text(
            info_text,
            10, SCREEN_HEIGHT - 10,
            arcade.color.WHITE if self.is_dark_theme else arcade.color.BLACK,
            14,
            bold=True,
            anchor_x="left",
            anchor_y="top"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.PAGE_UP or key == arcade.key.EQUAL:
            new_zoom = self.camera.zoom + ZOOM_SPEED * self.camera.zoom
            self.camera.zoom = min(new_zoom, MAX_SCALE)
        elif key == arcade.key.PAGE_DOWN or key == arcade.key.MINUS:
            new_zoom = self.camera.zoom - ZOOM_SPEED * self.camera.zoom
            self.camera.zoom = max(new_zoom, MIN_SCALE)


def setup_game(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE,
               start_x=INITIAL_CENTER_X, start_y=INITIAL_CENTER_Y, start_scale=INITIAL_SCALE):
    game = MapGame(width, height, title, start_x, start_y, start_scale)
    return game


def main():
    game = setup_game(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title=SCREEN_TITLE,
        start_x=2000,
        start_y=2000,
        start_scale=1.0
    )
    arcade.run()


if __name__ == "__main__":
    main()