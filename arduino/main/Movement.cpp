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
    tStepper.setSpeed(TMAXSPEED);

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
    xyMoving = false;
    tMoving = false;
    zMoving = false;

    isMovingToTarget = true;

    if (!isnan(x))
    {
        steppers.setTargetPosition(x * MICROSTEPPING * XSTEPPERMM, 0);
        xyMoving = true;
    }
    if (!isnan(y))
    {
        steppers.setTargetPosition(y * MICROSTEPPING * YSTEPPERMM, 1);
        steppers.setTargetPosition(y * MICROSTEPPING * YSTEPPERMM, 2);

        xyMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.setTargetPosition(z * 10);
        zMoving = true;
    }
    if (!isnan(t))
    {
        tStepper.setTargetPosition(t * MICROSTEPPING * TSTEPPERDEG);
        tMoving = true;
    }
}

void Movement::Update()
{
    bool moved = false;

    if(xyMoving)
    {
        xyMoving = steppers.run();
        moved = true;
    }
    if(tMoving)
    {
        tMoving = tStepper.run();
        moved = true;
    }
    if(zMoving)
    {
        zMoving = zStepper.run();
        moved = true;
    }

    isMovingToTarget = moved;
}