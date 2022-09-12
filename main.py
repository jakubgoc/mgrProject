import csv
import math
import sys
import pyvisa
from matplotlib import pyplot as pyplot

rm = pyvisa.ResourceManager()

helper_list_in_s = []
helper_list_C1_in_V = []
helper_list_C2_in_V = []
list_in_s = []
list_C1_in_V = []
list_C2_in_V = []

valuesOfArcTanInRadians = []
valuesOfArcTanInDegrees = []

valuesOfArcTanInRadians2 = []
valuesOfArcTanInDegrees2 = []

list_X_in_V_To_Plot_Hysteresis = []
list_Y_in_V_To_Plot_Hysteresis = []

phi = []
phiZero = []
k = 0

ostatecznyX = []
ostatecznyY = []

def pyvisa_manger():
    serialInstrumentAtComPort1 = rm.list_resources()[0]
    oscilloscope = rm.open_resource(serialInstrumentAtComPort1)
    print(oscilloscope)

    #Reset the device
    #oscilloscope.query('*RST')

    #Returns the instrument identification.
    print(oscilloscope.query("*IDN?"))

    #Queries the number of horizontal divisions on the screen.
    print(oscilloscope.query("TIMebase:DIVisions?"))

    #Queries the real acquisition time used in the hardware.
    # If FFT analysis is performed, the value can differ from the adjusted
    # acquisition time (TIMebase:ACQTime). #wartosc podstawy czasu
    print(oscilloscope.query("TIMebase:RATime?"))

    #Enables the function generator and outputs the waveform.
    #oscilloscope.query("WGENerator:OUTPut[:ENABle] ON")


    #oscilloscope.query("BPLot: OUTPut CH1 | CH2]")

    oscilloscope.query("FORM CSV")
    oscilloscope.query("CHAN:DATA:POIN DMAX")
    oscilloscope.query("SING;*OPC?")
    print(oscilloscope.query("CHAN:DATA:HEAD?"))
    print(oscilloscope.query("CHAN:DATA?"))

    #List of values according to the format settings -
    # the voltages of recorded waveform samples.
    # print(oscilloscope.query("FORM CSV"))
    # print(oscilloscope.query("CHAN1:DATA?"))

    #Sets the number of waveforms acquired with RUNSingle. (here 2)
    oscilloscope.query("ACQuire:NSINgle:COUNt 2")
    oscilloscope.query("RUNSingle")

    # Executes saving a waveform, for which the path and filename
    # have been defined by EXPort:WAVeform:NAME.
    oscilloscope.query("EXPort:WAVeform:SOURce CH1 | CH2")
    oscilloscope.query("EXPort:WAVeform:NAME HysteresisPlot")
    oscilloscope.query('EXP:WFMS:DEST "/USB_FRONT/WFM"')
    oscilloscope.query("EXPort:WAVeform:SAVE")


def read_csv_file():
    filePath = "WFM01V12.CSV"

    if len(sys.argv) > 1:
        filePath = sys.argv[1]

    with open(filePath, "r", newline="") as file:
        reader = csv.reader(file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
        next(file)
        for row in reader:
            helper_list_in_s.append([row[0]])
            helper_list_C1_in_V.append([row[1]])
            helper_list_C2_in_V.append([row[2]])

        for x in range(len(helper_list_in_s)):
            list_in_s.append(helper_list_in_s[x][0])
            list_C1_in_V.append(helper_list_C1_in_V[x][0])
            list_C2_in_V.append(helper_list_C2_in_V[x][0])

        file.close()


def calculate_arctan():
    for x in range(len(list_in_s)):
        valuesOfArcTanInRadians.append((math.atan(list_C2_in_V[x] / list_C1_in_V[x])))
        valuesOfArcTanInDegrees.append((valuesOfArcTanInRadians[x] * 180 / 3.14))


def calculate_final_arctan_values():
    for x in range(len(ostatecznyX)):
        valuesOfArcTanInRadians2.append((math.atan(ostatecznyY[x] / ostatecznyX[x])))
        valuesOfArcTanInDegrees2.append((valuesOfArcTanInRadians2[x] * 180 / 3.14))


def calculate_hysteresis_period():
    for x in range(len(valuesOfArcTanInDegrees)):
        ostatecznyX.append(list_C1_in_V[x])
        ostatecznyY.append(list_C2_in_V[x])

        if (x != 0 and valuesOfArcTanInDegrees[x] == valuesOfArcTanInDegrees[0]):
            break


#
#
# #def seperate_first_period_loop():
#
#     for x in range(len(valuesOfArcTanInDegrees)):
#         phi[x]=valuesOfArcTanInDegrees[x]
#
#         if (abs(phi[x]) < 5 or (abs(phi[x]) - 90) < 5 or (abs(phi[x])) > 175):
#             phiZero[x] = phi[x]
#
#         while ((abs(phi[x] - phiZero[x]) < 360)):
#
#             if(x!=0 and (phi[x-1] > 0 and phi[x] < 0)):
#                 k=k+1
#
#             if(x!= 0 and (phi[x-1] < 0 and phi[x] > 0)):
#                 k=k-1
#
#             phi[x]=phi[x] + 2*180*k
#             ostatecznyX[x] = list_C1_in_V[x]
#             ostatecznyY[x] = list_C2_in_V[x]

def calculate_hysteresis_area():
    if len(sys.argv) > 2:
        result = 0.0

        if sys.argv[2] == "calculateHysteresisArea":
            print("Calculating Hysteresis Area")
            for i in range(1, len(ostatecznyX)):
                result += ostatecznyY[i] * (ostatecznyX[i] - ostatecznyX[i - 1])
                if (i) == len(ostatecznyX) - 1:
                    result += ostatecznyY[i] * (ostatecznyX[0] - ostatecznyX[i])

        print(abs(result))
        input("Press Enter to continue...")


def plot_figures():
    if len(sys.argv) > 2:
        if sys.argv[2] == "plotHysteresis":
            print("Plotting hysteresis graph")
            plot_hysteresis()

    if len(sys.argv) > 2:
        if sys.argv[2] == "plotArctan":
            print("Plotting arctan graph")
            plot_arctan()

    pyplot.show()


def plot_arctan():
    pyplot.figure(1)
    pyplot.plot(range(len(valuesOfArcTanInDegrees2)), valuesOfArcTanInDegrees2, color='red', label='')
    pyplot.grid(visible=True, which='major', axis='x', color='black', linestyle='--')
    pyplot.grid(visible=True, which='major', axis='y', color='black', linestyle='--')
    pyplot.grid(visible=True, which='minor', axis='x', color='black', linestyle='--')
    pyplot.ylabel('Angle [°]')
    pyplot.xlabel('Time [s]')
    pyplot.title('Angle between current calc point and the point (0,0)')


def plot_hysteresis():
    pyplot.figure(2)
    pyplot.plot(ostatecznyX, ostatecznyY, color='red', label='')
    pyplot.grid(visible=True, which='major', axis='x', color='black', linestyle='--')
    pyplot.grid(visible=True, which='major', axis='y', color='black', linestyle='--')
    pyplot.grid(visible=True, which='minor', axis='x', color='black', linestyle='--')
    pyplot.ylabel('C1 [V]')
    pyplot.xlabel('C2 [V]')
    pyplot.title('Hysteresis plot')

pyvisa_manger()

#E:\Program Files\PuTTY
# read_csv_file()
# calculate_arctan()
# calculate_hysteresis_period()
# calculate_final_arctan_values()
#calculate_hysteresis_area()
#plot_figures()
