#ifndef Movement_h
#define Movement_h

#include "Arduino.h"
#include "Config.h"

#include <AccelStepper.h>

class Movement
{
    public:
        Movement();
        void Move();
        void SetTargetPosition(float x, float y, float z);
        bool IsMovingToTarget() {return isMovingToTarget;}

    private:
        float position[3] = {0, 0, 0};
        float targetPosition[3] = {0, 0, 0};
        bool isMovingToTarget = false;
        AccelStepper xStepper = AccelStepper(1, XDRIVERSTEPPIN, XDRIVERDIRECTIONPIN);
};

#endif