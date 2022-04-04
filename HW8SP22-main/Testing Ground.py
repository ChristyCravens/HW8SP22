from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import sys


form_class = uic.loadUiType("HW_8_GUI.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        pltgraph=self.graph
        pltgraph.clear()
        pltgraph.setLabel('left','Signal Sin Wave', units='(V)')
        pltgraph.plot(self.plotGraph())

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Choose a File", "","txt Files (*.txt)", options=options)
        self.FileName.setText(self.fileName)
        header=pd.read_csv(self.fileName,nrows=1,header=None)
        data = pd.read_csv(self.fileName,delim_whitespace=True)
        flow = np.loadtxt(self.fileName, usecols=0, skiprows=3)
        head = np.loadtxt(self.fileName, usecols=1, skiprows=3)
        eff = np.loadtxt(self.fileName, usecols=2, skiprows=3)
        self.PumpName.setText(header.iloc[0,0])
        self.FlowUnits.setText(data.iloc[1,0])
        self.HeadUnits.setText(data.iloc[1,1])
        polyfithead=np.polyfit(flow,head,3)
        polyfiteff = np.polyfit(flow, eff, 3)
        #self.HeadCoefficients.setText(polyfithead)
        print(flow)
        print(head)
        print(data)
        print(header)
        print(polyfithead)
        print(polyfiteff)
        self.plotGraph()

    def plotGraph(self):
        fig,self.ax=plt.subplot()
        p = np.poly1d(z)
        h = np.poly1d(g)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning)
            p30 = np.poly1d(np.polyfit(x, e, 50))
        xp = np.linspace(15, 45, 100)
        self.ax1.plot(x, y, 'wo', mec='k')
        self.ax1.plot(xp, p(xp), '--', color='k')
        self.ax1.set_ylim(5, 75)
        self.ax1.set_ylabel('Head(ft)')
        self.ax1.set_xlabel('Flow Rate (gpm)')
        self.ax2 = ax1.twinx()
        self.ax2.set_ylabel('Efficiency (%)')
        self.ax2.plot(x, e, '^', color='w', mec='k')
        self.ax2.plot(xp, h(xp), ':', color='k')
        self.ax2.set_ylim(5, 59)
        # plt.plot(x,y,'wo',mec='k')
        # plt.plot(xp,p(xp),'--',color='k')
        # plt.plot(x,e,'^',color='k')
        # plt.ylim(0,75)

        plt.show()

app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()