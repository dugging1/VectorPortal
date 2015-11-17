__author__ = "dugging"
import random


def Basics(*args):
    print("\nBasics:")
    print("The goal of the game is to get the player(@) to the exit(E).")
    print("To move the player enter the name of a vector for the level.")


def Portals(*args):
    print("\nPortals:")
    print("Type either 'O' or 'B'(capitalised) and then a vector to fire a portal at\na wall along that vector.")
    print("Eg.If vector 'a' is move 1 up then typing 'Oa' will fire an\norange portal straight up.")
    print("Entering a portal with a vector 'x' will make the player\nexit the other portal with vector 'x'.")
    print("Eg.If vector 'a' is move 1 up then moving with the vector\nof 'a' into the orange portal will move the player out of\nthe blue portal with a vector of 'a'.")


def Inv(*args):
    print("\nInventory:")
    print("Type 'P' to pick up an object(cube).")
    print("Type 'D' and the inventory position(number given in inventory\ncommand) to drop an object.")
    print("Eg.Typing 'D1' will drop the second object in your inventory.")


def Commands(*args):
    print("\nCommands:")
    print("-\"help\": displays the help screen.")
    print("-\"vectors\": displays the level's vectors.")
    print("-\"inventory\": displays your inventory.")
    print("-\"basics\": displays the basics help screen.")
    print("-\"portals\": displays the basics portals screen.")
    print("-\"inv\": displays the inventory help screen.")
    print("-\"commands\": displays the commands help screen.")
    print("-\"key\": displays the key help screen.")


def Key(*args):
    print("\nKey:")
    print("-\"@\": The player(you)")
    print("-\".\": Empty floor(can walk here)")
    print("-\"E\": The exit(get here)")
    print("-\"W\": A wall(can't walk through and stops portal)")
    print("-\"H\": A hole(can't walk here but doesn't stop portals)")
    print("-\"O\": An orange portal(see above 'Portals' section)")
    print("-\"B\": A blue portal(see above 'Portals' section)")
    print("-\"b\": A button(does something when the player or a cube is on it)")
    print("-\"C\": A Cube(a box)")
    print("-\"F\": An Arial Faith Plate(bon voyage)")
    print("-\"N\": A non-portal-able wall(blocks portals)")


def hlp(*args):
    Basics()
    Portals()
    Inv()
    Commands()
    Key()


def vector(chamber, *args):
    print("\nVectors:")
    for n, v in enumerate(chamber.Vectors):
        if chamber.Vectors[v][0] < 0:
            if chamber.Vectors[v][1] < 0:
                print(str(v) + " = " + str(chamber.Vectors[v][0] * (-1)) + " left and " + str(chamber.Vectors[v][1] * (-1)) + " up.")
            else:
                print(str(v) + " = " + str(chamber.Vectors[v][0] * (-1)) + " left and " + str(chamber.Vectors[v][1]) + " down.")
        else:
            if chamber.Vectors[v][1] < 0:
                print(str(v) + " = " + str(chamber.Vectors[v][0]) + " right and " + str(chamber.Vectors[v][1] * (-1)) + " up.")
            else:
                print(str(v) + " = " + str(chamber.Vectors[v][0]) + " right and " + str(chamber.Vectors[v][1]) + " down.")


def inv(chamber, *args):
    playerLoc = Player.getLocation(chamber, Player)
    if len(chamber.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].Objects) > 0:
        print("Inventory:")
        for O in range(len(chamber.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].Objects)):
            if isinstance(chamber.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].Objects[O], Cube):
                print("[" + str(O) + "]:Cube")
    else:
        print("Carrying no items.")


