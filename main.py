# https://engineering.stackexchange.com/questions/7702/calculating-car-engine-rpm-for-game

'''
Clutch engaged:
As hazzey mentioned in the comments,
the engine will turn at a gear ratio of the wheel speed.
Take your RPM and put it into the torque curve(for your given throttle position)
to give you torque. Torque times your gear ratio and tire radius gives you force.
Then solve F=MA with the mass of the vehicle to give you acceleration.
Then use the kinematic equation v=a*t+v0 to solve for your new velocity based on your current velocity and time step.
Which then is used to calculate your new RPM... and so goes the iteration.
Similarly you could solve it with kinetic energy equations instead.
'''

'''
Clutch disengaged:
This case can be modeled by considering energy input and internal friction of the engine.
When you stop pressing on the gas, even without the wheels on the ground, the system will slow down.
You could measure this for a particular car empirically by graphing RPMs when throttle input is removed.
The only difference between the wheels off the ground and the clutch disengaged is the amount of inertia or kinetic energy that is stored in the spinning system and additional friction imposed by the other spinning components.
This could also be determined empirically.
'''

def clamp(Input, LB, UB):
    if Input < LB:
        Input = LB
    elif Input > UB:
        Input = UB
    return Input

Ambient_Temperature_K = 300 # In kelvin

Clutch_Engaged = True

Moment_Of_Intertia = 1

torque_table = [ #{RPM, Torque} // Torque is in NM
[0,0],
[500, 16],
[1000, 295],
[2000,396],
[3000, 435],
[4000, 395],
[5000, 338],
[6000, 257],
[7000, 200],
[8000, 85],
[9000, 10]
]

#Shift RPM, Gear
Gear_Ratios = [[2.5, 7000], [2, 6500], [1.5, 6000], [1.3, 5700], [1.1, 0]]
Final_Drive_Ratio = 2

Throttle = 0.5

Gear = 0

RPM = 0

def Calc_Engine_Torque(LOCAL_RPM):
    lower_Indx = 0
    upper_Indx = 0
    count = 0
    for i in range(len(torque_table)):
        if (torque_table[i][0] < LOCAL_RPM):
            lower_Indx = i
        if (torque_table[i][0] > LOCAL_RPM):
            upper_Indx = i
            break
        count += 1
    x = (LOCAL_RPM - torque_table[lower_Indx][0]) / (torque_table[upper_Indx][0] - torque_table[lower_Indx][0])
    torque = torque_table[lower_Indx][1] + ((torque_table[upper_Indx][1] - torque_table[lower_Indx][1]) * x)
    return torque

Shaft_Radius = .1
Drivetrain_Contact_Area = 5
Friction_Coefficient = .01

def Calc_Engine_RPM(Angular_Force, LOCAL_Load, LOCAL_RPM): # Force from combustion
    Friction = pow((LOCAL_RPM) * (Drivetrain_Contact_Area * Friction_Coefficient), 1)

    LOCAL_RPM +=  (Angular_Force - Friction - LOCAL_Load)

    LOCAL_RPM = clamp(LOCAL_RPM, 0, 999999)
    return LOCAL_RPM

#
def Calc_Combustion_Force(My_Throttle, Cyl_Head_Area, AFR, Cyl_Count, Engine_Temp_K):
    Optimal_AFR = 12
    Mult_Factor = 7.5
    My_Combustion_Force = ((AFR - abs(AFR - (Optimal_AFR))) / Optimal_AFR) * Cyl_Head_Area * Cyl_Count * Mult_Factor + (Engine_Temp_K * .05) * My_Throttle
    return My_Combustion_Force

def Calc_Engine_Temperature

def auto_gearbox(MY_RPM):
    LOCAL_Gear = Gear
    if (MY_RPM > Gear_Ratios[Gear][1] and Gear < 4):
        return LOCAL_Gear + 1
    elif (MY_RPM < 1000 and Gear > 0):
        return LOCAL_Gear - 1
    return LOCAL_Gear


# Combustion_Force = 500
Combustion_Force = Calc_Combustion_Force(1, 15, 12, 4, 300)
print("FORCE: ", Combustion_Force)
Shift_Delay = 20 # In ticks
Base_Load = 500 # Load the vehicle
for i in range(0, 200, 1):
    Load = (1 / Gear_Ratios[Gear][0]) * Base_Load
    if (Clutch_Engaged):
        Load = (1 / ((Gear_Ratios[Gear][0]) * Final_Drive_Ratio)) * Base_Load
        
    RPM = Calc_Engine_RPM(Combustion_Force, Load, RPM)
    if i % 5 == 0:
        print("RPM: ", RPM , " | GEAR: " , Gear)
    Torque = Calc_Engine_Torque(RPM)
    Gear_Ratio = Gear_Ratios[Gear][0]
    Tire_Radius = 2 # in ft
    Output_Force = Torque * Gear_Ratio * Tire_Radius
    Shift_Delay -= 1
    if (Shift_Delay < 0):
        Gear = auto_gearbox(RPM)
        Shift_Delay = 20
