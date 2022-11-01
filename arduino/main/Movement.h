#ifndef Movement_h
#define Movement_h

#include "Arduino.h"
#include "Config.h"

#include <AccelStepper.h>
#include <MultiStepper.h>

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
        bool xMoving = false;
        bool yMoving = false;
        bool zMoving = false;

        AccelStepper xStepper = AccelStepper(1, XDRIVERSTEPPIN, XDRIVERDIRECTIONPIN);
        AccelStepper yStepper = AccelStepper(1, YDRIVERSTEPPIN, YDRIVERDIRECTIONPIN);
        AccelStepper yyStepper = AccelStepper(1, YYDRIVERSTEPPIN, YYDRIVERDIRECTIONPIN);
        AccelStepper zStepper = AccelStepper(1, ZDRIVERSTEPPIN, ZDRIVERDIRECTIONPIN);
        MultiStepper steppers;
        void SyncMovementXY(float x, float y);
        void SetDefaultSpeed();
};

#endif