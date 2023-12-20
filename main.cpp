#include <iostream>
#include <vector>
#include <cmath>

using namespace std;


double Final_Drive_Ratio = 2;
double Throttle = 0.5;
int Gear = 0;
double RPM = 0;
double Shaft_Radius = .1;
double Drivetrain_Contact_Area = 5;
double Friction_Coefficient = .01;

std::vector<std::vector<double>> torque_table = {
        {0, 0},
        {500, 16},
        {1000, 295},
        {2000, 396},
        {3000, 435},
        {4000, 395},
        {5000, 338},
        {6000, 257},
        {7000, 200},
        {8000, 85},
        {9000, 10}
    };
    std::vector<std::vector<double>> Gear_Ratios = {
        {2.5, 7000},
        {2, 6500},
        {1.7, 6000},
        {1.3, 5700},
        {1.1, 0}
    };

double clamp(double Input, double LB, double UB) {
    if (Input < LB) {
        Input = LB;
    } else if (Input > UB) {
        Input = UB;
    }
    return Input;
}

double Calc_Engine_Torque(double LOCAL_RPM) {
    int lower_Indx = 0;
    int upper_Indx = 0;
    int count = 0;
    for (int i = 0; i < torque_table.size(); i++) {
        if (torque_table[i][0] < LOCAL_RPM) {
            lower_Indx = i;
        }
        if (torque_table[i][0] > LOCAL_RPM) {
            upper_Indx = i;
            break;
        }
        count += 1;
    }
    double x = (LOCAL_RPM - torque_table[lower_Indx][0]) / (torque_table[upper_Indx][0] - torque_table[lower_Indx][0]);
    double torque = torque_table[lower_Indx][1] + ((torque_table[upper_Indx][1] - torque_table[lower_Indx][1]) * x);
    return torque;
}

double Calc_Engine_RPM(double Angular_Force, double LOCAL_Load, double LOCAL_RPM) {
    double Friction = pow((LOCAL_RPM) * (Drivetrain_Contact_Area * Friction_Coefficient), 1);
    LOCAL_RPM += (Angular_Force - Friction - LOCAL_Load);
    LOCAL_RPM = clamp(LOCAL_RPM, 0, 999999);
    return LOCAL_RPM;
}

double Calc_Combustion_Force(double My_Throttle, double Cyl_Head_Area, double AFR, double Cyl_Count, double Engine_Temp_K) {
    double Optimal_AFR = 12;
    double Mult_Factor = 7.5;
    double My_Combustion_Force = ((AFR - abs(AFR - (Optimal_AFR))) / Optimal_AFR) * Cyl_Head_Area * Cyl_Count * Mult_Factor + (Engine_Temp_K * .05) * My_Throttle;
    return My_Combustion_Force;
}

int auto_gearbox(double MY_RPM) {
    int LOCAL_Gear = Gear;
    if (MY_RPM > Gear_Ratios[Gear][1] && Gear < 4) {
        return LOCAL_Gear + 1;
    } else if (MY_RPM < 1000 && Gear > 0) {
        return LOCAL_Gear - 1;
    }
    return LOCAL_Gear;
}

int main() {
    double Ambient_Temperature_K = 300;
    bool Clutch_Engaged = true;
    double Moment_Of_Intertia = 1;

    double Combustion_Force = Calc_Combustion_Force(1, 15, 12, 4, 300);
    std::cout << "FORCE: " << Combustion_Force << "\n";
    double Shift_Delay = 20;
    double Base_Load = 500;
    for (int i = 0; i < 200; i++) {
        double Load = (1 / Gear_Ratios[Gear][0]) * Base_Load;
        if (Clutch_Engaged) {
            Load = (1 / ((Gear_Ratios[Gear][0]) * Final_Drive_Ratio)) * Base_Load;
        }
        RPM = Calc_Engine_RPM(Combustion_Force, Load, RPM);
        if (i % 5 == 0) {
            std::cout << "RPM: " << RPM << " | GEAR: " << Gear << std::endl;
        }
        double Torque = Calc_Engine_Torque(RPM);
        double Gear_Ratio = Gear_Ratios[Gear][0];
        double Tire_Radius = 2;
        double Output_Force = Torque * Gear_Ratio * Tire_Radius;
        Shift_Delay -= 1;
        if (Shift_Delay < 0) {
            Gear = auto_gearbox(RPM);
            Shift_Delay = 20;
        }
    }
    return 0;
}
