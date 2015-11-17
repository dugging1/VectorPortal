__author__ = 'dugging'
from PIL import Image


class Map():
    entMap = [["Key", "Image", "Layer"]]  # [Dict{RGB:index}, FileName<string>, int]
    dataMap = ["Key", "Image"]  # [Dict{RGB:index}, FileName<string>]
    tileSet = ["Image"]  # FileNames<string>
    entSet = ["Image"]  # FileNames<string>

    def __init__(self, entmap, datamap, tileset, entset):
        self.entMap = entmap
        self.dataMap = datamap
        self.tileSet = tileset
        self.entSet = entset

    def drawmap(self):
        DataMap = Image.open(self.dataMap[1])
        EntMap = []
        for E in self.entMap:
            EntMap