class Chamber():
    Vectors = None  # Dictionary of Vectors
    Map = None  # 2d array for Map

    def __init__(self, vectors):
        self.Vectors = vectors
        self.Commands = {"help": [hlp, None], "vectors": [vector, self], "inventory": [inv, self], "basics": [Basics, None], "portals": [Portals, None], "inv": [Inv, None], "commands": [Commands, None], "key": [Key, None]}

    def createMap(self, size, objects):
        temp = []  # temp map storage
        for x in range(size[0]):  # for X size
            temp.append([])  #add y columns
            for y in range(size[1]):  #for Y size
                temp[x].append(Tile([], "."))  #add floor tile
                try:
                    for n, v in enumerate(objects):  #cycle through objects for level
                        if v == "[" + str(x) + "," + str(y) + "]":  #if for this tile
                            if type(objects[v]) == list:
                                for e in objects[v]:
                                    temp[x][y].Obj.append(e)
                            else:
                                temp[x][y].Obj.append(objects[v])  #add objects given
                except KeyError:
                    pass
                if x == 0 and len(temp[x][y].Obj) == 0:  #if on top row
                    temp[x][y].Obj.append(Wall())  #add wall
                elif x == size[0] - 1 and len(temp[x][y].Obj) == 0:  #if on bottom row
                    temp[x][y].Obj.append(Wall())  #add wall
                elif y == 0 and len(temp[x][y].Obj) == 0:  #if on far left column
                    temp[x][y].Obj.append(Wall())  #add wall
                elif y == size[1] - 1 and len(temp[x][y].Obj) == 0:  #if on far right column
                    temp[x][y].Obj.append(Wall())  #add wall
                temp[x][y].checkDisplay(temp[x][y].Display)  #update the display icon for the tile
        self.Map = temp  # save temp storage to instance variable

    def displayMap(self):
        tmp = []  # temp storage(array of display icon lines)
        for y in range(len(self.Map[0])):  # for amount of lines on map(Y)
            tmp.append("")  #add blank display line
            for x in range(len(self.Map)):  #for amount of places on row(X)
                self.Map[x][y].checkDisplay(self.Map[x][y].Display)  #update display icon of this tile
                tmp[y] += self.Map[x][y].Display  #add this tile's icon to it's display line
        for p in range(len(tmp)):  # for the number of lines
            print(tmp[p])  #print the line

    def mainLoop(self):
        Commands()
        vector(self)
        while True:
            for x in range(len(self.Map)):
                for y in range(len(self.Map[x])):
                    for O in range(len(self.Map[x][y].Obj)):
                        if isinstance(self.Map[x][y].Obj[O], Door):
                            self.Map[x][y].Obj[O].checkDoor()
                        elif isinstance(self.Map[x][y].Obj[O], Button):
                            self.Map[x][y].Obj[O].checkButton()
                    self.Map[x][y].checkDisplay(self.Map[x][y].Display)
            self.displayMap()  # display the map
            inp = input("Please enter a command(for help type:help): ")  # get user input
            playerLoc = Player.getLocation(self, Player)  # get the player's location
            if len(inp) > 1 and inp[0] == "O":  # if firing the orange portal
                temp = playerLoc  #save the player's location in temp storage
                loop = True
                while loop:
                    try:
                        temp[0] = playerLoc[0] + self.Vectors[inp[1:]][0]  #add the X part of the vector to temp location
                        temp[1] = playerLoc[1] + self.Vectors[inp[1:]][1]  #add the Y part of the vector to temp location
                    except KeyError:
                        break
                    if temp[0] < 0 or temp[1] < 0 or temp[0] >= len(self.Map) or temp[1] >= len(self.Map[0]):  #if temp location is outside the map
                        break  #stop looping(while loop line 76)
                    for O in self.Map[temp[0]][temp[1]].Obj:  #for (O)bjects on tile
                        if isinstance(O, Wall):  #if the object is a wall
                            OportLoc = OPortal.getLocation(self, OPortal)
                            if OportLoc is not None:
                                self.Map[OportLoc[0]][OportLoc[1]].Obj.pop(OportLoc[2])  #destroy the old portal
                            self.Map[temp[0]][temp[1]].Obj.append(OPortal())  #place the new portal
                            OportLoc = OPortal.getLocation(self, OPortal)
                            if OportLoc is not None:
                                loop = False
            elif len(inp) > 1 and inp[0] == "B":  # if firing the blue portal
                temp = playerLoc
                loop = True
                while loop:
                    try:
                        temp[0] = playerLoc[0] + self.Vectors[inp[1:]][0]
                        temp[1] = playerLoc[1] + self.Vectors[inp[1:]][1]
                    except KeyError:
                        break
                    if temp[0] < 0 or temp[1] < 0 or temp[0] >= len(self.Map) or temp[1] >= len(self.Map[0]):
                        break
                    for O in self.Map[temp[0]][temp[1]].Obj:
                        if isinstance(O, Wall):
                            BportLoc = BPortal.getLocation(self, BPortal)
                            if BportLoc is not None:
                                self.Map[BportLoc[0]][BportLoc[1]].Obj.pop(BportLoc[2])
                            self.Map[temp[0]][temp[1]].Obj.append(BPortal())
                            BportLoc = BPortal.getLocation(self, BPortal)
                            if BportLoc is not None:
                                loop = False
            elif inp == "P":
                tmp = False
                tmpa = False
                for o in range(len(self.Map[playerLoc[0]][playerLoc[1]].Obj)):
                    if isinstance(self.Map[playerLoc[0]][playerLoc[1]].Obj[o], Player):
                        tmp = [playerLoc[0], playerLoc[1], o]
                    elif isinstance(self.Map[playerLoc[0]][playerLoc[1]].Obj[o], Cube):
                        tmpa = [playerLoc[0], playerLoc[1], o]
                if tmp != False and tmpa != False:
                    self.Map[tmp[0]][tmp[1]].Obj[tmp[2]].Objects.append(self.Map[tmpa[0]][tmpa[1]].Obj.pop(tmpa[2]))
            elif len(inp) > 1 and inp[0] == "D":
                if int(inp[1:]) <= len(self.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].Objects):
                    try:
                        self.Map[playerLoc[0]][playerLoc[1]].Obj.append(self.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].Objects.pop(int(inp[1:])))
                    except ValueError:
                        pass
                else:
                    print("Invalid inventory position.")
            else:
                try:
                    self.Vectors[inp]
                    self.Map[playerLoc[0]][playerLoc[1]].Obj[playerLoc[2]].move(inp, self)
                except KeyError:
                    try:
                        c = self.Commands[inp]
                        c[0](c[1])
                    except KeyError:
                        pass
            for x in range(len(self.Map)):
                for y in range(len(self.Map[x])):
                    for O in range(len(self.Map[x][y].Obj)):
                        if isinstance(self.Map[x][y].Obj[O], Door):
                            self.Map[x][y].Obj[O].checkDoor()
                        elif isinstance(self.Map[x][y].Obj[O], Button):
                            self.Map[x][y].Obj[O].checkButton()
                        elif isinstance(self.Map[x][y].Obj[O], faithPlate):
                            self.Map[x][y].Obj[O].checkPlate()
                            break
            ExitLoc = Exit.getLocation(self, Exit)
            if self.Map[ExitLoc[0]][ExitLoc[1]].Obj[ExitLoc[2]].checkExit(self):
                self.Map[ExitLoc[0]][ExitLoc[1]].Obj[ExitLoc[2]].Command()


