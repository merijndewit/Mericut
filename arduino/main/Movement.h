#ifndef Movement_h
#define Movement_h

#include "Arduino.h"
#include "Config.h"
#include "Stepperi.h"
#include "MultiStepperi.h"

#include <AccelStepper.h>
#include <MultiStepper.h>

class Movement
{
    public:
        Movement();
        void Update();
        void SetTargetPosition(float x, float y, float z, float t);
        bool IsMovingToTarget() {return isMovingToTarget;}
        void SetNormalSpeed();
        void SetTravelSpeed();
        void SetSpeedXY(float speed);
        void SetSpeedZ(float speed);

    private:
        float targetPosition[4] = {0, 0, 0, 0};
        bool isMovingToTarget = false;
        bool xyMoving = false;
        bool tMoving = false;
        bool zMoving = false;
        
        Stepperi xStepper = Stepperi(XDRIVERSTEPPIN, XDRIVERDIRECTIONPIN);
        Stepperi yStepper = Stepperi(YDRIVERSTEPPIN, YDRIVERDIRECTIONPIN);
        Stepperi yyStepper = Stepperi(YYDRIVERSTEPPIN, YYDRIVERDIRECTIONPIN);
        Stepperi zStepper = Stepperi(ZDRIVERSTEPPIN, ZDRIVERDIRECTIONPIN);
        Stepperi tStepper = Stepperi(TDRIVERSTEPPIN, TDRIVERDIRECTIONPIN);
        MultiStepperi steppers;
};

#endif