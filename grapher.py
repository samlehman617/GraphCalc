import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import sympy as sym
from numpy import sin, cos, tan

class Grapher(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.figure = matplotlib.pyplot.Figure()
        
        self.configureWindow()
        self.createFrames()
        self.createButtons()

        self.plots = []
        
    def configureWindow(self):
        self.parent.title("Graphing Calc")
        self.parent.geometry("400x550")

    def createFrames(self):
        self.mainFrame = tk.Frame(self)
        self.buttons = tk.Frame(self.mainFrame, height = 100)
        self.numBtns = tk.Frame(self.buttons)
        self.opBtns = tk.Frame(self.buttons)
        self.graphControls = tk.Frame(self.buttons)
        self.graphEntry = tk.Frame(self.graphControls)
        self.graphBtns = tk.Frame(self.graphControls)

        
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self.buttons.pack(side=tk.BOTTOM,
                          fill=tk.X,
                          expand=False)
        self.createPlot()
        self.numBtns.pack(side=tk.LEFT, fill=tk.Y)
        self.opBtns.pack(side=tk.RIGHT, fill=tk.Y)
        self.graphControls.pack(fill=tk.BOTH)
        self.graphEntry.pack(side=tk.TOP, fill=tk.X)
        self.graphBtns.pack(side=tk.BOTTOM, fill=tk.X)

    def createCanvas(self):
        self.canvas = FigureCanvasTkAgg(self.figure, self.mainFrame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.graphBtns)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()
        
    def createButtons(self):
        self.eqtext = tk.Entry(master=self.graphEntry,
                               width=10,
                               font=("Calibri", 14),
                               justify="center")
        self.eqtext.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.graphBtn = tk.Button(master=self.graphEntry,
                                  width=10,
                                  height=10,
                                  text="Graph",
                                  command=lambda: self.graphPlots())

        self.graphBtn.pack(side=tk.RIGHT)
        
        self.graphClear = tk.Button(master=self.graphEntry, text="Clear", height=10)
        self.graphClear.pack()
        self.graphClear.configure(command=lambda: self.eqtext.delete(0, tk.END))

        for i in range(1, 10):
            print(i, ": row=", i//3+1, ", column=", i%3)
            tk.Button(master=self.numBtns, text=i, height=2, width=2, command=lambda i=i: self.eqtext.insert(tk.INSERT, str(i))).grid(row=(i-1)//3 + 1, column=(i-1)%3) 

        for i, btntxt in enumerate(("DEL", "0", ".")):
            print(i, ": row=", i//3+1, ", column=", i%3)
            if btntxt == "DEL":
                tk.Button(master=self.numBtns, text=btntxt, height=2, width=2, command=lambda: self.eqtext.delete(len(self.eqtext.get())-1, tk.END)).grid(row=4, column=i)
            else:
                tk.Button(master=self.numBtns, text=btntxt, height=2, width=2, command=lambda btntxt=btntxt: self.eqtext.insert(tk.INSERT, btntxt)).grid(row=4, column=i)
                
        for i, btntxt in enumerate(("+" , "-", "*", "/", "**", "log", "e", "pi", "(", ")", "%", "sin", "cos", "tan")):
            print(i, ": ", btntxt)
            tk.Button(master=self.opBtns, text=btntxt, height=1, width=2, command=lambda btntxt=btntxt: self.eqtext.insert(tk.INSERT, btntxt)).grid(row=(i)//4+1, column=(i)%4)

        eqbtn = tk.Button(master=self.opBtns, text="=", height=3, width=10, command=lambda: self.evalexpr())
        eqbtn.grid(row=6, column=0, columnspan=4)

    def createPlot(self):
        self.figure = matplotlib.figure.Figure(figsize=(5,5), dpi=50)
        self.graph1 = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.mainFrame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def updatePlot(self, y):
        #print("Updating plot...")
        #self.graph1.clear()
        self.graph1.plot(y)
        self.graph1.grid(True)
        self.canvas.draw()
        self.plots = []

    def graphPlots(self, x_range=np.linspace(-5, 5, 1000)):
        try:
            print("Graphing: ", self.plots)
            x = np.array(x_range)
            f=matplotlib.figure.Figure(figsize=(70,70))
            self.figure=matplotlib.figure.Figure(figsize=(70,70))
            currEQ = self.eqtext.get()
            if currEQ not in self.plots:
                print("Adding plot", self.eqtext.get())
                self.plots.append(currEQ)
            
            for fx in self.plots:
                eq = self.str2Math(fx)
                y=eq(x)
                graph1 = f.add_subplot(111)
                graph1 = self.figure.add_subplot(111) 
                self.updatePlot(y)
            print(self.plots)
        except Exception as ex:
            self.eqtext.delete(0, tk.END)
            self.eqtext.insert(0, "YOU DUN FUCKD UP! {0}".format(ex))
            self.plots = []
            self.clearEQs()


            
    def clearEQs(self):
        print("Clearing plots...")
        self.plots = []
        self.updatePlot(0)
        self.graph1.clear()
        
        self.figure = matplotlib.pyplot.Figure()

        
        self.canvas.draw()
    
    def str2Math(self, string):
        funs = sym.sympify(string)
        x = sym.symbols('x')
        if 'y' in string:
            print("3D plot")
            y = sym.symbols('y')
            fun = sym.lambdify((x, y), funs)
        else:
            fun = sym.lambdify(x, funs)
        return fun
    

    def evalexpr(self):
        try:
            res = eval(self.eqtext.get())
            print(res)
            self.eqtext.delete(0, tk.END)
            self.eqtext.insert(0, str(res))
        except Exception as ex:
            self.eqtext.delete(0, tk.END)
            self.eqtext.insert(0, "YOU DUN FUCKD UP")
            self.plots = []
            self.clearEQs()








def main():
    matplotlib.use("TkAgg")
    root = tk.Tk()
    
    Grapher(root).pack(fill=tk.BOTH, expand=True)
    root.mainloop()










if __name__=="__main__":
    main()