class Tile():
    Display = None

    def __init__(self, objects, display="."):
        self.Obj = objects
        self.checkDisplay(display)

    def checkDisplay(self, display):
        if len(self.Obj) == 1:
            self.Display = self.Obj[0].Display
        elif len(self.Obj) > 1:
            for O in self.Obj:
                if isinstance(O, Player):
                    self.Display = "@"
                    break
                elif isinstance(O, OPortal):
                    self.Display = "O"
                elif isinstance(O, BPortal):
                    self.Display = "B"
                elif isinstance(O, Cube):
                    self.Display = "C"
                elif isinstance(O, Button):
                    self.Display = "b"
        else:
            self.Display = display


class Object():
    def __init__(self, command=[], display="."):
        self.Command = command
        self.Display = display
        self.ID = random.random()

    def findSelf(self, command):
        for x in range(len(command[1].Map)):
            for y in range(len(command[1].Map[x])):
                for O in range(len(command[1].Map[x][y].Obj)):
                    if command[1].Map[x][y].Obj[O].ID == self.ID:
                        self.Pos = [x, y, O]

    @staticmethod
    def getLocation(chamber, clas):
        for x in range(len(chamber.Map)):
            for y in range(len(chamber.Map[x])):
                for O in range(len(chamber.Map[x][y].Obj)):
                    if isinstance(chamber.Map[x][y].Obj[O], type(clas())):
                        return [x, y, O]


