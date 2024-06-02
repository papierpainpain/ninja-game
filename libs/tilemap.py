
import json
import pygame

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [
    (-1, 0), (-1, -1), (0, -1), (1, -1),
    (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone"}
AUTOTILE_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def tiles_around(self, position: list) -> list:
        tiles = []
        tile_location = (
            int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = f"{
                tile_location[0] + offset[0]};{tile_location[1] + offset[1]}"
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])

        return tiles

    def save(self, filename: str):
        file_content = open(filename, "w")
        json.dump({
            "tilemap": self.tilemap,
            "tile_size": self.tile_size,
            "offgrid": self.offgrid_tiles
        }, file_content)
        file_content.close()

    def load(self, filename: str):
        file_content = open(filename, "r")
        map_data = json.load(file_content)
        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]
        file_content.close()

    def physics_rects_around(self, position: list) -> list:
        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(
                    tile["pos"][0] * self.tile_size, tile["pos"][1] *
                    self.tile_size,
                    self.tile_size, self.tile_size
                ))

        return rects

    def autotile(self):
        for location in self.tilemap:
            tile = self.tilemap[location]
            neighbors = set()
            for shift in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
                check_location = f"{tile['pos'][0] +
                                    shift[0]};{tile['pos'][1] + shift[1]}"
                if check_location in self.tilemap:
                    if self.tilemap[check_location]["type"] == tile["type"]:
                        neighbors.add(shift)

            neighbors = tuple(sorted(neighbors))
            if tile["type"] in AUTOTILE_TILES and neighbors in AUTOTILE_MAP:
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def render(self, surface, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surface.blit(
                self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = f"{x};{y}"
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (tile["pos"][0] * self.tile_size - offset[0],
                         tile["pos"][1] * self.tile_size - offset[1])
                    )
