import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Rankine_GUI import Ui_Form
from Rankine_Classes import rankineController
from Rankine_Classes import rankineView as RV
from Calc_state import UnitConverter as UC
from Calc_state import SatPropsIsobar as SPI

#this group has 3 members: Christy Cravens, Robert Lucas, and Gabe Moya
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
        self.widgets = (self.le_H1, self.le_H2, self.le_H3, self.le_H4, self.le_TurbineWork, self.le_PumpWork, self.le_HeatAdded, self.le_Efficiency, self.lbl_SatPropHigh, self.lbl_SatPropLow, self.ax, self.canvas)
        #Creating widgets for units for plot
        self.otherwidgets = (self.le_PHigh, self.lbl_PHigh, self.le_PLow, self.lbl_PLow, self.lbl_H1Units, self.lbl_H2Units, self.lbl_H3Units, self.lbl_H4Units,  self.le_TurbineInletCondition, self.lbl_TurbineWorkUnits, self.lbl_PumpWorkUnits, self.lbl_HeatAddedUnits)
        self.RC=rankineController(self.widgets)  # instantiate a rankineController object

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
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.rdo_Quality.clicked.connect(self.SelectQualityOrTHigh)
        self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        self.le_PHigh.textChanged[str].connect(self.newTemp) #changing PHigh using the new function defined below for new temp
        self.le_PLow.textChanged[str].connect(self.newPLow) #changing PLow using the new function defined below for new PLow
        self.le_TurbineInletCondition.textChanged[str].connect(self.newTemp) #changing PHigh using the new function defined below for new temp
        self.rb_English.clicked.connect(self.newUnits) #changing the units to English if English radio button is clicked

    def newTemp(self):
        """
        This function changes the temperature and updates the model based on inputs from the user.
        :return:
        """
        self.RC.updateModel((self.le_PHigh, self.le_PLow, self.rdo_Quality, self.le_TurbineInletCondition, self.le_TurbineEff))
        self.show()

    def newPLow(self):
        """
        This function changes the PLow value and updates the model based on inputs from the user.
        :return:
        """
        # Creating a shortcut for the radio button SI being checked
        SI=self.rb_SI.isChecked()
        # Creating a conversion factor for pressure if SI/English is checked
        PC=100 if SI else UC.psi_to_kpa
        #Set the text for the SatPropHigh for PLow based on SI being changed and converting accordingly
        self.lbl_SatPropHigh.setText(SPI(float(self.le_PLow.text())*PC, SI=SI).txtOut)

    def newPHigh(self):
        """
        This function changes the PHigh value and updates the model based on inputs from the user.
        :return:
        """
        # Creating a shortcut for the radio button SI being checked
        SI=self.rb_SI.isChecked()
        # Creating a conversion factor for pressure if SI/English is checked
        PC=100 if SI else UC.psi_to_kpa
        # Set the text for SatPropHigh for PHigh based on SI being changed and converting accordingly
        self.lbl_SatPropHigh.setText(SPI(float(self.le_PHigh.text())*PC, SI=SI).txtOut)
        self.SelectQualityOrTHigh()

    def newUnits(self):
        """
        This function updates the unit outputs based on what the user selects, between SI and English.
        :return:
        """
        # Update units if SI is checked
        self.RC.updateUnits(self.widgets, self.otherwidgets, SI=self.rb_SI.isChecked())

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
        self.gb_Output.layout().addWidget(self.canvas, 6)# ,0,1,6) # THIS LINE IS GIVING AN ERROR: ARG 3 TYPE 'INT'
        self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

    #since my main window is a widget, I can customize its events by overriding the default event
    def mouseMoveEvent(self, event):
        self.oldXData=event.xdata if event.xdata is not None else self.oldXData
        self.oldYData=event.ydata if event.ydata is not None else self.oldYData
        # Updating units if SI is checked, otherwise change to English units
        sUnit='KJ/(kg*K)' if self.rb_SI.isChecked() else 'BTU/(lb*R)'
        TUnit='C' if self.rb_SI.isChecked() else 'F'
        # Updating the window title based on whether SI/English is checked
        self.setWindowTitle('s:{:0.2f} {}, T:{:0.2f} {}'.format(self.oldXData, sUnit, self.oldYData, TUnit))

    def Calculate(self):
        #use rankineController to update the model based on user inputs
        self.RC.updateModel((self.le_PHigh, self.le_PLow, self.rdo_Quality, self.le_TurbineInletCondition, self.le_TurbineEff))

    def SelectQualityOrTHigh(self):
        """
        Actions for the code to take when quality or thigh is selected.
        :return:
        """
        PC = 100 if self.rb_SI.isChecked() else UC.psi_to_kpa
        if self.rdo_Quality.isChecked():
            self.le_TurbineInletCondition.setText("1.0")
            self.le_TurbineInletCondition.setEnabled(False)
        else:
            SI = self.rb_SI.isChecked()
            Tsat=SPI(float(self.le_PHigh.text())*PC).TSat
            Tsat=Tsat if SI else UC.C_to_F(Tsat)
            self.le_TurbineInletCondition.setText("{:0.2f}".format(Tsat))
            self.le_TurbineInletCondition.setEnabled(True)
        x=self.rdo_Quality.isChecked()
        self.lbl_TurbineInletCondition.setText(("Turbine Inlet: {}{} =".format('x' if x else 'THigh', '' if x else ('(C)' if SI else '(F)'))))

#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    sys.exit(app.exec())