class Player(Object):
    Display = "@"

    def __init__(self, objects=[]):
        self.Objects = objects
        self.ID = random.random()

    def move(self, inp, chamber):
        try:
            vector = chamber.Vectors[inp]
        except KeyError:
            return False
        playerLoc = Player.getLocation(chamber, Player)
        for O in chamber.Map[playerLoc[0] + vector[0]][playerLoc[1] + vector[1]].Obj:
            if isinstance(O, Wall):
                tmp = False
                for o in chamber.Map[playerLoc[0] + vector[0]][playerLoc[1] + vector[1]].Obj:
                    if isinstance(o, OPortal):
                        if BPortal.getLocation(chamber, BPortal) is not None:
                            tmp = True
                            OPortal.checkPort(chamber, vector)
                            return True
                        else:
                            print("Please fire a blue portal.")
                    elif isinstance(o, BPortal):
                        if OPortal.getLocation(chamber, OPortal) is not None:
                            tmp = True
                            BPortal.checkPort(chamber, vector)
                            return True
                        else:
                            print("Please fire an orange portal.")
                if not tmp:
                    return False
            elif isinstance(O, Hole):
                return False
            elif isinstance(O, Door):
                if not O.Open:
                    return False
            elif isinstance(O, noPortWall):
                return False
        else:
            chamber.Map[playerLoc[0]][playerLoc[1]].Obj.pop(playerLoc[2])
            chamber.Map[playerLoc[0]][playerLoc[1]].checkDisplay(".")
            chamber.Map[playerLoc[0] + vector[0]][playerLoc[1] + vector[1]].Obj.append(self)


class OPortal(Object):
    def __init__(self, command=None, display="O"):
        super(OPortal, self).__init__(command, display)
        self.Command = OPortal.port
        self.ID += 1

    @staticmethod
    def checkPort(chamber, Vector):
        if (OPortal.getLocation(chamber, OPortal)[0] == (Player.getLocation(chamber, Player)[0] + Vector[0])) and (OPortal.getLocation(chamber, OPortal)[1] == (Player.getLocation(chamber, Player)[1] + Vector[1])):
            OPortal.port(chamber, Vector)

    @staticmethod
    def port(chamber, Vector):
        OP = BPortal.getLocation(chamber, BPortal)
        PP = Player.getLocation(chamber, Player)
        if (OP[0] + Vector[0] > len(chamber.Map) - 1) or (OP[0] + Vector[0] < 0) or (OP[1] + Vector[1] > len(chamber.Map[0]) - 1) or (+OP[1] + Vector[1] < 0):
            print("That will leave the chamber illegally.")
        else:
            chamber.Map[OP[0] + Vector[0]][OP[1] + Vector[1]].Obj.append(chamber.Map[PP[0]][PP[1]].Obj[PP[2]])
            chamber.Map[PP[0]][PP[1]].Obj.pop(PP[2])
            chamber.Map[PP[0]][PP[1]].checkDisplay(".")


