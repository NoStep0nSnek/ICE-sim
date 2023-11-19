#include <iostream>
#include <vector>

using namespace std;

float clamp(float val, float LB, float UB) {
    if (val < LB) {
        val = LB;
    } else if (val > UB) {
        val = UB;
    }
    return val;
}

float ackermann_value = 1.1;
float steering = .5; // Left and Right (-1 to 1)


int main() {

    float left_wheel = steering+steering*clamp(steering*(ackermann_value/10),-1,0);
    float right_wheel = steering-(steering*clamp(steering*(ackermann_value/10),0,1));
    cout << left_wheel << "\n";
    cout << right_wheel << "\n";

    return 0;
}
