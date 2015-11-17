__author__ = 'dugging'
from PIL import Image


class Map():
    entMap = [["Key", "Image", "Layer"]]  # [[Dict{RGB<tuple>:[index, [xStart, yStart]]}, FileName<string>, int]]
    dataMap = ["Key", "Image"]  # [Dict{RGB<tuple>: index}, FileName<string>]
    tileSet = ["Image"]  # FileNames<string>
    entSet = ["Image"]  # FileNames<string>

    def __init__(self, entmap, datamap, tileset, entset, size):
        self.entMap = entmap
        self.dataMap = datamap
        self.tileSet = tileset
        self.entSet = entset
        self.size = size

    def drawMap(self):
        # Data Map(Background Image)
        dataMap = Image.open(self.dataMap[1])
        dataPix = dataMap.load()
        newMap = Image.new("RGB", self.size)
        newPix = newMap.load()
        currentPos = [0, 0]
        for X in range(dataMap.size[0]):
            for Y in range(dataMap.size[1]):
                tile = Image.open(self.tileSet[self.dataMap[0][dataPix[X, Y]]])
                tilePix = tile.load()
                for x in range(tile.size[0]):
                    for y in range(tile.size[1]):
                        newPix[currentPos[0] + x, currentPos[1] + y] = tilePix[x, y]
                currentPos[1] += tile.size[1]
            currentPos[0] += tile.size[0]
            currentPos[1] = 0
        print("Completed data map")

        # Entity Map(Objects[eg. walls, player])
        # EntMap = [[Key, Image(), Layer, Image().load()]]
        EntMap = []
        if len(self.entMap) == 0:
            newMap.save("Maps/FullMap.gif")
            return
        #Creates a list of entities and stats.ect
        for E in self.entMap:
            EntMap.append([E[0], Image.open(self.entSet[[1][0]]), E[2], Image.open(self.entSet[[1][0]]).load()])
        #Orders entities smallest to biggest layer value
        for passnum in range(len(EntMap) - 1, 0, -1):
            for i in range(passnum):
                if EntMap[i][2] > EntMap[i + 1][2]:
                    temp = EntMap[i]
                    EntMap[i] = EntMap[i + 1]
                    EntMap[i + 1] = temp
        #draw entities
        for e in EntMap:
            for X in range(e[1].size[0]):
                for Y in range(e[1].size[1]):
                    translated = e[0][e[3][X, Y]]
                    if translated is None:
                        continue
                    newMap.paste(e[1], (translated[1][0], translated[1][1],), e[1])
        newMap.save("Maps/FullMap.gif")

    @staticmethod
    def overlayEntity(base, overlay, pos=(0, 0,)):
        ent = Image.open(base)
        ov = Image.open(overlay)
        ent.paste(ov, pos, ov)
        return base

    @staticmethod
    def UpScale(image, scale):
        New = Image.new("RGB", (image.size[0] * scale, image.size[1] * scale))
        ImPix = image.load()
        NewPix = New.load()
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                for Xa in range(scale):
                    for Ya in range(scale):
                        NewPix[x * scale + Xa, y * scale + Ya] = ImPix[x, y]
        return New


test = Map([], [{(255, 255, 255,): 0}, "Textures/testMap.png"], ["Textures/test.png"], [], [64, 64])
test.drawMap()