class BPortal(Object):
    def __init__(self, command=None, display="B"):
        super(BPortal, self).__init__(command, display)
        self.ID += 2

    @staticmethod
    def checkPort(chamber, Vector):
        if (BPortal.getLocation(chamber, BPortal)[0] == (Player.getLocation(chamber, Player)[0] + Vector[0])) and (BPortal.getLocation(chamber, BPortal)[1] == (Player.getLocation(chamber, Player)[1] + Vector[1])):
            BPortal.port(chamber, Vector)

    @staticmethod
    def port(chamber, Vector):
        BP = OPortal.getLocation(chamber, OPortal)
        PP = Player.getLocation(chamber, Player)
        if (BP[0] + Vector[0] > len(chamber.Map) - 1) or (BP[0] + Vector[0] < 0) or (BP[1] + Vector[1] > len(chamber.Map[0]) - 1) or (BP[1] + Vector[1] < 0):
            print("That will leave the chamber illegally.")
        else:
            chamber.Map[BP[0] + Vector[0]][BP[1] + Vector[1]].Obj.append(chamber.Map[PP[0]][PP[1]].Obj[PP[2]])
            chamber.Map[PP[0]][PP[1]].Obj.pop(PP[2])
            chamber.Map[PP[0]][PP[1]].checkDisplay(".")


class Wall(Object):
    def __init__(self, command=None, display="W"):
        super(Wall, self).__init__(command, display)
        self.ID += 3


class noPortWall(Object):
    def __init__(self, command=None, display="N"):
        super(noPortWall, self).__init__(command, display)
        self.ID += 10


class Hole(Object):
    def __init__(self, command=None, display="H"):
        super(Hole, self).__init__(command, display)
        self.ID += 4


class Button(Object):
    def __init__(self, command=[None, None], display="b"):
        super(Button, self).__init__(command, display)
        self.ID += 5
        # command = [index, chamber]

    def checkButton(self):
        # command = [index, chamber]
        self.findSelf(self.Command)
        for o in self.Command[1].Map[self.Pos[0]][self.Pos[1]].Obj:
            if isinstance(o, Player) or isinstance(o, Cube):
                self.Command[1].D[self.Command[0]] = True
                return
            else:
                self.Command[1].D[self.Command[0]] = False


class Door(Object):
    def __init__(self, command=[], Open=False, display="D"):
        super(Door, self).__init__(command, display)
        self.Open = Open
        self.ID += 6
        # [index, ch]

    def checkDoor(self):
        if self.Command[1].D[self.Command[0]]:
            self.Open = True
            self.Display = "d"
        else:
            self.Open = False
            self.Display = "D"


class Cube(Object):
    def __init__(self, command=None, display="C"):
        super(Cube, self).__init__(command, display)
        self.ID += 7


class Exit(Object):
    def __init__(self, command=[compile("""raise""", '<string>', 'exec')], display="E"):
        super(Exit, self).__init__(command, display)
        self.ID += 8

    def checkExit(self, chamber):
        playerLoc = Player.getLocation(chamber, Player)
        exitLoc = Exit.getLocation(chamber, Exit)
        return (playerLoc[0] == exitLoc[0]) and (playerLoc[1] == exitLoc[1])


