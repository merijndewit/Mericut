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
    steppers.addStepper(tStepper);
    xStepper.setAcceleration(STEPPERACCELERATION);
    yStepper.setAcceleration(STEPPERACCELERATION);
    yyStepper.setAcceleration(STEPPERACCELERATION);
    zStepper.setAcceleration(ZACCELERATION);
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
    xytMoving = false;
    zMoving = false;

    long xyPositions[4] = {long(targetPosition[0]), long(targetPosition[1]), long(targetPosition[1]), long(targetPosition[3])};

    isMovingToTarget = true;

    if (!isnan(x))
    {
        targetPosition[0] = (x * XSTEPPERMM) * MICROSTEPPING;
        xyPositions[0] = long((x * XSTEPPERMM) * MICROSTEPPING);
        xytMoving = true;
    }
    if (!isnan(y))
    {
        xyPositions[1] = long((y * YSTEPPERMM) * MICROSTEPPING);
        xyPositions[2] = long((y * YSTEPPERMM) * MICROSTEPPING);

        targetPosition[1] = (y * YSTEPPERMM) * MICROSTEPPING;
        xytMoving = true;
    }    
    if (!isnan(z))
    {
        zStepper.moveTo(z * MICROSTEPPING);
        targetPosition[2] = z;
        zMoving = true;
    }
    if (!isnan(t))
    {
        targetPosition[3] = ((t * TSTEPPERDEG) * MICROSTEPPING);
        xyPositions[3] = long((t * TSTEPPERDEG) * MICROSTEPPING);
        xytMoving = true;
    }
    if (xytMoving)
    {
        steppers.moveTo(xyPositions);
    }
}

void Movement::Move()
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