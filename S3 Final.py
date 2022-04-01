import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.widgets import CheckButtons
import tkinter as tk


#Checkboxes switch visibilty when clicked 
#==================================================================
def func(label):
    global line1, line2, line3, line4, line5, line6, line7, line1Full, line2Full, line3Full, line4Full, line5Full, line6Full, line7Full
    if label == names[0]:
        line1.set_visible(not line1.get_visible())
        line1Full.set_visible(not line1Full.get_visible())
    elif label == names[1]:
        line2.set_visible(not line2.get_visible())
        line2Full.set_visible(not line2Full.get_visible())
    elif label == names[2]:
        line3.set_visible(not line3.get_visible())
        line3Full.set_visible(not line3Full.get_visible())
    elif label == names[3]:
        line4.set_visible(not line4.get_visible())
        line4Full.set_visible(not line4Full.get_visible())
    elif label == names[4]:
        line5.set_visible(not line5.get_visible())
        line5Full.set_visible(not line5Full.get_visible())
    elif label == names[5]:
        line6.set_visible(not line6.get_visible())
        line6Full.set_visible(not line6Full.get_visible())
    elif label == names[6]:
        line7.set_visible(not line7.get_visible())
        line7Full.set_visible(not line7Full.get_visible())
    plt.draw()
    return


#Math - Euler's Method and Flow Rates
#==================================================================
def dC(LeavingCompartment):
    global EquilibriumNCalc, Flowrates, dN, change
    SUM = 0
    for i in range(7):
        SUM += Flowrates[i][LeavingCompartment]
    change = sum(Flowrates[LeavingCompartment]) - SUM
    return change

def Euler(LeavingCompartment, current, dt):
    global EquilibriumNCalc, Flowrates, dN
    result = dN[LeavingCompartment][current - 1] + (dC(LeavingCompartment) * dt)
    if result <= 0:
        result = 0        
    return result

def graphit():
    global n, EquilibriumNCalc, FCalc, Flowrates, constant, dN, NEquilibrium, Flowrates, line1, line2, line3, line4, line5, line6, line7, line1Full, line2Full, line3Full, line4Full, line5Full, line6Full, line7Fullline1, names, time, educationProbability
    #Defines all the variables
    #------------------------------------------------------------------

    educationProbability = np.zeros(501)
    educationProbability[0] = .25
    for i in range(1,501):
        educationProbability[i] = .25 + (.1 * i) / 500 #q
    Recruitment = 14 #^
    Transmission = 2 #B
    HeavyQuitters = 0.25 #y2
    Mortality = 0.014 #u
    NonSmokerCancer = 0.00001 #pn
    SecondHandSmokeCancer = 0.0001 #ps
    EducatedSecondHandSmokeCancer = 0.00001 #Be
    LightToHeavy = 0.60 #y1
    LightStop = 0.50 #a1
    LungCancerMortality = 0.016 #d/.
    LightQuitPerm = 0.025 #p1
    HeavyQuitPerm = 0.025 #p2
    QuitterLungCancer = 0.005 #&q
    HeavyLungCancer = 0.03 #&2
    LightLungCancer = 0.015 #&1
    NonSmokers = 500 #N
    LightSmokers = 200 #I1
    HeavySmokers = 200 #I2
    TotalPopulation = 1700 #T
    LikelyReturn = 200 #S
    Educated = 200 #E
    Quitters = 200 #Q
    PeopleWithLungCancer = 200 #L