class faithPlate(Object):
    def __init__(self, command=[], display="F"):
        super(faithPlate, self).__init__(command, display)
        self.ID += 9
        # command = [vector[], Ch]

    def checkPlate(self):
        self.findSelf(self.Command)
        for O in self.Command[1].Map[self.Pos[0]][self.Pos[1]].Obj:
            if isinstance(O, Player) or isinstance(O, Cube):
                O.findSelf(self.Command)
                Loc = O.Pos
                newLoc = [Loc[0] + self.Command[0][0], Loc[1] + self.Command[0][1]]
                if (OPortal.getLocation(self.Command[1], OPortal) is not None) and (BPortal.getLocation(self.Command[1], BPortal) is not None):
                    OLoc = OPortal.getLocation(self.Command[1], OPortal)
                    BLoc = BPortal.getLocation(self.Command[1], BPortal)
                    if newLoc[0] == OLoc[0] and newLoc[1] == OLoc[1]:
                        NPortLoc = [BLoc[0] + self.Command[0][0], BLoc[1] + self.Command[0][1]]
                        if (NPortLoc[0] < 0) or (NPortLoc[0] > len(self.Command[1].Map)) or (NPortLoc[1] < 0) or (NPortLoc[1] > len(self.Command[1].Map[0])):
                            return False
                        OPortal.port(self.Command[1], self.Command[0])
                        return True
                    elif newLoc[0] == BLoc[0] and newLoc[1] == BLoc[1]:
                        NPortLoc = [OLoc[0] + self.Command[0][0], OLoc[1] + self.Command[0][1]]
                        if (NPortLoc[0] < 0) or (NPortLoc[0] > len(self.Command[1].Map)) or (NPortLoc[1] < 0) or (NPortLoc[1] > len(self.Command[1].Map[0])):
                            return False
                        BPortal.port(self.Command[1], self.Command[0])
                        return True
                self.Command[1].Map[newLoc[0]][newLoc[1]].Obj.append(self.Command[1].Map[Loc[0]][Loc[1]].Obj.pop(Loc[2]))


