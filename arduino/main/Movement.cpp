#include "Arduino.h"
#include "Movement.h"

bool compareFloats(float A, float B, float tolerance = 0.05f)
{
    return (fabs(A - B) < tolerance);
}

Movement::Movement()
{
    steppers.addStepper(xStepper);
    steppers.addStepper(yStepper);
    steppers.addStepper(yyStepper);

    steppers.setMaxSpeed(XYMAXSPEED);
    zStepper.setSpeed(ZMAXSPEED);
    SetNormalSpeed();
}

void Movement::SetNormalSpeed()
{
    tStepper.setSpeed(TMAXSPEED);
}

void Movement::SetTravelSpeed()
{
    tStepper.setSpeed(TMAXTRAVELSPEED);
}

void Movement::SetSpeedXY(float speed)
{
    steppers.setMaxSpeed(speed);
}

void Movement::SetSpeedZ(float speed)
{
    zStepper.setSpeed(speed);
}

void Movement::SetTargetPosition(float x, float y, float z, float t)
{
    xytMoving = false;
    zMoving = false;

    isMovingToTarget = true;

    if (!isnan(x))
    {
        steppers.setTargetPosition(x * MICROSTEPPING * XSTEPPERMM, 0);
        xytMoving = true;
    }
    if (!isnan(y))
    {
        steppers.setTargetPosition(y * MICROSTEPPING * YSTEPPERMM, 1);
        steppers.setTargetPosition(y * MICROSTEPPING * YSTEPPERMM, 2);

        xytMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.setTargetPosition(z * 10);
        zMoving = true;
    }
    if (!isnan(t))
    {
        zStepper.setTargetPosition(t * MICROSTEPPING * TSTEPPERDEG);
        xytMoving = true;
    }
}

void Movement::Update()
{
    int moved = 0;

    if(xytMoving)
    {
        xytMoving = steppers.run();
        moved++;
    }

    if(zMoving)
    {
        zMoving = zStepper.run();
        moved++;
    }

    if (moved == 0)
    {
        isMovingToTarget = false;
    }
}