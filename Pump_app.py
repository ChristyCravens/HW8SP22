import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
#from HW_8_App import Ui_Form
import warnings
import sys
import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Pump_Gui2 import Ui_Form

#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()  #if you inherit, you generally should run the parent constructor first.
        # Main UI code goes here
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()
        #A tuple containing the widgets that get updated in the View
        self.widgets = (self.le_P1, self.le_P2, self.le_P3, self.le_P4, self.le_p5, self.le_PHigh, self.ax, self.canvas)
        #self.RC=rankineController(self.widgets)  # instantiate a rankineController object

        # a place to store coordinates from last position on graph
        self.oldXData=0.0
        self.oldYData=0.0
        # End main ui code
        self.show()

    def AssignSlots(self):
        """
        Setup signals and slots for my program
        :return:
        """
        #self.btn_Calculate.clicked.connect(self.Calculate)

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
        self.gb_Output.layout().addWidget(self.canvas, 6, 0, 1, 6)
        self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

    #since my main window is a widget, I can customize its events by overriding the default event
    def mouseMoveEvent(self, event):
        self.oldXData=event.xdata if event.xdata is not None else self.oldXData
        self.oldYData=event.ydata if event.ydata is not None else self.oldYData
        self.setWindowTitle('s:{:0.2f} kJ/(kg*K), T:{:0.2f} C'.format(self.oldXData, self.oldYData))

    def Warnings(self):
        self.x= np.array([0,1,2,3,4,5])
        self.y= np.array([0,0.8,0.9,0.1,-.8,-1])
        self.z=np.polyfit(self.x,self.y,3)
        print('z= {}'.format(self.z))
        return self.z

#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    sys.exit(app.exec())