##0#Non   
##1#LightSmoker
##2#Heavy
##3#Quitter
##4#Likely
##5#Lung
##6#Educated 

    year = 50
    n = int(year / dt.get())
    time = np.linspace(0, year, n + 1)
    NEquilibrium = np.array([500, 200, 200, 200, 200, 200, 200])
    Flowrates = np.array([[-(Mortality*NonSmokers), (((1-NonSmokerCancer)*Transmission*NonSmokers)*(LightSmokers+HeavySmokers))/TotalPopulation, (1 - educationProbability[0])*Recruitment, 0, 0,
                                   (NonSmokerCancer*Transmission*NonSmokers)*(LightSmokers+HeavySmokers)/TotalPopulation, 0],
     [-Mortality*LightSmokers, (1-NonSmokerCancer)*(Transmission*NonSmokers), LightToHeavy*LightSmokers, LightQuitPerm*LightStop*LightSmokers, 0, LightLungCancer*LightSmokers, 0],
     [-Mortality*HeavySmokers, 0, 0, HeavySmokers*HeavyQuitPerm*HeavyQuitters, (1-HeavyQuitPerm)*HeavySmokers*HeavyQuitters, HeavyLungCancer*HeavySmokers, 0],
     [-Mortality*Quitters, 0, 0, 0, 0, QuitterLungCancer*Quitters, 0],
     [-LikelyReturn*Mortality, 0, 0, 0, 0, (((1-SecondHandSmokeCancer)*Transmission*LikelyReturn)*(LightSmokers+HeavySmokers))/TotalPopulation, 0],
     [((1-SecondHandSmokeCancer)*(Transmission*LikelyReturn))*(LightSmokers+HeavySmokers)/TotalPopulation, -(Mortality + LungCancerMortality) * PeopleWithLungCancer, 0, 0, 0, 0, 0],
     [-(Mortality*Educated), 0, 0, 0, 0, ((EducatedSecondHandSmokeCancer*Educated)*(LightSmokers+HeavySmokers))/TotalPopulation, educationProbability[0]*Recruitment]])
    
    

    #Sets up all the values for each iteration
    #------------------------------------------------------------------
    dN = np.zeros([7, n + 1])
    for i in range(7): 
        dN[i][0] = NEquilibrium[i] #Set initial NEquilibrium values at t = 0
    for i in range(1, n + 1):
        for j in range(7):
            dN[j][i] = Euler(j, i, dt.get()) #Calculates each N value per iteration
            Flowrates = np.array([[-(Mortality*NonSmokers), (((1-NonSmokerCancer)*Transmission*dN[0][i-1])*(dN[1][i-1]+dN[2][i-1]))/(dN[0][i-1]+dN[1][i-1]+dN[2][i-1]+dN[3][i-1]+dN[4][i-1]+dN[5][i-1]+dN[6][i-1])
, (1 - educationProbability[i])*Recruitment, 0, 0,
                                   (NonSmokerCancer*Transmission*dN[0][i-1])*(dN[1][i-1]+dN[2][i-1])/(dN[0][i-1]+dN[1][i-1]+dN[2][i-1]+dN[3][i-1]+dN[4][i-1]+dN[5][i-1]+dN[6][i-1])
, 0],
     [-Mortality*LightSmokers, (1-NonSmokerCancer)*(Transmission*NonSmokers), LightToHeavy*dN[1][i-1], LightQuitPerm*LightStop*dN[1][i-1], 0, LightLungCancer*dN[1][i-1], 0],
     [-Mortality*HeavySmokers, 0, 0, dN[2][i-1]*HeavyQuitPerm*HeavyQuitters, (1-HeavyQuitPerm)*HeavySmokers*HeavyQuitters, HeavyLungCancer*dN[2][i-1], 0],
     [-Mortality*Quitters, 0, 0, 0, 0, QuitterLungCancer*dN[3][i-1], 0],
     [-LikelyReturn*Mortality, 0, 0, 0, 0, (((1-SecondHandSmokeCancer)*Transmission*dN[4][i-1])*(dN[1][i-1]+ dN[2][i-1]))/(dN[0][i-1]+dN[1][i-1]+dN[2][i-1]+dN[3][i-1]+dN[4][i-1]+dN[5][i-1]+dN[6][i-1])
, 0],
     [((1-SecondHandSmokeCancer)*(Transmission*dN[4][i-1]))*(dN[1][i-1]+dN[2][i-1])/(dN[0][i-1]+dN[1][i-1]+dN[2][i-1]+dN[3][i-1]+dN[4][i-1]+dN[5][i-1]+dN[6][i-1])
, -(Mortality + LungCancerMortality) * PeopleWithLungCancer, 0, 0, 0, 0, 0],
     [-Mortality*Educated, 0, 0, 0, 0, ((EducatedSecondHandSmokeCancer*dN[6][i-1])*(dN[1][i-1]+dN[2][i-1]))/(dN[0][i-1]+dN[1][i-1]+dN[2][i-1]+dN[3][i-1]+dN[4][i-1]+dN[5][i-1]+dN[6][i-1])
, educationProbability[i]*Recruitment]])
    
    #Create subplots
    #------------------------------------------------------------------
    fig = plt.figure(figsize = (20,10))
    dNN = np.zeros([7,int((n/25)+1)])
    timetwo = time[:21]
    for i in range(7):
        for j in range(int((n/25)+1)):
            dNN[i][j] = dN[i][j]
            
    ax = fig.add_subplot(121)
    line1, = ax.plot(timetwo, dNN[0], visible=True)
    line2, = ax.plot(timetwo, dNN[1], visible=True)
    line3, = ax.plot(timetwo, dNN[2], visible=True)
    line4, = ax.plot(timetwo, dNN[3], visible=True)
    line5, = ax.plot(timetwo, dNN[4], visible=True)
    line6, = ax.plot(timetwo, dNN[5], visible=True)
    line7, = ax.plot(timetwo, dNN[6], visible=True)

    ax2 = fig.add_subplot(122)
    line1Full, = ax2.plot(time, dN[0], visible=True)
    line2Full, = ax2.plot(time, dN[1], visible=True)
    line3Full, = ax2.plot(time, dN[2], visible=True)
    line4Full, = ax2.plot(time, dN[3], visible=True)
    line5Full, = ax2.plot(time, dN[4], visible=True)
    line6Full, = ax2.plot(time, dN[5], visible=True)
    line7Full, = ax2.plot(time, dN[6], visible=True)
    
    plt.subplots_adjust(left=0.27)
    
    plt.xlabel('years')
    plt.ylabel('Populations')
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(("Nonsmokers", "Light Smokers", "Heavy Smokers",
                "Quitters", "Likely to Return", "Lung Cancer", "Educated"),
               loc = 'upper center',bbox_to_anchor=(0.5, 1.11), ncol = 4, prop = fontP)
    plt.axhline(0, color='black', lw=2)
    plt.axvline(0, color='black', lw=2)
    rax = plt.axes([0.03, 0.35, 0.2, 0.35])

    check = CheckButtons(rax, ("Nonsmoker", "Light Smokers", "Heavy Smokers",
         "Quitters", "Likely to Return", "Lung Cancer", "Educated"),
                                (True, True, True, True, True, True, True))
    check.on_clicked(func)
    plt.show()
    return


#Kill window
#==================================================================
def killit():
    plt.close()
    return

#Name labels
#==================================================================

names = np.array(["Nonsmoker", "Light Smokers", "Heavy Smokers",
         "Quitters", "Likely to Return", "Lung Cancer", "Educated"])


#Entry boxes, buttons, and variables
#==================================================================
root = tk.Tk()
f1 = tk.Frame(root)
#Assign coefficient variables
dt = tk.DoubleVar()
dt.set(0.1)
dtLabel = tk.Label(f1, text = 'Enter dt:')
dtEntry = tk.Entry(f1, textvariable = dt)
button1 = tk.Button(root, text='Graph It', command=graphit)
button2 = tk.Button(root, text = 'Kill Graph Window', command = killit)

#Grid and pack everything
#==================================================================
dtLabel.grid(row = 8, column = 1)
dtEntry.grid(row = 8, column = 2)
f1.pack()
button1.pack()
button2.pack()


root.mainloop()
