from Calc_state import Steam_SI as steam
from Calc_state import SatPropsIsobar
from Calc_state import UnitConverter as UC
import numpy as np
from matplotlib import pyplot as plt

# Group Members: Christy Cravens, Robert Lucas, and Gabe Moya
#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class rankineModel():
    def __init__(self):
        '''
        Constructor for rankine power cycle data (in the Model-View-Controller design pattern).  This class
        is for storing data only.  The Controller class should update the model depending on input from the user.
        The View class should display the model data depending on the desired output.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param eff_turbine: isentropic efficiency of the turbine
        :param name: a convenient name
        '''
        self.p_low=None
        self.p_high=None
        self.t_high=None
        self.name=None
        self.efficiency=None
        self.turbine_eff=None
        self.turbine_work=None
        self.pump_work=None
        self.heat_added=None
        self.state1=None
        self.state2s=None
        self.state2=None
        self.state3=None
        self.state4=None
        self.SI=True

class rankineController():
    def __init__(self, *args):
        """
        Create rankineModel object.  The rankineController class updates the model based on user input
        and updates the rankineView as well
        :param *args: a tuple containing widgets that get updated in the View
        """

        self.Model=rankineModel()
        self.View=rankineView()
        self.Widgets=args[0]

    def updateModel(self, *args):
        """
        I'm expecting a tuple of input widgets from the GUI.  Read and apply them here.
        :param args: a tuple of input widgets, other arguments such as SI or ENG
        :return: nothing
        """
        #unpack tuple of input widgets
        le_PHigh, le_PLow, rdo_Quality, le_TurbineInletCondition, le_TurbineEff=args[0]

        # Converter for PHigh/PLow based on selection of SI or English
        PC = 100 if self.Model.SI else UC.psi_to_kpa

        #update the model
        self.Model.p_high = float(le_PHigh.text()) * PC  # get the high pressure isobar in kPa
        self.Model.p_low = float(le_PLow.text()) * PC  # get the low pressure isobar in kPa

        # Shortcut for the turbine inlet float value
        TI = float(le_TurbineInletCondition.text())
        # If SI/English is selected, the output is modified accordingly with the latter if/else statement
        self.Model.t_high = None if rdo_Quality.isChecked() else (TI if self.Model.SI else UC.F_to_C(TI))

        self.Model.turbine_eff = float(le_TurbineEff.text())
        # do the calculation
        self.calc_efficiency()
        self.updateView(self.Widgets)

    def calc_efficiency(self):
        # calculate the 4 states
        # state 1: turbine inlet (p_high, t_high) superheated or saturated vapor
        if (self.Model.t_high == None):
            self.Model.state1 = steam(self.Model.p_high, x=1.0,
                                name='Turbine Inlet')  # instantiate a steam object with conditions of state 1 as saturated steam, named 'Turbine Inlet'
        else:
            self.Model.state1 = steam(self.Model.p_high, T=self.Model.t_high,
                                name='Turbine Inlet')  # instantiate a steam object with conditions of state 1 at t_high, named 'Turbine Inlet'
        # state 2: turbine exit (p_low, s=s_turbine inlet) two-phase
        self.Model.state2s = steam(self.Model.p_low, s=self.Model.state1.s,
                             name="Turbine Exit")  # instantiate a steam object with conditions of state 2s, named 'Turbine Exit'
        if self.Model.turbine_eff < 1.0:  # eff=(h1-h2)/(h1-h2s) -> h2=h1-eff(h1-h2s)
            h2 = self.Model.state1.h - self.Model.turbine_eff * (self.Model.state1.h - self.Model.state2s.h)
            self.Model.state2 = steam(self.Model.p_low, h=h2, name="Turbine Exit")
        else:
            self.Model.state2 = self.Model.state2s
        # state 3: pump inlet (p_low, x=0) saturated liquid
        self.Model.state3 = steam(self.Model.p_low, x=0,
                            name='Pump Inlet')  # instantiate a steam object with conditions of state 3 as saturated liquid, named 'Pump Inlet'
        # state 4: pump exit (p_high,s=s_pump_inlet) typically sub-cooled, but estimate as saturated liquid
        self.Model.state4 = steam(self.Model.p_high, s=self.Model.state3.s, name='Pump Exit')
        self.Model.state4.h = self.Model.state3.h + self.Model.state3.v * (self.Model.p_high - self.Model.p_low)

        self.Model.turbine_work = self.Model.state1.h - self.Model.state2.h  # calculate turbine work
        self.Model.pump_work = self.Model.state4.h - self.Model.state3.h  # calculate pump work
        self.Model.heat_added = self.Model.state1.h - self.Model.state4.h  # calculate heat added
        self.Model.efficiency = 100.0 * (self.Model.turbine_work - self.Model.pump_work) / self.Model.heat_added
        return self.Model.efficiency

    def updateView(self, *args):
        """
        This is a pass-through function that calls and identically named function in the View, but passes along the
        Model as an argument.
        :param args: A tuple of Widgets that get unpacked and updated in the view
        :return:
        """
        self.View.outputToGUI(args[0], Model=self.Model)

    def setRankine(self,p_low=8, p_high=8000, t_high=None, eff_turbine=1.0, name='Rankine Cycle'):
        '''
        Set model values for rankine power cycle.  If t_high is not specified, the State 1
        is assigned x=1 (saturated steam @ p_high).  Otherwise, use t_high to find State 1.
        :param p_low: the low pressure isobar for the cycle in kPa
        :param p_high: the high pressure isobar for the cycle in kPa
        :param t_high: optional temperature for State1 (turbine inlet) in degrees C
        :param eff_turbine: isentropic efficiency of the turbine
        :param name: a convenient name
        '''
        self.Model.p_low=p_low
        self.Model.p_high=p_high
        self.Model.t_high=t_high
        self.Model.name=name
        self.Model.efficiency=None
        self.Model.turbine_eff=eff_turbine
        self.Model.turbine_work=0
        self.Model.pump_work=0
        self.Model.heat_added=0
        self.Model.state1=None
        self.Model.state2s=None
        self.Model.state2=None
        self.Model.state3=None
        self.Model.state4=None

    def print_summary(self):
        """
        A pass-thrugh method for accessing View and passing Model.
        :return:
        """
        self.View.print_summary(Model=self.Model)

    def plot_cycle_TS(self, axObj=None):
        """
        A pass-thrugh method for accessing View and passing Model.
        :return:
        """
        self.View.plot_cycle_TS(axObj=axObj, Model=self.Model)

    def updateUnits(self, w, ow, SI=True):
        """
        This function updates the units from SI to English or vice versa.
        :param args: Widgets to update
        :param SI: True = SI is selected
        :return:
        """
        # I've got to pass the correct set of widgets to work on.
        # I'll pass them through *args.  In the app, I define self.widgets and self.other widgets
        # I'll pass these widgets along to the view as well as the model
        # in the view, I will unpack the widgets, change numerical values, label units and the chart
        self.Model.SI=SI
        # Update the view with the new units
        self.View.newUnits(w, ow, Model=self.Model)
        pass

    def newUnits(self):
        """
        This function updates the unit outputs based on what the user selects, between SI and English.
        :return:
        """
        self.RC.updateUnits(self.widgets, self.otherwidgets, SI=self.rb_SI.isChecked())
        return


