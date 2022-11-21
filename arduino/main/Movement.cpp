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
    xStepper.setAcceleration(STEPPERACCELERATION);
    yStepper.setAcceleration(STEPPERACCELERATION);
    yyStepper.setAcceleration(STEPPERACCELERATION);
    zStepper.setAcceleration(STEPPERACCELERATION);
    tStepper.setAcceleration(STEPPERACCELERATION);
    SetNormalSpeed();
}

void Movement::SetNormalSpeed()
{
    xStepper.setMaxSpeed(XYMAXSPEED);
    yStepper.setMaxSpeed(XYMAXSPEED);
    yyStepper.setMaxSpeed(XYMAXSPEED);
    zStepper.setMaxSpeed(ZMAXSPEED);
    tStepper.setMaxSpeed(TMAXSPEED);
}

void Movement::SetTravelSpeed()
{
    xStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    yyStepper.setMaxSpeed(XYMAXTRAVELSPEED);
    zStepper.setMaxSpeed(ZMAXTRAVELSPEED);
    tStepper.setMaxSpeed(TMAXTRAVELSPEED);
}

void Movement::SetTargetPosition(float x, float y, float z, float t)
{
    xyMoving = false;
    zMoving = false;
    tMoving = false;

    long xyPositions[3] = {long(targetPosition[0]), long(targetPosition[1]), long(targetPosition[1])};

    isMovingToTarget = true;
    //SyncMovementXY(x, y);
    if (!isnan(x))
    {
        targetPosition[0] = (x * XSTEPPERMM) * MICROSTEPPING;
        xyPositions[0] = long((x * XSTEPPERMM) * MICROSTEPPING);
        //xStepper.moveTo((x * XSTEPPERMM) * MICROSTEPPING);
        xyMoving = true;
    }
    if (!isnan(y))
    {
        //yStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        //yyStepper.moveTo((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[1] = long((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[2] = long((y * YSTEPPERMM) * MICROSTEPPING);

        targetPosition[1] = (y * YSTEPPERMM) * MICROSTEPPING;
        xyMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        targetPosition[2] = z;
        zMoving = true;
    }
    if (!isnan(t))
    {
        tStepper.moveTo((t * TSTEPPERDEG) * MICROSTEPPING);
        targetPosition[3] = t;
        tMoving = true;
    }
    if (xyMoving)
    {
        steppers.moveTo(xyPositions);
    }
}

void Movement::Move()
{
    int moved = 0;

    if(xyMoving)
    {
        xyMoving = steppers.run();
        moved++;
    }

    if(zMoving)
    {
        zMoving = zStepper.run();
        moved++;
    }
    if(tMoving)
    {
        tMoving = tStepper.run();
        moved++;
    }

    if (moved == 0)
    {
        isMovingToTarget = false;
    }
}