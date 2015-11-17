from tkinter import *
import vectorPortal as vP
import threading
import queue
import time

class output():
    def __init__(self, fname):
        self.fname = fname
        self.file = open(fname, "w")
        self.file.write("from vectorPortal import *")
        self.file.close()

    def newLvl(self, chamberNumber, vectors, objects, size):
        self.file = open(self.fname, "a")
        self.file.write("\ndef Chamber"+str(chamberNumber)+"():")
        self.file.write("\n\tCh = Chamber("+str(vectors)+")")
        self.file.write("\n\tCh.createMap("+str(size)+", "+str(objects)+")")
        self.file.write("\n\tCh.mainLoop()")
        self.file.close()

    @staticmethod
    def test():
        print("Hi")

class Object(Frame):
    widgets = []
    def addEntry(self, X, Y, TYPE):
        self.widgets.append(Label(self, text="X co-ordinate:"+str(X)))
        self.widgets[0].grid(column=0,row=0)
        self.widgets.append(Label(self, text="Y co-ordinate:"+str(Y)))
        self.widgets[1].grid(column=1,row=0)
        self.widgets.append(Label(self, text="Type:"+str(TYPE)))
        self.widgets[2].grid(column=2,row=0)
        #self.widgets.append(Button(self, text="Remove", command=lambda:self.remove))
        #self.widgets[3].grid(column=3,row=0)


class Editor():
    Maps = queue.Queue()
    Size = queue.Queue()
    Objs = {}
    Nobjects = []
    objects = []
    def __init__(self):
        self.GUI = Tk()
        self.GUI.geometry("600x480")
        #MenuBar
        MenuBar = Menu(self.GUI)
        #File
        fileMenu = Menu(MenuBar, tearoff=0)
        fileMenu.add_command(label="New", command=lambda:print("New"))
        fileMenu.add_command(label="Save", command=lambda:print("Save"))
        #Adding cascades
        MenuBar.add_cascade(label="File", menu=fileMenu)
        self.GUI.config(menu=MenuBar)

        self.widgets = []
        self.widgets.append(Frame(self.GUI)) #Map size frame
        self.widgets[0].grid(column=0,row=0)
        self.widgets.append(Label(self.widgets[0], text="Chamber X size:"))
        self.widgets[1].grid(column=0,row=0)
        self.widgets.append(Entry(self.widgets[0])) #X size entry
        self.widgets[2].grid(column=1,row=0)
        self.widgets.append(Label(self.widgets[0], text="Chamber Y size:"))
        self.widgets[3].grid(column=0,row=1)
        self.widgets.append(Entry(self.widgets[0])) #Y size entry
        self.widgets[4].grid(column=1,row=1)
        self.widgets.append(Frame(self.GUI, bd=5, relief=SUNKEN, height=500, width=500)) #Map
        self.widgets[5].grid(column=0,row=1)
        self.widgets.append(Frame(self.GUI, bd=5, relief=SUNKEN, height=100, width=100)) #Vectors
        self.widgets[6].grid(column=2,row=0)
        self.widgets.append(Frame(self.GUI, bd=5, height=100, width=100)) #Objects ,relief=SUNKEN
        self.widgets[7].grid(column=2,row=1, sticky=NW)
        self.widgets.append(Frame(self.widgets[7], bd=5, height=100)) #Objects -subset
        self.widgets[8].grid(column=0,row=1)

        self.Ch = vP.Chamber({})
        self.MainLoop = threading.Thread(target=self.Loop)
        self.MainLoop.start()

    def objectEntry(self):
        self.Nobjects.append(Frame(self.widgets[7], bd=5, relief=SUNKEN))
        self.Nobjects[0].grid(column=0,row=0)
        self.Nobjects.append(Label(self.Nobjects[0], text="X co-ordinate"))
        self.Nobjects[1].grid(column=0,row=0)
        self.Nobjects.append(Entry(self.Nobjects[0], width=5))
        self.Nobjects[2].grid(column=1,row=0)
        self.Nobjects.append(Label(self.Nobjects[0], text="Y co-ordinate"))
        self.Nobjects[3].grid(column=2,row=0)
        self.Nobjects.append(Entry(self.Nobjects[0], width=5))
        self.Nobjects[4].grid(column=3,row=0)

        self.NoVar = StringVar(self.Nobjects[0])
        self.NoVar.set("Wall")
        self.Nobjects.append(OptionMenu(self.Nobjects[0], self.NoVar, "Wall", "Player", "Hole", "Exit", "Button", "Door", "Cube"))
        self.Nobjects[5].grid(column=4,row=0)

        self.Nobjects.append(Button(self.Nobjects[0], text="Submit", command=self.objectSubmit))
        self.Nobjects[6].grid(column=5,row=0)

    def objectSubmit(self):
        def getIndex():
            self.index = None
            t = Toplevel(self.GUI)
            Label(t, text="Please enter the an index(start at zero and increment by 1 each buuton/door pair)").grid(column=0,row=0)
            e = Entry(t)
            e.grid(column=0,row=1)
            def submit():
                try:
                    self.index = int(e.get())
                except ValueError:
                    pass
                t.destroy()
            Button(t, text="Submit", command=submit).grid(column=0,row=2)
            if self.index is not None:
                return self.index
        X = str(self.Nobjects[2].get())
        Y = str(self.Nobjects[4].get())
        TYPE = self.NoVar.get()
        tmp = "["+X+","+Y+"]"
        if TYPE == "Wall":
            vP.Wall()
        elif TYPE == "Player":
            vP.Player()
        elif TYPE == "Hole":
            vP.Hole()
        elif TYPE == "Exit":
            vP.Exit()
        elif TYPE == "Button":
            vP.Button()
            i = getIndex()
        elif TYPE == "Door":
            vP.Door()
            i = getIndex()
        elif TYPE == "Cube":
            vP.Cube()
        

    def Loop(self):
        while True:
            try:
                temp = [int(self.widgets[2].get()), int(self.widgets[4].get())]
                if temp[0] <= 30 and temp[1] <= 30:
                    self.Size.put(temp)
                    self.createMap()
                self.widgets[2].delete(0, END)
                self.widgets[4].delete(0, END)
            except ValueError:
                pass
            time.sleep(2)

    def createMap(self):
        while not self.Size.empty():
            for child in self.widgets[5].winfo_children():
                child.destroy()
            self.Ch.createMap(self.Size.get(), self.Objs)
            self.Map = []
            for x in range(len(self.Ch.Map)):
                self.Map.append([])
                for y in range(len(self.Ch.Map[x])):
                    self.Map[x].append(Label(self.widgets[5], text=self.Ch.Map[x][y].Display))
                    self.Map[x][y].grid(column=x,row=y)
            self.widgets[5].update()


test = Editor()
test.Size.put([4, 4])
test.createMap()
test.objectEntry()
test.GUI.mainloop()



    
        