class rankineView():
    def __init__(self):
        """
        Empty constructor by design
        """

    def outputToGUI(self, *args, Model=None):
        widgets=args[0]
        #unpack the args
        le_H1, le_H2, le_H3, le_H4, le_TurbineWork, le_PumpWork, le_HeatAdded, le_Efficiency, lbl_SatPropHigh, lbl_SatPropLow, ax, canvas = widgets

        if len(args)>1:
            otherwidgets = args[1]

        #update the line edits and labels
        # Creating shortcuts to call in the lines below; less to type each time
        H1=Model.state1.h; H2=Model.state2.h; H3=Model.state3.h; H4=Model.state4.h
        TW=Model.turbine_work; PW=Model.pump_work; HA=Model.heat_added

        # Added if/else statements below based on if the user has selected SI or English units.
        # These statements convert the values for H1, H2, H3, H4, Turbine Work, Pump Work, and Heat Added
        le_H1.setText("{:0.2f}".format(Model.state1.h)) #H1 if Model.SI else UC.kJperkg_to_BTUperlb(H1)))
        le_H2.setText("{:0.2f}".format(Model.state2.h)) #H2 if Model.SI else UC.kJperkg_to_BTUperlb(H2)))
        le_H3.setText("{:0.2f}".format(Model.state3.h)) #H3 if Model.SI else UC.kJperkg_to_BTUperlb(H3)))
        le_H4.setText("{:0.2f}".format(Model.state4.h)) #H4 if Model.SI else UC.kJperkg_to_BTUperlb(H4)))
        le_TurbineWork.setText("{:0.2f}".format(Model.turbine_work)) #TW if Model.SI else UC.kJperkg_to_BTUperlb(TW)))
        le_PumpWork.setText("{:0.2f}".format(Model.pump_work)) #PW if Model.SI else UC.kJperkg_to_BTUperlb(PW)))
        le_HeatAdded.setText("{:0.2f}".format(Model.heat_added)) #HA if Model.SI else UC.kJperkg_to_BTUperlb(HA)))

        # Efficiency doesn't need converting and PLow and PHigh are already converted previously in the code
        le_Efficiency.setText("{:0.2f}".format(Model.efficiency))
        lbl_SatPropLow.setText(SatPropsIsobar(Model.p_low).txtOut)
        lbl_SatPropHigh.setText(SatPropsIsobar(Model.p_high).txtOut)

        #update the plot
        ax.clear()
        self.plot_cycle_TS(axObj=ax, Model=Model)
        canvas.draw()

    def newUnits(self,w,ow,Model=None):
        """
        This function updates the unit outputs based on what the user selects, between SI and English.
        :return:
        """
        self.outputToGUI(w,Model=Model)
        # Assigne the tuple of widgets
        lbl_TurbineInletConditon, rdo_Quality, le_PHigh, le_PLow, le_TurbineInletCondition,lbl_PHigh,lbl_PLow,lbl_H1Units,lbl_H2Units,lbl_H3Units,lbl_H4Units,lbl_TurbinWorkUnits,lbl_PumpWorkUnits,lbl_HeatAddedUnits,lbl_SatPropHigh,lbl_SatPropLow=ow
        # Create a shortcut for the pressure conversions based on SI/English selected
        PC=1/100 if Model.SI else UC.kpa_to_psi
        # Set text for PHigh/PLow with conversion
        le_PHigh.setText("{:0.2f}".format(PC*Model.p_high))
        le_PLow.setText("{:0.2f}".format(PC*Model.p_low))
        # If Quality isn't checked, update the text for the Turbine Inlet Condition based on units selected
        if not rdo_Quality.isChecked():
            # Shortcut for the turbine inlet condition text
            T=float(le_TurbineInletCondition.text())
            # Updated shortcut for conversions using the previous shortcut for the turbine inlet condition
            T=UC.F_to_C(T) if Model.SI else UC.C_to_F(T)
            # Temp unit conversion for C or F
            TUnits= "C" if Model.SI else "F"
            # Update the turbine inlet condition output text for F or C
            le_TurbineInletCondition.setText("{:0.2f}".format(T))
            # Update the displayed text for THigh
            lbl_TurbineInletCondition.SetText("Turbine Inlet: THigh({}):".format(TUnits))
        # Update the displayed text for PHigh that has the appropriate conversions
        lbl_PHigh.setText("P High ({})".format('bar' if Model.SI else 'psi'))
        # Update the displayed text for PLow that has the appropriate conversions
        lbl_PLow.setText("P Low ({})".format('bar' if Model.SI else 'psi'))
        # Create a shortcut to update units between kJ/kg and BTU/lb based on if SI/English is selected
        Units="kJ/kg" if Model.SI else "BTU/lb"
        # Update text for the units for H1, H2, H3 & H4
        lbl_H1Units.setText(Units)
        lbl_H2Units.setText(Units)
        lbl_H3Units.setText(Units)
        lbl_H4Units.setText(Units)
        # Update text for the units for Turbine Work, Pump Work, and Heat added
        lbl_TurbineWorkUnits.setText(Units)
        lbl_PumpWorkUnits.setText(Units)
        lbl_HeatAddedUnits.setText(Units)
        return

    def print_summary(self, Model=None):
        """
        Prints to CLI.
        :param Model: a rankineModel object
        :return: nothing
        """
        if Model.efficiency==None:
            Model.calc_efficiency()
        print('Cycle Summary for: ', Model.name)
        print('\tEfficiency: {:0.3f}%'.format(Model.efficiency))
        print('\tTurbine Eff:  {:0.2f}'.format(Model.turbine_eff))
        print('\tTurbine Work: {:0.3f} kJ/kg'.format(Model.turbine_work))
        print('\tPump Work: {:0.3f} kJ/kg'.format(Model.pump_work))
        print('\tHeat Added: {:0.3f} kJ/kg'.format(Model.heat_added))
        Model.state1.print()
        Model.state2.print()
        Model.state3.print()
        Model.state4.print()

    def plot_cycle_TS(self, axObj=None, Model=None):
        """
        I want to plot the Rankine cycle on T-S coordinates along with the vapor dome and shading in the cycle.
        I notice there are several lines on the plot:
        saturated liquid T(s) colored blue
        saturated vapor T(s) colored red
        The high and low isobars and lines connecting state 1 to 2, and 3 to saturated liquid at phigh
        step 1:  build data for saturated liquid line
        step 2:  build data for saturated vapor line
        step 3:  build data between state 3 and sat liquid at p_high
        step 4:  build data between sat liquid at p_high and state 1
        step 5:  build data between state 1 and state 2
        step 6:  build data between state 2 and state 3
        step 7:  put together data from 3,4,5 for top line and build bottom line
        step 8:  make and decorate plot
        Note:  will plot using pyplot if axObj is None else just returns
        :param axObj:  if None, used plt.subplot else a MatplotLib axes object.
        :return:
        """
        #step 1&2:
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs= np.loadtxt('sat_water_table.txt',skiprows=1, unpack=True) #use np.loadtxt to read the saturated properties
        ax = plt.subplot() if axObj is None else axObj

        ax.plot(sfs,ts, color='blue')
        ax.plot(sgs, ts, color='red')

        #step 3:  I'll just make a straight line between state3 and state3p
        st3p=steam(Model.p_high,x=0) #saturated liquid state at p_high
        svals=np.linspace(Model.state3.s, st3p.s, 20)
        tvals=np.linspace(Model.state3.T, st3p.T, 20)
        line3=np.column_stack([svals, tvals])
        #plt.plot(line3[:,0], line3[:,1])

        #step 4:
        sat_pHigh=steam(Model.p_high, x=1.0)
        st1=Model.state1
        svals2p=np.linspace(st3p.s, sat_pHigh.s, 20)
        tvals2p=[st3p.T for i in range(20)]
        line4=np.column_stack([svals2p, tvals2p])
        if st1.T>sat_pHigh.T:  #need to add data points to state1 for superheated
            svals_sh=np.linspace(sat_pHigh.s,st1.s, 20)
            tvals_sh=np.array([steam(Model.p_high,s=ss).T for ss in svals_sh])
            line4 =np.append(line4, np.column_stack([svals_sh, tvals_sh]), axis=0)
        #plt.plot(line4[:,0], line4[:,1])

        #step 5:
        svals=np.linspace(Model.state1.s, Model.state2.s, 20)
        tvals=np.linspace(Model.state1.T, Model.state2.T, 20)
        line5=np.array(svals)
        line5=np.column_stack([line5, tvals])
        #plt.plot(line5[:,0], line5[:,1])

        #step 6:
        svals=np.linspace(Model.state2.s, Model.state3.s, 20)
        tvals=np.array([Model.state2.T for i in range(20)])
        line6=np.column_stack([svals, tvals])
        #plt.plot(line6[:,0], line6[:,1])

        #step 7:
        topLine=np.append(line3, line4, axis=0)
        topLine=np.append(topLine, line5, axis=0)
        xvals=topLine[:,0]
        y1=topLine[:,1]
        y2=[Model.state3.T for s in xvals]

        ax.plot(xvals, y1, color='darkgreen')
        ax.plot(xvals, y2, color='black')
        ax.fill_between(xvals, y1, y2, color='gray', alpha=0.5)
        ax.plot(Model.state1.s, Model.state1.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        ax.plot(Model.state2.s, Model.state2.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        ax.plot(Model.state3.s, Model.state3.T, marker='o', markeredgecolor='k', markerfacecolor='w')
        ax.set_xlabel(r's $\left(\frac{kJ}{kg\cdot K}\right)$', fontsize=18)  #different than plt
        ax.set_ylabel(r'T $\left( ^{o}C \right)$', fontsize=18)  #different than plt
        ax.set_title(Model.name)  #different than plt
        ax.grid(visible='both', alpha=0.5)
        ax.tick_params(axis='both', direction='in', labelsize=18)

        sMin=min(sfs)
        sMax=max(sgs)
        ax.set_xlim(sMin, sMax)  #different than plt

        tMin=min(ts)
        tMax=max(max(ts),st1.T)
        ax.set_ylim(tMin,tMax*1.05)  #different than plt

        txt= 'Summary:'
        txt+= '\n$\eta_{cycle} = $'+'{:0.2f}%'.format(Model.efficiency)
        txt+= '\n$\eta_{turbine} = $'+'{:0.2f}'.format(Model.turbine_eff)
        txt+= '\n$W_{turbine} = $'+ '{:0.2f}'.format(Model.turbine_work)+r'$\frac{kJ}{kg}$'
        txt+= '\n$W_{pump} = $'+'{:0.2f}'.format(Model.pump_work)+r'$\frac{kJ}{kg}$'
        txt+= '\n$Q_{in} = $'+ '{:0.2f}'.format(Model.heat_added)+r'$\frac{kJ}{kg}$'
        ax.text(sMin+0.05*(sMax-sMin), tMax, txt, ha='left', va='top', fontsize=18)  #different than plt

        if axObj is None:  # this allows me to show plot if not being displayed on a figure
            plt.show()

def main():
    RC=rankineController()
    RC.setRankine(8,8000,t_high=500, eff_turbine=0.9,name='Rankine Cycle - Superheated at turbine inlet')
    #t_high is specified
    #if t_high were not specified, then x_high = 1 is assumed
    eff=RC.calc_efficiency()
    print(eff)
    RC.print_summary()
    RC.plot_cycle_TS()

if __name__=="__main__":
    main()