class Levels():
    def changeChamber(self, fromLvl, toLvl):
        print("\n\nLevel " + str(fromLvl) + " complete!\n\n")
        toLvl()

    def end(self):
        print("End of Game...\n\n")

    def Chamber1(self):
        Ch = Chamber({"a": [0, -1], "b": [1, -1], "-a": [0, 1], "-b": [-1, 1]})  # Creates an instance of the Chamber Class(a level) with vector options a=(0 1) and b=(1 1)(+Y = down, +X = Right)
        objs = {"[2,0]": Exit(lambda: self.changeChamber("1", self.Chamber2)),  # Places the exit at (3,5)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                "[1,3]": Player()}  # Places the player at (1, 2)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
        Ch.createMap([5, 5], objs)  # Creates a room of size 5,5 and places the exit at (3,5)(Y co-ord is reversed so Y=0 is at the top and lines start at 0 not 1)
        Ch.mainLoop()  # Starts the level

    def Chamber2(self):
        Ch = Chamber({"a": [0, -1], "b": [1, -1], "-a": [0, 1], "-b": [-1, 1]})  # Creates an instance of the Chamber Class(a level) with vector options a=(0 1) and b=(1 1)(+Y = down, +X = Right)
        objs = {"[2,0]": Exit(lambda: self.changeChamber("2", self.Chamber3)),  # Places the exit at (3, 5)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                "[1,3]": Player(),  #Places the player at (1, 2)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                "[1,2]": Hole(),  #Places a hole at (1, 3)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                "[2,2]": Hole(),  #Places a hole at (2, 3)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                "[3,2]": Hole()  #Places a hole at (3, 3)(Y co-ords are reversed so Y=0 is the top and X=0 is the far left)
                }
        Ch.createMap([5, 5], objs)  # Creates a room of size 5,5 and places the exit at (3,5)(Y co-ord is reversed so Y=0 is at the top and lines start at 0 not 1)
        Ch.mainLoop()  # Starts the Level

    def Chamber3(self):
        Ch = Chamber({"a": [0, -1], "b": [1, -1], "-a": [0, 1], "-b": [-1, 1]})
        objs = {"[7,2]": Exit(lambda: self.changeChamber("3", self.Chamber4)),
                "[2,5]": Player(),
                "[4,1]": Hole(),
                "[4,2]": Hole(),
                "[4,3]": Hole(),
                "[3,3]": Hole(),
                "[2,3]": Hole(),
                "[1,3]": Hole(),
                "[4,4]": Wall(),
                "[4,5]": Wall(),
                "[5,4]": Wall(),
                "[6,4]": Wall()
                }
        Ch.createMap([8, 7], objs)
        Ch.mainLoop()

    def Chamber4(self):
        Ch = Chamber({"a": [0, -1], "b": [1, -1], "-a": [0, 1], "-b": [-1, 1]})
        Ch.D = [False]
        objs = {"[2,0]": Exit(lambda: self.changeChamber("4", self.Chamber5)),
                "[1,2]": Wall(),
                "[2,2]": Door([0, Ch]),
                "[3,2]": Wall(),
                "[1,4]": Button([0, Ch]),
                "[2,4]": Player(),
                "[3,4]": Cube()}
        Ch.createMap([5, 6], objs)
        Ch.mainLoop()

    def Chamber5(self):
        Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
        Ch.D = [True, False]
        objs = {"[5,0]": Exit(lambda: self.changeChamber("5", self.Chamber6)),
                "[1,1]": [Button([0, Ch]), Cube()],
                "[3,1]": Wall(),
                "[3,2]": Wall(),
                "[1,3]": Wall(),
                "[2,3]": Door([0, Ch], True),
                "[3,3]": Wall(),
                "[4,3]": Wall(),
                "[5,3]": Door([1, Ch]),
                "[2,5]": Player(),
                "[5,5]": Button([1, Ch])}
        Ch.createMap([7, 7], objs)
        Ch.mainLoop()

    def Chamber6(self):
        Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
        objs = {"[6,3]": Exit(lambda: self.changeChamber("6", self.Chamber7)),
                "[2,3]": Player(),
                "[1,2]": faithPlate([[3, 0], Ch]),
                "[3,0]": noPortWall(),
                "[4,0]": noPortWall(),
                "[5,0]": noPortWall(),
                "[6,0]": noPortWall(),
                "[6,1]": noPortWall(),
                "[6,2]": noPortWall(),
                "[6,4]": noPortWall(),
                "[6,5]": noPortWall(),
                "[5,5]": noPortWall(),
                "[4,5]": noPortWall(),
                "[3,5]": noPortWall(),
                "[3,1]": Hole(),
                "[3,2]": Hole(),
                "[3,3]": Hole(),
                "[3,4]": Hole()}
        Ch.createMap([7, 6], objs)
        Ch.mainLoop()

    def Chamber7(self):
        Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
        objs = {"[9,2]": Exit(lambda: self.changeChamber("7", self.Chamber8)),
                "[2,4]": Player(),
                "[1,2]": faithPlate([[3, 0], Ch]),
                "[7,0]": noPortWall(),
                "[8,0]": noPortWall(),
                "[9,0]": noPortWall(),
                "[9,1]": noPortWall(),
                "[9,3]": noPortWall(),
                "[9,4]": noPortWall(),
                "[9,5]": noPortWall(),
                "[9,6]": noPortWall(),
                "[8,6]": noPortWall(),
                "[7,6]": noPortWall(),
                "[4,1]": Wall(),
                "[5,1]": Wall(),
                "[4,2]": Wall(),
                "[5,2]": Wall(),
                "[4,3]": Wall(),
                "[5,3]": Wall(),
                "[7,1]": Hole(),
                "[7,2]": Hole(),
                "[7,3]": Hole(),
                "[7,4]": Hole(),
                "[7,5]": Hole()}
        Ch.createMap([10, 7], objs)
        Ch.mainLoop()

    def Chamber8(self):
        Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
        Ch.D = [False, False]
        objs = {"[9,3]": Exit(lambda: self.changeChamber("8", self.Chamber9)), "[1,3]": Player(), "[3,0]": noPortWall(), "[3,1]": noPortWall(), "[4,0]": noPortWall(), "[5,0]": noPortWall(), "[6,0]": noPortWall(), "[7,0]": noPortWall(),
                "[8,0]": noPortWall(), "[8,1]": noPortWall(), "[8,2]": noPortWall(), "[7,2]": noPortWall(), "[7,3]": noPortWall(), "[7,4]": noPortWall(), "[6,4]": noPortWall(), "[5,4]": noPortWall(), "[4,4]": noPortWall(),
                "[3,4]": noPortWall(), "[3,3]": noPortWall(), "[9,5]": noPortWall(), "[7,7]": noPortWall(), "[7,6]": noPortWall(), "[7,1]": Wall(), "[5,3]": Wall(), "[2,6]": Wall(), "[3,6]": Wall(), "[3,5]": Wall(), "[3,7]": Wall(),
                "[1,6]": Hole(), "[5,5]": Hole(), "[5,6]": Hole(), "[5,7]": Hole(), "[2,7]": Cube(), "[2,4]": Button([0, Ch]), "[8,7]": Button([1, Ch]), "[3,2]": Door([0, Ch]), "[8,4]": Door([1, Ch]), "[4,1]": faithPlate([[3, 0], Ch])}
        Ch.createMap([10, 9], objs)
        Ch.mainLoop()

    def Chamber9(self):
        Ch = Chamber({"a": [-1, -1], "-a": [1, 1], "b": [1, -1], "-b": [-1, 1]})
        Ch.D = [False]
        objs = {"[9,3]": Exit(lambda: self.changeChamber("9", self.end)), "[2,6]": Player(), "[2,1]": Cube(), "[1,2]": faithPlate([[0, 3], Ch]), "[2,4]": faithPlate([[0, -3], Ch]), "[5,3]": faithPlate([[-2, 2], Ch]),
                "[4,6]": faithPlate([[2, -2], Ch]), "[4,8]": faithPlate([[3, 0], Ch]), "[7,8]": Button([0, Ch]), "[5,1]": Door([0, Ch]), "[6,2]": Door([0, Ch]), "[7,3]": Door([0, Ch]), "[8,4]": Door([0, Ch]), "[5,0]": noPortWall(),
                "[6,0]": noPortWall(), "[7,0]": noPortWall(), "[8,0]": noPortWall(), "[9,0]": noPortWall(), "[9,1]": noPortWall(), "[9,2]": noPortWall(), "[9,4]": noPortWall(), "[3,1]": Hole(), "[3,2]": Hole(), "[3,3]": Hole(),
                "[2,3]": Hole(), "[1,3]": Hole(), "[3,4]": Hole(), "[4,3]": Hole(), "[4,4]": Hole(), "[4,5]": Hole(), "[5,4]": Hole(), "[5,5]": Hole(), "[5,6]": Hole(), "[6,5]": Hole(), "[6,6]": Hole(), "[6,7]": Hole(), "[6,8]": Hole(),
                "[7,6]": Hole(), "[8,6]": Hole()}
        Ch.createMap([10, 10], objs)
        Ch.mainLoop()

    def Chamber10(self):
        objects = []

        def Part1():
            Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
            objs = {"[3,1]": Exit(lambda: transfer(Ch.Map[3][1].Obj[Player.getLocation(Ch, Player)[2]].Objects, Part2)), "[2,1]": Player(objects), "[1,2]": Cube()}
            Ch.createMap([4, 4], objs)
            Ch.mainLoop()

        def Part2():
            Ch = Chamber({"a": [0, -1], "-a": [0, 1], "b": [1, 0], "-b": [-1, 0]})
            Ch.D = [False]
            objs = {"[0,1]": Exit(lambda: transfer(Ch.Map[0][1].Obj[Player.getLocation(Ch, Player)[2]].Objects, Part1)), "[1,1]": Player(objects), "[1,2]": Button([0, Ch]), "[2,1]": Door([0, Ch]), "[2,2]": Wall(),
                    "[4,1]": Exit(lambda: self.changeChamber("10", self.end))}
            Ch.createMap([5, 4], objs)
            Ch.mainLoop()

        def transfer(Objects, To):
            objects = Objects
            To()

        transfer(objects, Part1)


if __name__ == "__main__":
    lvl = Levels()
    lvl.Chamber1()
