#ifndef MultiStepperi_h
#define MultiStepperi_h

#include <Arduino.h>
#include "Stepperi.h"
#include "Config.h"

#define MAXSTEPPERS 5

class MultiStepperi
{
    public:
        MultiStepperi();
        void addStepper(Stepperi& stepper);
        void setTargetPosition(int stepperPosition, int stepper);
        void setMaxSpeed(float speed);
        bool run();

    private:
        Stepperi* steppers[MAXSTEPPERS]; //max amount of steppers is 5
        int stepperCount;
        float steppersMaxSpeed[MAXSTEPPERS];
        float maxSpeed;
        void calculateSpeed();
};

#endif