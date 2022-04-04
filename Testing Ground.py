from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np
import pandas as pd
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import warnings
import matplotlib.pyplot as plt


form_class = uic.loadUiType("HW_8_GUI.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.MakeCanvas()

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Choose a File","","txt Files (*.txt)", options=options)
        self.FileName.setText(self.fileName)
        header=pd.read_csv(self.fileName,nrows=1,header=None)
        data = pd.read_csv(self.fileName,delim_whitespace=True)
        flow = np.loadtxt(self.fileName, usecols=0, skiprows=3)
        head = np.loadtxt(self.fileName, usecols=1, skiprows=3)
        eff = np.loadtxt(self.fileName, usecols=2, skiprows=3)
        stName = ""
        for a in header.iloc[0]:
            stName += "{}".format(a) + " "
        self.PumpName.setText(stName)
        self.FlowUnits.setText(data.iloc[1,0])
        self.HeadUnits.setText(data.iloc[1,1])
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
        flow = np.loadtxt(self.fileName, usecols=0, skiprows=3)
        head = np.loadtxt(self.fileName, usecols=1, skiprows=3)
        eff = np.loadtxt(self.fileName, usecols=2, skiprows=3)
        z = np.polyfit(flow, head, 3)
        g = np.polyfit(flow, eff, 3)
        print("z= {}".format(z))
        print("g= {}".format(g))
        p = np.poly1d(z)
        h = np.poly1d(g)
        print('h= {}'.format(h))
        print("p= {}".format(p))
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning)
            p30 = np.poly1d(np.polyfit(flow, eff, 50))
        xp = np.linspace(15, 45, 100)

        ax1=self.ax
        ax1.clear()
        #fig, ax1 = plt.subplots()
        # Work done on first axis
        ax1.plot(xp, p(xp), '--', color='k')
        ax1.plot(flow, head, 'wo', mec='k')
        ax1.set_ylim(5, 75)
        ax1.set_ylabel('Head(ft)')
        ax1.set_xlabel('Flow Rate (gpm)')
        ax1.legend(['Head($R^2$ = 1.000', 'Head'], loc=6)
        # Work done on second axis
        ax2 = ax1.twinx()
        ax2.set_ylabel('Efficiency (%)')
        ax2.plot(xp, h(xp), ':', color='k')
        ax2.plot(flow, eff, '^', color='w', mec='k')
        ax2.set_ylim(5, 59)
        ax2.legend(['Efficiency($R^2$=.989)', 'Efficiency'], loc=1)
        self.canvas.draw()


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()