from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import numpy as np
import pandas as pd
import sys


form_class = uic.loadUiType("HW_8_GUI.ui")[0]  # Load the UI

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

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

app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()