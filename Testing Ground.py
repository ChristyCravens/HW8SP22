from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np
import pandas as pd
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import warnings
import matplotlib.pyplot as plt

#GROUP MEMBERS, Christy Cravens, Robert Lucas, Gabe Moya
form_class = uic.loadUiType("HW_8_GUI.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        #main UI code goes here
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.MakeCanvas()

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Choose a File","","txt Files (*.txt)", options=options)
        self.FileName.setText(self.fileName)
        header=pd.read_csv(self.fileName,nrows=1,header=None) #Sets the top row(1/2 horepower) and applies it to header
        data = pd.read_csv(self.fileName,delim_whitespace=True)
        flow = np.loadtxt(self.fileName, usecols=0, skiprows=3) #takes first column of data from selected file
        head = np.loadtxt(self.fileName, usecols=1, skiprows=3) #takes second column of data for selected file
        eff = np.loadtxt(self.fileName, usecols=2, skiprows=3) #takes third column of data for selected file
        stName = ""
        for a in header.iloc[0]:
            stName += "{}".format(a) + " "
        self.PumpName.setText(stName)
        self.FlowUnits.setText(data.iloc[1,0]) #locates data based on position
        self.HeadUnits.setText(data.iloc[1,1]) #locates data based on position
        polyfithead=np.polyfit(flow,head,3)
        polyfiteff = np.polyfit(flow, eff, 3)
        stHead=""
        for a in polyfithead:
            stHead+= "{:0.2f}".format(a)+" "
        self.HeadCoefficients.setText(stHead)
        stEff = ""
        for a in polyfiteff:
            stEff+= "{:0.2f}".format(a)+" "
        self.EfficiencyCoefficients.setText(stEff)
        print(flow)
        print(head)
        print(data)
        print(header)
        print(polyfithead)
        print(polyfiteff)
        self.makeGraph()

    def MakeCanvas(self):
        """
        Create a place to make graph of Rankine cycle
        Step 1:  create a Figure object called self.figure
        Step 2:  create a FigureCanvasQTAgg object called self.canvas
        Step 3:  create an axes object for making plot
        Step 4:  add self.canvas to self.gb_Output.layout() which is a grid layout
        :return:
        """
        #Step 1.
        self.figure=Figure(figsize=(2,4),tight_layout=True, frameon=True)
        #Step 2.
        self.canvas=FigureCanvasQTAgg(self.figure)
        #Step 3.
        self.ax = self.figure.add_subplot()
        #Step 4.
        self.Output.layout().addWidget(self.canvas, 5,0,1,4)

    def makeGraph(self):
        """Makes the graph look pretty
        Step 1: Load data from selected file as an array
        Step 2: take the polyfit and put into new variable
        Step 3: Output values for head vs flow and eff vs flow to check
        Step 4: Create plot with 2 vertical axis' (head and efficiency) with flow as horizontal"""
        # Takes the data from the selected file and puts it into flow,head,eff
        flow = np.loadtxt(self.fileName, usecols=0, skiprows=3)#flow gpm
        head = np.loadtxt(self.fileName, usecols=1, skiprows=3)#head ft
        eff = np.loadtxt(self.fileName, usecols=2, skiprows=3)#Efficiency %

        #minimized sum of squared errors for a quadric and cubic fit
        z = np.polyfit(flow, head, 3)
        g = np.polyfit(flow, eff, 3)
        print("z= {}".format(z))
        print("g= {}".format(g))
        # Poly1d is nice to use for polynomials
        p = np.poly1d(z)
        h = np.poly1d(g)
        print('h= {}'.format(h)) #outputted in terminal to check values and polynomial
        print("p= {}".format(p))
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning) #Warning issued when the least-squares fit is badly conditioned
        xp = np.linspace(15, 45, 100)

        #Work done on Axis 1
        ax1=self.ax
        ax1.clear()
        #fig, ax1 = plt.subplots()
        ax1.plot(xp, p(xp), '--', color='k') #Dashed lines for Head error
        ax1.plot(flow, head, 'wo', mec='k') #Circles for Head
        ax1.set_ylim(5, 75) #sets y limit for Left vertical Axis
        ax1.set_ylabel('Head(ft)') #sets label for left vertical axis
        ax1.set_xlabel('Flow Rate (gpm)') #sets label for horizontal axis
        ax1.legend(['Head($R^2$ = 1.000', 'Head'], loc=6) #Puts legend for first axis center left

        # Work done on second axis
        ax2 = ax1.twinx() #Makes a second vertical axis on the right
        ax2.set_ylabel('Efficiency (%)') #sets label for right vertical axis
        ax2.plot(xp, h(xp), ':', color='k') #black dotted line style for efficiency error
        ax2.plot(flow, eff, '^', color='w', mec='k')#triangle for Efficiency
        ax2.set_ylim(5, 59) #y limit for second vertical axis on the right
        ax2.legend(['Efficiency($R^2$=.989)', 'Efficiency'], loc=1) #legend for eff error and eff vs flow at top right
        self.canvas.draw() #put on canvas


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
